import pandas as pd
from IPython.display import display, Markdown
import src.report.tree as tr
from pathlib import Path

def read_csv(path):
    df = pd.read_csv(path, sep='\t', quotechar='"', encoding='utf-8')

    return df

def format_data(data):
    """
    Accepts either a dataframe or a file path.
    Adds 'date', 'month', 'year', 'year_month', and 'country' columns
    if usable source columns exist.
    """

    # --- allow path OR dataframe input ---
    if isinstance(data, (str, Path)):
        df = pd.read_csv(data)
    else:
        df = data.copy()

    # --- find a usable date column ---
    date_cols = ["Collection_Date"]
    date_col = next((c for c in date_cols if c in df.columns), None)

    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")
        df["month"] = df["date"].dt.strftime("%m")
        df["year"] = df["date"].dt.strftime("%Y")
        df["year_month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    else:
        df["date"] = pd.NaT
        df["month"] = pd.NaT
        df["year"] = pd.NaT
        df["year_month"] = pd.NaT

    # --- extract country from Location like "Region/Country/..." ---
    loc_cols = ["Location"]
    loc_col = next((c for c in loc_cols if c in df.columns), None)

    if loc_col:
        df["country"] = (
            df[loc_col]
            .astype(str)
            .str.split("/")
            .str[1]
            .str.strip()
        )
    else:
        df["country"] = pd.NA

    return df

# def report_subtype(df):
#     for st, st_df in df.groupby("subtype"):
#         display(Markdown(f"### {st}"))
#         display(st_df)
        
#         tree_file = Path(f"data/{st}.nwk")
#         if tree_file.exists():
#             fig = tr.plot_tree(tree_file, st_df, ['state', 'year_month'])
#             display(fig)
