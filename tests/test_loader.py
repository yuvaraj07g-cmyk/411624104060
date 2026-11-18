from rti_mate.db.loader import fingerprint, to_row


def test_fingerprint_is_independent_of_mapping_order():
    assert fingerprint({"id": "1", "topic": "roads"}) == fingerprint(
        {"topic": "roads", "id": "1"}
    )


def test_to_row_splits_columns_and_json_metadata():
    record = {
        "id": "42",
        "decision_no": "CIC/2024/001",
        "published_on": "2024-03-31",
        "source_url": "https://example.test/decision/42",
        "topic": "roads",
    }

    row = to_row(record)

    assert row["external_id"] == "42"
    assert row["title"] == "CIC/2024/001"
    assert row["published_on"].isoformat() == "2024-03-31"
    assert row["metadata_"] == {"decision_no": "CIC/2024/001", "topic": "roads"}
    assert row["sha256"] == fingerprint(record)
