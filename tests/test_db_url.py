from sqlalchemy.engine import make_url

from rti_mate.db.url import to_asyncpg_url


def test_neon_url_is_converted_for_asyncpg():
    converted = make_url(
        to_asyncpg_url(
            "postgresql://user:secret@db.example.test/rti?sslmode=require&channel_binding=require"
        )
    )

    assert converted.drivername == "postgresql+asyncpg"
    assert converted.query["ssl"] == "require"
    assert "sslmode" not in converted.query
    assert "channel_binding" not in converted.query


def test_url_conversion_preserves_other_query_parameters():
    converted = make_url(
        to_asyncpg_url("postgres://user:secret@db.example.test/rti?application_name=rti-mate")
    )

    assert converted.drivername == "postgresql+asyncpg"
    assert converted.query["application_name"] == "rti-mate"
