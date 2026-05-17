from typing import Type

from seaql.core.plugin import DatabasePlugin


def get_plugin(name: str) -> Type[DatabasePlugin]:
    if name == 'mysql':
        from seaql.plugins.mysql import MySQLPlugin
        return MySQLPlugin
    elif name == 'postgres':
        from seaql.plugins.postgres import PostgresPlugin
        return PostgresPlugin
    elif name == 'sqlite':
        from seaql.plugins.sqlite import SQLitePlugin
        return SQLitePlugin
    raise KeyError(f'Unknown database type: {name}')
