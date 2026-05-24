from __future__ import annotations

import sys

from typing import Any

from .parseutils import is_destructive


class ConfirmBoolParamType:
    name = "confirmation"

    def convert(self, value: bool | str, param: Any = None, ctx: Any = None) -> bool:
        if isinstance(value, bool):
            return value
        value = value.lower()
        if value in ("yes", "y"):
            return True
        if value in ("no", "n"):
            return False
        raise ValueError(f"{value} is not a valid boolean")

    def __repr__(self) -> str:
        return "BOOL"


BOOLEAN_TYPE = ConfirmBoolParamType()


def confirm_destructive_query(queries: str) -> bool | None:
    prompt_text = "You're about to run a destructive command.\nDo you want to proceed? (y/n)"
    if is_destructive(queries) and sys.stdin.isatty():
        return bool(prompt(prompt_text, type=BOOLEAN_TYPE))
    return None


def confirm(*args: Any, **kwargs: Any) -> bool:
    try:
        default = kwargs.pop('default', False)
        prompt_text = args[0] if args else kwargs.pop('text', 'Confirm')
        suffix = ' [Y/n]' if default else ' [y/N]'
        value = input(prompt_text + suffix + ' ').strip().lower()
        if not value:
            return bool(default)
        return value in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        return False


def prompt(*args: Any, **kwargs: Any) -> Any:
    try:
        type_check = kwargs.pop('type', None)
        prompt_text = args[0] if args else kwargs.pop('text', '')
        while True:
            value = input(prompt_text + ' ').strip()
            if type_check and hasattr(type_check, 'convert'):
                try:
                    return type_check.convert(value, None, None)
                except ValueError as e:
                    print(e)
                    continue
            return value
    except (EOFError, KeyboardInterrupt):
        return False
