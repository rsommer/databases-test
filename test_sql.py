import pytest as _pytest
import databases as _db
import sqlalchemy as _sa
import sqlalchemy.sql as _sa_sql


_t = _sa_sql.text
m = _sa.MetaData()


testdata = _sa.Table(
    "testdata",
    m,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("description", _sa.String(length=100)),
)


@_pytest.mark.asyncio
@_pytest.mark.parametrize(
    "DB_URL", ["postgresql://pytest@localhost:5436/example", "sqlite:///example.db"]
)
async def test_sql(DB_URL):
    engine = _sa.create_engine(DB_URL)
    m.create_all(engine)
    try:
        engine.execute("INSERT INTO testdata VALUES (1, 'TESTDATA')")
    except Exception:
        # Ignore duplication
        pass

    database = _db.Database(DB_URL)
    await database.connect()

    query = _sa.select([_t("t.description")], from_obj=[_t("testdata t")])
    compiled = str(query)
    manual = """SELECT t.description \nFROM testdata t"""

    # Generated querys are identical
    assert compiled == manual

    result_raw = await database.fetch_one(manual)
    result_compiled = await database.fetch_one(query)
    result_alchemy = engine.execute(query).fetchone()

    assert dict(result_raw) == dict(result_compiled) == dict(result_alchemy)
