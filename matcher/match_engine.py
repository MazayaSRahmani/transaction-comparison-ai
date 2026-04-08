import pandas as pd
from rapidfuzz import fuzz

def match_transactions(bank_df, finance_df, tolerance=0.02):
    results = []

    for _, b in bank_df.iterrows():
        best_match = None
        best_score = 0

        for _, f in finance_df.iterrows():
            amount_match = abs(b["amount"] - f["amount"]) <= tolerance * b["amount"]

            desc_score = fuzz.token_sort_ratio(b["description"], f["description"]) / 100

            score = (0.6 * amount_match) + (0.4 * desc_score)

            if score > best_score:
                best_score = score
                best_match = f

        if best_score == 1:
            status = "exact"
        elif best_score > 0.7:
            status = "fuzzy"
        else:
            status = "unmatched"

        results.append({
            "bank_date": b["date"],
            "bank_desc": b["description"],
            "bank_amount": b["amount"],
            "match_status": status,
            "confidence": best_score
        })

    return pd.DataFrame(results)