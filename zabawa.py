import pandas as pd

df = pd.read_json('test2.jsonl', lines=True)

df["month"] = df["year"].astype(str).str.split().str[1]

monthlist = ["January","February","March","April","May","June","July",
            "August","September","October","November","December"]

df2 = df.groupby(["month"]).mean().sort_values(by=['average_rating'])

print(df2.query("month in @monthlist"))