import logging
import os
import sys
import threading

import click
from prompt_toolkit.application import get_app
from prompt_toolkit.completion import DynamicCompleter, ThreadedCompleter
from prompt_toolkit.cursor_shapes import ModalCursorShapeConfig
from prompt_toolkit.enums import DEFAULT_BUFFER, EditingMode
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle, PromptSession

from .plugin import DatabasePlugin


class DbCliApp:
    """Shared REPL application for all database plugins."""

    def __init__(self, plugin: DatabasePlugin, connection_info: dict):
        self.plugin = plugin
        self.connection_info = connection_info
        self.logger = logging.getLogger(f'dbcli.{plugin.name}')
        self.query_history: list = []
        self.executor = None
        self.completer = None
        self.prompt_session: PromptSession | None = None
        self._completer_lock = threading.Lock()

        handler = logging.NullHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s'))
        root = logging.getLogger('dbcli')
        root.addHandler(handler)
        root.setLevel(logging.CRITICAL)

        self._connect()

    def _connect(self) -> None:
        try:
            self.executor = self.plugin.create_executor(self.connection_info)
            self.completer = self.plugin.create_completer(
                smart_completion=True,
                settings={'executor': self.executor},
            )
        except Exception as e:
            self.logger.debug('Connection failed: %r', e)
            click.secho(str(e), err=True, fg='red')
            sys.exit(1)

    def run_cli(self) -> None:
        self.prompt_session = PromptSession(
            lexer=self.plugin.lexer,
            reserve_space_for_menu=5,
            message=self._get_message(self.plugin.default_prompt),
            prompt_continuation=self._get_continuation('.'),
            complete_style=CompleteStyle.COLUMN,
            multiline=self._cli_is_multiline(),
            completer=ThreadedCompleter(DynamicCompleter(lambda: self.completer)),
            complete_while_typing=True,
            style=self.plugin.create_style('default', {}),
            include_default_pygments_style=False,
            search_ignore_case=True,
            cursor=ModalCursorShapeConfig(),
        )

        click.echo(f'{self.plugin.name} {self.plugin.version}')

        try:
            while True:
                try:
                    text = self.prompt_session.prompt()
                except KeyboardInterrupt:
                    continue
                except EOFError:
                    raise
                self._execute_and_display(text)
        except EOFError:
            click.echo('Goodbye!')

    def _get_message(self, prompt_format):
        def message():
            return ANSI(self._format_prompt(prompt_format))
        return message

    def _get_continuation(self, char):
        def continuation(width, line_number, is_soft_wrap):
            return [('class:continuation', char * (width - 1) + ' ')]
        return continuation

    @staticmethod
    def _multiline_exception(text: str) -> bool:
        text = text.strip()
        return (
            text.startswith("\\")
            or text.endswith(";")
            or text.endswith("\\g")
            or text.endswith("\\G")
            or text in ("exit", "quit", ":q", "")
        )

    def _cli_is_multiline(self):
        @Condition
        def cond():
            try:
                buf = get_app().layout.get_buffer_by_name(DEFAULT_BUFFER)
                if buf is None:
                    return True
                return not self._multiline_exception(buf.document.text)
            except Exception:
                return True
        return cond

    def _format_prompt(self, prompt_format):
        host = self.connection_info.get('host', '(none)')
        user = self.connection_info.get('user', '(none)')
        dbname = self.connection_info.get('database', '(none)')
        prompt = prompt_format.replace('\\u', user)
        prompt = prompt.replace('\\h', host)
        prompt = prompt.replace('\\d', dbname)
        return prompt

    def _execute_and_display(self, text: str) -> None:
        if not text.strip():
            return
        stripped = text.strip()
        if stripped.lower() in ('exit', 'quit', ':q', '\\q'):
            raise EOFError
        try:
            results = self.plugin.execute_query(self.executor, text)
            output = self.plugin.format_output(results, 'psql')
            for line in output:
                click.echo(line)
        except Exception as e:
            self.logger.error('sql: %r, error: %r', text, e)
            click.secho(str(e), err=True, fg='red')
