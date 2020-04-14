from datasette.app import Datasette
import sqlite_utils
import pytest
import httpx


@pytest.mark.asyncio
async def test_datasette_mask_columns(tmpdir):
    path = str(tmpdir / "foo.db")
    db = sqlite_utils.Database(path)
    db["users"].insert({"id": 1, "password": "secret"})
    datasette = Datasette([path], memory=True)
    # Without the plugin:
    async with httpx.AsyncClient(app=datasette.app()) as client:
        response = await client.get("http://localhost/foo/users.json?_shape=array")
        assert 200 == response.status_code
        assert [{"rowid": 1, "id": 1, "password": "secret"}] == response.json()
        # The text 'REDACTED' should not show up on the table page
        html_response = await client.get("http://localhost/foo/users")
        assert b"REDACTED" not in html_response.content
    # With the plugin:
    datasette2 = Datasette(
        [path],
        memory=True,
        metadata={
            "databases": {
                "foo": {"plugins": {"datasette-mask-columns": {"users": ["password"]}}}
            }
        },
    )
    async with httpx.AsyncClient(app=datasette2.app()) as client:
        response = await client.get("http://localhost/foo/users.json?_shape=array")
        assert 200 == response.status_code
        assert [{"rowid": 1, "id": 1, "password": None}] == response.json()
        # The text 'REDACTED' SHOULD show up on the table page
        html_response = await client.get("http://localhost/foo/users")
        assert b"REDACTED" in html_response.content
