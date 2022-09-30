# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# !pip install pinotdb

import pinotdb

connection = pinotdb.connect("pinot", 8000)

cursor = connection.cursor()

cursor.execute("""
SELECT * 
FROM baseballStats
LIMIT 20
""")

for row in cursor:
    print(row)

cursor.description

import pandas as pd

# +
cursor.execute("""
SELECT *
FROM baseballStats
""")


pd.DataFrame(cursor, columns=[value[0] for value in cursor.description])
