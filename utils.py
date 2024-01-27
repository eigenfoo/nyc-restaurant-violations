import string

import pandas as pd

import streamlit as st


@st.cache_data(persist=True)
def get_restaurant_violation_data():
    """ Read CSV from NYC Open Data website. """
    CSV_URL = (
        "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
    )
    df = pd.read_csv(CSV_URL)
    return df


def normalize(s):
    """ Normalize a string. """
    if not isinstance(s, str):
        s = str(s)
    return string.capwords(" ".join(s.strip().split()))


def interpret_action(s):
    if not isinstance(s, str):
        s = str(s)

    if "establishment closed" in s.lower():
        return "we were closed by the DOHMH."
    elif "establishment re-opened" in s.lower():
        return "we were allowed to re-open by the DOHMH."
    elif "establishment re-closed" in s.lower():
        return "we were re-closed by the DOHMH."
    elif "violations were cited" in s.lower():
        return "we were cited for the following violation(s):"
    elif "no violations" in s.lower():
        return "we were inspected and no violations were found."
    else:
        return "we were inspected and no violations were found."


def summarize_violation_description(s):
    if not isinstance(s, str):
        s = str(s)
    return s.split(".")[0] + "."


def write_violations(violations):
    first_row = violations.iloc[0]  # Just get the first row

    # Display restaurant DBA as header
    st.header(normalize(first_row['DBA']))

    # Display building, street, and boro as a subheader on a new line
    st.subheader(
        f"{normalize(first_row['BUILDING'])} {normalize(first_row['STREET'])}, {normalize(first_row['BORO'])}"
    )

    violations.loc[:, "INSPECTION DATE"] = pd.to_datetime(
        violations.loc[:, "INSPECTION DATE"]
    )
    for _, indexes in sorted(
        violations.groupby(["INSPECTION DATE", "ACTION"]).groups.items(), reverse=True
    ):
        first_row = violations.loc[indexes].iloc[0]  # Just get the first row
        inspection_date = pd.to_datetime(first_row["INSPECTION DATE"])
        if pd.isnull(inspection_date):
            inspection_date = "N/A"
        else:
            inspection_date = inspection_date.strftime("%Y-%m-%d")

        if inspection_date == "1900-01-01":
            st.write("We've applied for a permit, but haven't been inspected yet.")
            return

        interpreted_action = interpret_action(first_row["ACTION"])
        st.write(
            f"On {inspection_date}, {interpreted_action}"
        )
        if "cited" in interpreted_action:
            # If there is a list of citations, write them. Critical citations first.
            days_violations = violations.loc[
                indexes, ["VIOLATION DESCRIPTION", "CRITICAL FLAG"]
            ].sort_values("CRITICAL FLAG", ascending=False)
            for _, (description, critical) in days_violations.iterrows():
                if critical == "Y":
                    st.write(f"  - **{summarize_violation_description(description)}**")
                else:
                    st.write(f"  - {summarize_violation_description(description)}")
