# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import streamlit as st

st.markdown("# Querying Baseball stats")
#
st.markdown("In this notebook we're going to learn how to query Apache Pinot using its Python driver. We'll then put the results into a Pandas DataFrame and create some pretty visualisations.")
#
# First, let's install some libraries:

# !pip install pinotdb plotly

# And now import libraries:

import pinotdb
import pandas as pd
import plotly.graph_objects as go

# Create a connection to Pinot and instantiate a cursor:

connection = pinotdb.connect("pinot", 8000)

cursor = connection.cursor()

st.markdown("Now, let's write a query to find the first 20 rows in the `baseballStats` table:")

cursor.execute("""
SELECT *
FROM baseballStats
LIMIT 20
""")

st.markdown("""
```sql
SELECT *
FROM baseballStats
LIMIT 20
```
""")

# Iterate over the cursor and print out those rows:

# for row in cursor:
#     print(row)

# We can get information about the columns from the `description` function:

# cursor.description

# Or we can use the `schema` function, which returns the same data in a slightly different format:

# cursor.schema

# Now let's query `baseballStats` and put the results into a DataFrame:

# +
cursor.execute("""
SELECT *
FROM baseballStats
""")

df = pd.DataFrame(
    cursor,
    columns=[value["name"] for value in cursor.schema]
)
df # Same as st.dataframe(df)

st.table(df)

# -

# So far, so good. How about if we find the teams that have scored the most home runs?

# +
cursor.execute("""
SELECT sum(homeRuns) AS totalHomeRuns, teamID
FROM baseballStats
GROUP BY teamID
ORDER BY totalHomeRuns DESC
""")

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)
df
# -

# And render the results using plot.ly!

# +
fig = go.FigureWidget(data=[
    go.Bar(x=df.teamID, y=df.totalHomeRuns)
])
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(showlegend=False, title=f"Home runs by team", margin=dict(l=0, r=0, t=40, b=0),)
fig.update_yaxes(range=[0, df.totalHomeRuns.max() * 1.1])

# fig.show(renderer='iframe')
st.plotly_chart(fig)
# -

# How about if we only want to find the top home run scorers for a specific year?

# +
cursor.execute("""
SELECT yearID as year, count(*)
FROM baseballStats
GROUP BY year
ORDER BY count(*) DESC
LIMIT 20
""")

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)

year = int(st.selectbox("Select year:", options=df.year.values))

# year = 2006
cursor.execute("""
SELECT sum(homeRuns) AS totalHomeRuns, teamID
FROM baseballStats
WHERE yearID = %(year)d
GROUP BY teamID
ORDER BY totalHomeRuns DESC
LIMIT 20
""", {"year": year})

df = pd.DataFrame(
    cursor,
    columns=[value[0] for value in cursor.description]
)


fig = go.FigureWidget(data=[
    go.Bar(x=df.teamID, y=df.totalHomeRuns)
])
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(showlegend=False, title=f"Home runs by team in {year}", margin=dict(l=0, r=0, t=40, b=0),)
fig.update_yaxes(range=[0, df.totalHomeRuns.max() * 1.1])

# fig.show(renderer='iframe')
st.plotly_chart(fig)
