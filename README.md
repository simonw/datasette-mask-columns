# datasette-mask-columns

[![PyPI](https://img.shields.io/pypi/v/datasette-mask-columns.svg)](https://pypi.org/project/datasette-mask-columns/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-mask-columns.svg?style=svg)](https://circleci.com/gh/simonw/datasette-mask-columns)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-mask-columns/blob/master/LICENSE)

Datasette plugin that masks specified database columns

## Installation

    pip install datasette-mask-columns

This depends on plugin hook changes in a not-yet released branch of Datasette. See [issue #678](https://github.com/simonw/datasette/issues/678) for details.

## Usage

In your `metadata.json` file add a section like this describing the database and table in which you wish to mask columns:

```json
{
    "databases": {
        "my-database": {
            "plugins": {
                "datasette-mask-columns": {
                    "users": ["password"]
                }
            }
        }
    }
}
```
All SQL queries against the `users` table in `my-database.db` will now return `null` for the `password` column, no matter what value that column actually holds.

The table page for `users` will display the text `REDACTED` in the masked column. This visual hint will only be available on the table page; it will not display his text for arbitrary queries against the table.
