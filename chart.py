# %%
import re
from datetime import datetime
from IPython.display import display
import pandas as pd
import seaborn as sns


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
    df["interval"] = df.apply(lambda row: row["timestamp"].timestamp() * 1000, axis=1)
    df = df.set_index(["timestamp", "invocation"]).diff().reset_index()
    df["delay"] = df.apply(lambda row: row["interval"] - 10000, axis=1)
    return df


df = create_df()

sns.set_theme(style="darkgrid")
sns.lineplot(x="invocation", y="delay", data=df).set_title("Delay by invocation")

# %%
display(pd.DataFrame(df[df.invocation >= 200]["delay"].describe()))
