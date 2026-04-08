import streamlit as st
import pandas as pd

from parser.gemini_parser import read_file, parse_with_gemini
from parser.preprocess import clean_dataframe
from matcher.match_engine import match_transactions
from report.generate_report import generate_pdf

st.title("📊 Transaction Comparison AI")

st.write("Upload bank statement and finance records")

bank_file = st.file_uploader("Upload Bank Statement (PDF/Excel)")
finance_file = st.file_uploader("Upload Finance Record (Excel)")

if st.button("Run Comparison"):

    if not bank_file or not finance_file:
        st.error("Please upload both files")
    else:
        with st.spinner("Processing..."):

            # Parse
            bank_text = read_file(bank_file)
            finance_text = read_file(finance_file)

            bank_df = parse_with_gemini(bank_text)
            finance_df = parse_with_gemini(finance_text)

            # Clean
            bank_df = clean_dataframe(bank_df, "bank")
            finance_df = clean_dataframe(finance_df, "finance")

            # Match
            result_df = match_transactions(bank_df, finance_df)

            st.success("Done!")

            st.dataframe(result_df)

            # CSV download
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "result.csv")

            # Summary
            summary = {
                "total": len(result_df),
                "matched": (result_df["match_status"] == "exact").sum(),
                "fuzzy": (result_df["match_status"] == "fuzzy").sum(),
                "unmatched": (result_df["match_status"] == "unmatched").sum(),
            }

            pdf_file = generate_pdf(summary)

            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, "report.pdf")