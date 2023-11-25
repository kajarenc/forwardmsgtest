import pandas as pd
import streamlit as st
from utils import download_file
from prometheus_client.parser import text_string_to_metric_families

st.title("Simple Streamlit app monitoring")


app_url = st.text_input(
    "Streamlit app url: ",
      placeholder="https://state-of-llm.streamlit.app"
)

app_url.removesuffix("/")
stat_url = f"{app_url}/~/+/_stcore/metrics"
st.write("\n")
st.write("\n")

if app_url:
    try:
        stats_response_content = download_file(stat_url)
    except Exception as e:
        st.error(str(e), icon="☝️")
    else:
        cache_types = []
        values = []

        for family in text_string_to_metric_families(stats_response_content):
            for sample in family.samples:
                cache_types.append(sample.labels["cache_type"])
                values.append(sample.value)

        st.subheader(
            "Memory consumed by cache primitives, session_state and ForwardMSGCache, in megabytes",
            divider="violet"
            )

        df = pd.DataFrame({
            "cache_type": cache_types,
            "value": values
        })
        left, _, right  = st.columns([4, 2, 4])

        grouped_by_df = df.groupby("cache_type").sum()
        grouped_by_df["value"]  = grouped_by_df["value"].div(1024 * 1024).round(3)

        with right:
            st.button("Refresh results")
            st.write("\n")
            st.dataframe(grouped_by_df)
        
        with left:
            st.bar_chart(grouped_by_df)