import streamlit as st
import pinotdb
import pandas as pd

connection = pinotdb.connect("pinot", 8000)
cursor = connection.cursor()

st.markdown("# Streamlit Metrics")

cursor.execute("""
SELECT distinct(yearID) AS year
FROM baseballStats
ORDER BY yearID DESC
LIMIT 20
""")

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)

starting_year=int(st.selectbox("Select starting year", options=df.year.values))
cursor.execute("""
SELECT sum(homeRuns) AS totalHomeRuns,
       sum(stolenBases) AS totalStolenBases,
       sum(strikeouts) AS totalStrikeouts
FROM baseballStats
WHERE yearID = %(year)d
""", {"year": starting_year})

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)

cursor.execute("""
SELECT sum(homeRuns) AS totalHomeRuns,
       sum(stolenBases) AS totalStolenBases,
       sum(strikeouts) AS totalStrikeouts
FROM baseballStats
WHERE yearID = %(year)d
""", {"year": starting_year-1})

df_prev = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)

st.subheader(f"Year: {starting_year}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Home Runs",
        value=df.totalHomeRuns.values[0],
        delta=df.totalHomeRuns.values[0]-df_prev.totalHomeRuns.values[0]
    )

with col2:
    st.metric(
        label="Stolen Bases",
        value=df.totalStolenBases.values[0],
        delta=df.totalStolenBases.values[0]-df_prev.totalStolenBases.values[0]
    )

with col3:
    st.metric(
        label="Strikeouts",
        value=df.totalStrikeouts.values[0],
        delta=df.totalStrikeouts.values[0]-df_prev.totalStrikeouts.values[0],
        delta_color="inverse"
    )
