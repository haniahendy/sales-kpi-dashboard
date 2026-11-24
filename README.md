# sales-kpi-dashboard

Streamlit dashboard for sales KPIs (revenue, units, average price, month-over-month change, top regions) with region/category filters. KPI logic lives in `kpi/metrics.py` as pure pandas functions with tests; `app.py` only draws it.

## Run
```bash
pip install -r requirements.txt
python -m pytest -q        # 5 tests
streamlit run app.py
```

## Data
Fully **synthetic** (`make_sales`, fixed seed): 180 days, 3 regions, 3 categories, weekly seasonality. Numbers mean nothing about a real business. To use real data, load a CSV with columns `date, region, category, units, revenue`.

## Limits
No database connection or caching, the UI is not covered by automated tests (only the metric functions are), the first/last month may be partial and distort month-over-month.

## Provenance
A learning and portfolio project.

Filter behavior: an empty Region or Category selection means no filter on that field (checked with Streamlit AppTest).
