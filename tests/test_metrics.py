import pandas as pd

from kpi.metrics import filter_data, kpi_summary, make_sales, month_over_month, top_n


def small():
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-01-10", "2026-01-20", "2026-02-10"]),
        "region": ["Cairo", "Giza", "Cairo"], "category": ["Home", "Home", "Fashion"],
        "units": [2, 3, 5], "revenue": [20.0, 60.0, 100.0]})


def test_kpi_summary():
    assert kpi_summary(small()) == {"revenue": 180.0, "units": 10, "avg_price": 18.0}


def test_kpi_summary_empty_and_zero_units():
    assert kpi_summary(small().iloc[0:0])["revenue"] == 0.0
    z = small().assign(units=0)
    assert kpi_summary(z)["avg_price"] == 0.0


def test_month_over_month():
    m = month_over_month(small())
    assert m["revenue"].tolist() == [80.0, 100.0]
    assert m["mom_change_pct"].iloc[1] == 25.0


def test_top_n_and_filter():
    assert top_n(small(), "region", 1)["region"].iloc[0] == "Cairo"
    assert len(filter_data(small(), regions=["Giza"])) == 1
    assert len(filter_data(small(), start="2026-02-01")) == 1


def test_synthetic_data_is_deterministic_and_clean():
    a, b = make_sales(), make_sales()
    assert a.equals(b)
    assert (a["units"] >= 0).all() and a["revenue"].notna().all()
    assert len(a) == 180 * 9
