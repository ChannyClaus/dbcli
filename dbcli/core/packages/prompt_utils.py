import click


def confirm(prompt):
    return click.prompt(prompt, default='y')


def confirm_destructive_query(query, warning_keywords, dsn_alias=None):
    if warning_keywords and any(kw in query.upper() for kw in warning_keywords):
        return click.confirm('You are about to run a destructive command.\nDo you want to proceed?', default=False)
    return True
