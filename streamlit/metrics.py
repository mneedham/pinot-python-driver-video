import streamlit as st
import pinotdb
import pandas as pd

st.markdown("# Streamlit Metrics")

connection = pinotdb.connect("pinot", 8000)
cursor = connection.cursor()

year = 2006
cursor.execute("""
SELECT sum(homeRuns) AS totalHomeRuns
FROM baseballStats
WHERE yearID = %(year)d
""", {"year": year})

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)
st.dataframe(df)