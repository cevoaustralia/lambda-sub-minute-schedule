#%%
import re
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")


def parse_ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")


def extract_ts(filename="note/log-events-viewer-result.csv"):
    with open(filename, "r") as reader:
        lines = reader.readlines()
    ptn = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")
    return [parse_ts(ptn.search(l).group(0)) for l in lines if ptn.search(l) is not None]


def create_df():
    ts = extract_ts()
    df = pd.DataFrame(ts, columns=["timestamp"])
    df["invocation"] = df.index + 1
    df["interval"] = df.apply(lambda row: row["timestamp"].timestamp(), axis=1)
    return df.set_index(["timestamp", "invocation"]).diff().reset_index()


df = create_df()
print(df["interval"].describe())

sns.lineplot(x="invocation", y="interval", data=df).set_title("Interval by invocation")

# %%
