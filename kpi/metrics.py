"""Pure functions for sales KPIs, kept separate from the Streamlit UI so they can be tested."""
import numpy as np
import pandas as pd


def make_sales(seed: int = 3, days: int = 180) -> pd.DataFrame:
    """Synthetic daily sales by region/category with weekly seasonality."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=days, freq="D")
    rows = []
    for region in ["Cairo", "Alexandria", "Giza"]:
        for cat in ["Electronics", "Home", "Fashion"]:
            base = rng.uniform(80, 200)
            weekly = 1 + 0.25 * np.sin(2 * np.pi * dates.dayofweek / 7)
            units = rng.poisson(base * weekly / 10)
            price = rng.uniform(20, 120)
            rows.append(pd.DataFrame({"date": dates, "region": region, "category": cat,
                                      "units": units, "revenue": (units * price).round(2)}))
    return pd.concat(rows, ignore_index=True)


def kpi_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"revenue": 0.0, "units": 0, "avg_price": 0.0}
    units = int(df["units"].sum())
    revenue = float(df["revenue"].sum())
    return {"revenue": round(revenue, 2), "units": units, "avg_price": round(revenue / units, 2) if units else 0.0}


def month_over_month(df: pd.DataFrame) -> pd.DataFrame:
    m = df.assign(month=df["date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["revenue"].sum()
    m["mom_change_pct"] = (m["revenue"].pct_change() * 100).round(1)
    return m


def top_n(df: pd.DataFrame, by: str, n: int = 3) -> pd.DataFrame:
    return df.groupby(by, as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(n).reset_index(drop=True)


def filter_data(df: pd.DataFrame, regions=None, categories=None, start=None, end=None) -> pd.DataFrame:
    out = df
    if regions:
        out = out[out["region"].isin(regions)]
    if categories:
        out = out[out["category"].isin(categories)]
    if start is not None:
        out = out[out["date"] >= pd.Timestamp(start)]
    if end is not None:
        out = out[out["date"] <= pd.Timestamp(end)]
    return out
