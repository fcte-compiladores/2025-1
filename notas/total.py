from collections import Counter

import pandas as pd
import rich


def final(x: float) -> str:
    e = 2.0
    if x <= 0.0:
        return "SR"
    if x < 30.0 - e:
        return "II"
    if x < 50.0 - e:
        return "MI"
    elif x < 70.0 - e:
        return "MM"
    elif x < 90.0 - e:
        return "MS"
    else:
        return "SS"


p1 = pd.read_csv("p1.csv", index_col=0)
p2 = pd.read_csv("p2.csv", index_col=0)
p3 = pd.read_csv("p3.csv", index_col=0)
ta = pd.read_csv("trabalho-a.csv", index_col=0)
tb = pd.read_csv("trabalho-b.csv", index_col=0)
tf = pd.read_csv("trabalho-b.csv", index_col=0) * 0  # todo, !
roster = pd.read_csv("../roster.csv", dtype=str)

id_map = dict(zip(roster["github_id"].values, roster["id"].values))
id_map = {k.removeprefix("@"): v for k, v in id_map.items()}
id_map.update(
    {
        # ...
    }
)
rich.print(id_map)

df = pd.DataFrame(
    {
        "p1": p1["total"],
        "p2": p2["total"],
        "p3": p3["total"],
        "exercicios": ta["total"] + tb["total"],
        "trabalho": tf["total"],
    }
)
df = df.fillna(0.0).round(2)
df["total"] = df.sum(axis=1) - df.min(axis=1)
df.index = [id_map.get(x, f"gh:{x}") for x in df.index]  # type: ignore
df["mencao"] = df["total"].apply(final)
df.to_csv("notas.csv")

# Summary
summary = df.describe().T.round(2)
del summary["count"]
print(summary)


print("\n\nData loaded successfully.")
print("p1: ", p1.shape)
print("p2: ", p2.shape)
print("p3: ", p3.shape)
print("ta: ", ta.shape)
print("tb: ", tb.shape)
print("tf: ", tf.shape)
print("df: ", df.shape)

rich.print(Counter(df["mencao"]))
