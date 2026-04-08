import pandas as pd

def clean_dataframe(df, source):
    df = df.copy()

    df.columns = [c.lower() for c in df.columns]

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df["description"] = df["description"].astype(str).str.lower().str.strip()

    df["source"] = source

    df = df.dropna(subset=["date", "amount"])

    return df