"""Database plugin interface."""

from abc import ABC, abstractmethod
from typing import Any

from prompt_toolkit.completion import Completer
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style


class DatabasePlugin(ABC):
    """A database backend plugin providing database-specific functionality."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def version(self) -> str: ...

    @property
    @abstractmethod
    def lexer(self) -> PygmentsLexer: ...

    @property
    def default_prompt(self) -> str:
        return "\\u@\\h:\\d> "

    @abstractmethod
    def create_style(self, syntax_style: str, cli_style: dict) -> Style: ...

    def create_output_style(self, syntax_style: str, cli_style: dict) -> Any:
        return None

    @abstractmethod
    def create_completer(self, smart_completion: bool, settings: dict) -> Completer: ...

    @abstractmethod
    def create_executor(self, connection_info: dict) -> Any: ...

    @abstractmethod
    def execute_query(self, executor: Any, query: str) -> list[tuple]:
        """Execute a query and return list of (title, rows, headers, status)."""
        ...

    @abstractmethod
    def format_output(self, results: list[tuple], table_format: str) -> list[str]:
        """Format query results into output lines."""
        ...

    @abstractmethod
    def connect(self, args: list[str]) -> dict: ...

    @abstractmethod
    def get_default_config_path(self) -> str: ...

    def get_default_config_content(self) -> str:
        return ''
