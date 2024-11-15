import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Sample Data Generation (Replace this with actual data)
user_count = 33
collections_count = 42
ingested_files = 10900
searches_count = 3900
conversations_count = 192
market_reports_count = 16

# Generate a sample DataFrame for "Questions Asked Trend" and "Active Users"
date_range = pd.date_range(start="2024-10-15", end="2024-11-14")
questions_data = pd.DataFrame({
    'Date': date_range,
    'Queries Count': [int(abs(100 * (0.5 - i % 7 / 10))) for i in range(len(date_range))]
})

# Generate sample data for "Questions by Collection"
collection_data = pd.DataFrame({
    'Collection': ['Market-Intel-Data-Processing', 'Adtalem-student-bot-v', 'Chicago HR Policies',
                   'tropicana-demo-bot', 'Irving-demo', 'EDU_Demo', 'frenchopendemo',
                   'GoSpotCheck_Trop', 'EDU_VirtualTA'],
    'Percentage': [51.41, 10.02, 7.25, 6.54, 3.82, 3.35, 2.93, 1.53, 1.4]
})

# Sidebar title
st.sidebar.title("Chatbot Interaction Dashboard")

# Display metrics at the top
st.write("### Summary Metrics")
cols = st.columns(6)
metrics = [
    ("Users", user_count),
    ("Collections", collections_count),
    ("Ingested Files", ingested_files),
    ("Searches", searches_count),
    ("Conversations", conversations_count),
    ("Market Reports", market_reports_count),
]
for col, (metric_name, metric_value) in zip(cols, metrics):
    col.metric(metric_name, f"{metric_value:,}")

# Questions Asked Trend over Time
st.write("### Questions Asked Trend")

# Add mouseover vertical line tooltip for "Questions Asked Trend"
nearest = alt.selection_point(nearest=True, on="pointerover", fields=["Date"], empty=False)

line = alt.Chart(questions_data).mark_line().encode(
    x="Date:T",
    y="Queries Count:Q"
)

selectors = alt.Chart(questions_data).mark_point().encode(
    x="Date:T",
    opacity=alt.value(0),
).add_params(
    nearest
)

points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Tooltip includes both Date and Queries Count
rules = alt.Chart(questions_data).mark_rule(color="gray").encode(
    x="Date:T",
    tooltip=[alt.Tooltip('Date:T', title='Date'),
             alt.Tooltip('Queries Count:Q', title='Queries Count')]
).transform_filter(
    nearest
)

trend_chart = alt.layer(
    line, selectors, points, rules
).properties(
    width=700, height=300
)

st.altair_chart(trend_chart, use_container_width=True)

# Questions by Collection Pie Chart
st.write("### Questions by Collection")
pie_chart = alt.Chart(collection_data).mark_arc().encode(
    theta=alt.Theta(field="Percentage", type="quantitative"),
    color=alt.Color(field="Collection", type="nominal"),
    tooltip=["Collection", "Percentage"]
).properties(width=350, height=350)
st.altair_chart(pie_chart, use_container_width=True)

# Active Users Trend
st.write("### Active Users")
active_users_data = questions_data.copy()
active_users_data['Users Count'] = (active_users_data['Queries Count'] // 10).clip(upper=8)

nearest_active = alt.selection_point(nearest=True, on="pointerover", fields=["Date"], empty=False)

# Active Users Trend without interpolation
line_active = alt.Chart(active_users_data).mark_line().encode(
    x="Date:T",
    y="Users Count:Q"
)

selectors_active = alt.Chart(active_users_data).mark_point().encode(
    x="Date:T",
    opacity=alt.value(0),
).add_params(
    nearest_active
)

points_active = line_active.mark_point().encode(
    opacity=alt.condition(nearest_active, alt.value(1), alt.value(0))
)

# Tooltip includes both Date and Users Count
rules_active = alt.Chart(active_users_data).mark_rule(color="gray").encode(
    x="Date:T",
    tooltip=[alt.Tooltip('Date:T', title='Date'),
             alt.Tooltip('Users Count:Q', title='Users Count')]
).transform_filter(
    nearest_active
)

active_users_chart = alt.layer(
    line_active, selectors_active, points_active, rules_active
).properties(
    width=700, height=300
)

st.altair_chart(active_users_chart, use_container_width=True)
