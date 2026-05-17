from typing import Type

from dbcli.core.plugin import DatabasePlugin


def get_plugin(name: str) -> Type[DatabasePlugin]:
    if name == 'mysql':
        from dbcli.plugins.mysql import MySQLPlugin
        return MySQLPlugin
    elif name == 'postgres':
        from dbcli.plugins.postgres import PostgresPlugin
        return PostgresPlugin
    elif name == 'sqlite':
        from dbcli.plugins.sqlite import SQLitePlugin
        return SQLitePlugin
    raise KeyError(f'Unknown database type: {name}')
