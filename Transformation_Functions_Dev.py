import requests
import json
from datetime import datetime
from pandas import json_normalize
import pandas as pd

# Returns a dictionary of top-level key-value pairs from a JSON/dict object.
def extract_top_level_keys(data):
    if isinstance(data, dict):
        return {key: value for key, value in data.items()}
    else:
        raise TypeError("Input must be a dictionary.")


# Returns count of each key value listing
def count_json_records(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)} items (list)")
        elif isinstance(value, dict):
            print(f"{key}: {len(value)} keys (dict)")
        else:
            print(f"{key}: single value ({type(value).__name__})")


#Recursively flattens all 'children' columns that contain dicts, lists, or tuples.
def flatten_children(df, max_depth=5):
    for _ in range(max_depth):
        children_cols = [col for col in df.columns if col == 'children']

        if not children_cols:
            break  # No more 'children' columns to flatten

        for col in children_cols:
            sample = df[col].dropna()
            if sample.empty:
                continue

            # Check type of the first non-null value
            sample_val = sample.iloc[0]

            if isinstance(sample_val, dict):
                # Expand dict into new columns
                expanded = df[col].apply(lambda x: pd.Series(x) if isinstance(x, dict) else None)
                expanded.columns = [f"{col}_{subcol}" for subcol in expanded.columns]
                df = df.drop(columns=[col]).join(expanded)

            elif isinstance(sample_val, (list, tuple)):
                # Explode lists/tuples into multiple rows
                df = df.explode(col).reset_index(drop=True)

                # Recurse into dicts within list after explode
                df[col] = df[col].apply(lambda x: x if isinstance(x, (dict, list, tuple)) else None)

                # If it's a dict again after explode, expand
                if df[col].apply(lambda x: isinstance(x, dict)).any():
                    expanded = df[col].apply(lambda x: pd.Series(x) if isinstance(x, dict) else None)
                    expanded.columns = [f"{col}_{subcol}" for subcol in expanded.columns]
                    df = df.drop(columns=[col]).join(expanded)

            else:
                continue  # Not a flattenable type

    return df


#return Children JSON
def json_subdf(name, data):
    subjson = data.get(name, [])
    df_ = pd.json_normalize(subjson)
    return df_



#Flattens any list, tuple, or dict in each column into multiple columns
def flatten_columns(df):
    flat_df = pd.DataFrame()

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, tuple, dict))).any():
            expanded = df[col].apply(
                lambda x: pd.Series(x) if isinstance(x, (list, tuple, dict)) else pd.Series([x])
            )
            # Rename new columns to show original col name
            expanded.columns = [f"{col}_{i}" for i in expanded.columns]
            flat_df = pd.concat([flat_df, expanded], axis=1)
        else:
            flat_df[col] = df[col]
    
    return flat_df


# Check each DataFrame unique values per column
def unique_value_counts_summary(df):
    summary = []
    for column in df.columns:
        unique_count = len(df[column].value_counts())
        summary.append((column, unique_count))
    return pd.DataFrame(summary, columns=["Column", "UniqueValues"])

