import pytest

@pytest.mark.data
@pytest.mark.skip(reason="ApiClient and DbClient not implemented yet")
def test_sample_data_parity(settings, api, db):
    # Placeholder parity test: adapt to your schema
    # TODO: Implement ApiClient and DbClient when needed
    # API: fetch count
    r = api.get("/customers/count")
    assert r.status_code == 200
    api_count = r.json().get("count", 0)

    # DB: fetch count
    row = db.fetch_one("SELECT COUNT(*) as c FROM customers")
    db_count = row["c"] if row else 0

    # Expect near parity (allow small lag)
    assert abs(api_count - db_count) <= 5
