import pandas as pd

def get_data(filename):
    df = pd.read_csv(filename)

    sorted_df = df.sort_values(by=['popularity'], ascending=False)
    top = {}
    top["top"] = [i for i in range(1, 11)]
    top["show"] = sorted_df["title"][:10]
    top["popularity"] = sorted_df["popularity"][:10]
    top["sensitivity"] = sorted_df["sensitivity"][:10]
    popularity_df = pd.DataFrame(data=top)

    sorted_df = df.sort_values(by=['sensitivity'], ascending=False)
    top = {}
    top["top"] = [i for i in range(1, 11)]
    top["show"] = sorted_df["title"][:10]
    top["popularity"] = sorted_df["popularity"][:10]
    top["sensitivity"] = sorted_df["sensitivity"][:10]
    sensitivity_df = pd.DataFrame(data=top)

    return df, popularity_df, sensitivity_df