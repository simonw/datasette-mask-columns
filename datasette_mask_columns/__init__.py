from datasette import hookimpl
import jinja2
import sqlite3


def make_authorizer(datasette, database):
    def authorizer(action, table, column, db_name, trigger_name):
        if action != sqlite3.SQLITE_READ:
            return sqlite3.SQLITE_OK
        masks = (
            datasette.plugin_config("datasette-mask-columns", database=database) or {}
        )
        columns_to_mask = masks.get(table) or None
        if not columns_to_mask:
            return sqlite3.SQLITE_OK
        if column in columns_to_mask:
            return sqlite3.SQLITE_IGNORE
        else:
            return sqlite3.SQLITE_OK

    return authorizer


@hookimpl
def prepare_connection(conn, database, datasette):
    conn.set_authorizer(make_authorizer(datasette, database))


@hookimpl()
def render_cell(column, table, database, datasette):
    masks = datasette.plugin_config("datasette-mask-columns", database=database) or {}
    columns_to_mask = masks.get(table) or set()
    if column in columns_to_mask:
        return jinja2.Markup(
            '<span style="font-size: 0.8em; color: red; opacity: 0.8">REDACTED</span>'
        )
