""" NYC Restaurant Violations Data App """

import urllib

import streamlit as st
import utils

# Define title and sidebar

st.title("NYC Restaurant Violations")

name = st.sidebar.text_input("Restaurant Name:", "")
name = name.strip().upper()

street = st.sidebar.text_input("Street:", "")
street = street.strip().upper()

boro = st.sidebar.selectbox(
    "Borough:", ["", "Manhattan", "Queens", "Brooklyn", "Staten Island", "Bronx"]
)

st.sidebar.markdown(
    """
    More details [on the README](https://github.com/eigenfoo/nyc-restaurant-violations/blob/main/README.md).

    Source code available [on GitHub](https://github.com/eigenfoo/nyc-restaurant-violations).

    Built by [George Ho](https://eigenfoo.xyz/).
    """
)

# Get and cache data

try:
    df = utils.get_restaurant_violation_data()
except urllib.error.URLError as err:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: {}
        """.format(
            err.reason
        )
    )

# Query data

query = " & ".join(
    [
        f'{column_name}.str.contains("{field}", na=False)'
        for column_name, field in [("DBA", name), ("BORO", boro), ("STREET", street)]
        if field
    ]
)

if not query:
    st.write("Welcome! Search on the sidebar to get started.")
else:
    filtered = df.query(query, engine="python")
    num_results = filtered["CAMIS"].nunique()

    if num_results > 1000:
        st.write("Welcome! Search on the sidebar to get started.")
    elif num_results > 100:
        st.write("That's too many results! Please narrow down your search.")
    elif num_results == 0:
        msg = """
        Restaurant not found!

        If you're sure that your query is right, then there are two possible
        reasons why your restaurant is not found:

        - **The restaurant is not in active status:** keep in mind that
          thousands of restaurants start and go out of business every year in
          New York City; only restaurants in an active status are included in
          the dataset.
        - **Data error:** because this dataset is compiled from several large
          New York City administrative data systems, it may contain illogical
          values that could be a result of data entry or transfer errors. Data
          may also be missing.

        For more details, check out [the dataset on the NYC Open Data
        website](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j).
        """
        st.write(msg)
    elif num_results > 1:
        choices = filtered[
            ["CAMIS", "DBA", "BUILDING", "STREET", "BORO", "CUISINE DESCRIPTION"]
        ].drop_duplicates()
        choices = [
            (
                row["CAMIS"],
                (
                    f"{utils.normalize(row['DBA'])}: "
                    f"{utils.normalize(row['BUILDING'])} "
                    f"{utils.normalize(row['STREET'])}, "
                    f"{utils.normalize(row['BORO'])}. "
                    f"(Cuisine: {utils.normalize(row['CUISINE DESCRIPTION'])})"
                ),
            )
            for _, row in choices.iterrows()
        ]

        # Pagination with buttons
        display_limit = 15
        num_pages = (len(choices) + display_limit - 1) // display_limit

        # Display page selector before radio button list
        page = st.number_input("Select Page", 1, num_pages, 1)

        # Calculate the range of choices to display for the selected page
        start_index = (page - 1) * display_limit
        end_index = min(start_index + display_limit, len(choices))
        display_choices = choices[start_index:end_index]

        # Display the choices
        selected_str = st.radio(
            "You're probably looking for one of these restaurants, right?",
            [s for _, s in display_choices],
        )
        selected_camis = [camis for camis, s in display_choices if s == selected_str]
        filtered = df.query(f"CAMIS == {selected_camis}")
        st.write("---")
        utils.write_violations(filtered)
    else:
        utils.write_violations(filtered)
