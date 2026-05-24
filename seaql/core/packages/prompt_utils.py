def confirm(prompt):
    default = 'y'
    value = input(f"{prompt} [{default}]: ").strip().lower()
    return value if value else default


def confirm_destructive_query(query, warning_keywords, dsn_alias=None):
    if warning_keywords and any(kw in query.upper() for kw in warning_keywords):
        value = input('You are about to run a destructive command.\nDo you want to proceed? [y/N]: ').strip().lower()
        return value == 'y'
    return True
