import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st

from kpi.metrics import filter_data, kpi_summary, make_sales, month_over_month, top_n

st.title("Sales KPI dashboard (synthetic data)")
df = make_sales()
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
st.sidebar.caption("Leaving a filter empty means no filter on that field.")
view = filter_data(df, regions, cats)
k = kpi_summary(view)
c1, c2, c3 = st.columns(3)
c1.metric("Revenue", f"{k['revenue']:,.0f}")
c2.metric("Units", f"{k['units']:,}")
c3.metric("Avg price", f"{k['avg_price']:.2f}")
mom = month_over_month(view)
st.subheader("Revenue by month")
fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(mom["month"], mom["revenue"], color="#2a6f97")
ax.set_ylabel("Revenue")
ax.set_title("Monthly revenue (filtered view)")
fig.tight_layout()
st.pyplot(fig)
st.dataframe(mom)
st.subheader("Top regions")
st.dataframe(top_n(view, "region"))
