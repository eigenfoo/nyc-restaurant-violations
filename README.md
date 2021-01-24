# Data Dashboard — New York City Restaurant Violation Citations

> View dashboard here: https://share.streamlit.io/eigenfoo/nyc-restaurant-violations/main/app.py

This is a dashboard for New York City restaurant inspection results -
specifically, violation citations. The dataset is compiled and published by the
New York City Department of Health and Mental Hygeine (NYC DOHMH).

Built by [George Ho](https://eigenfoo.xyz/) using
[Streamlit](https://www.streamlit.io/).

## Overview

The underlying dataset contains "every sustained or not yet adjudicated
violation citation from every full or special program inspection conducted up
to three years prior to the most recent inspection for restaurants and college
cafeterias in an active status on [the date of the data pull]".

Upon startup, the dashboard pulls the latest dataset from the NYC Open Data
website, and is thus kept up-to-date. Unfortunately, this means that there is
no full historical view of data (i.e. the dashboard does not show all violation
citations ever for a particular restaurant).

In addition to this three-year sliding view of the data, there are two more
caveats to the dashboard:

1. **Only restaurants in active status are shown:** keep in mind that thousands
   of restaurants start and go out of business every year in New York City;
   only restaurants in an active status are included in the dataset.
2. **There may be data errors:** because the dataset is compiled from several
   large New York City administrative data systems, it may contain illogical
   values that could be a result of data entry or transfer errors. Data may
   also be missing.

## Links and References

- Dataset: [DOHMH New York City Restaurant Inspection Results
  Dataset](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j)
- Dataset FAQs: [NYC Restaurant Inspection
  FAQs](https://a816-health.nyc.gov/ABCEatsRestaurants/#/faq)
- Related work:
  * [Department of Health Letter Grades app, by Eater New
    York](https://ny.eater.com/2015/7/29/8780489/department-of-health-nyc-inspection)
  * [Visualizing New York City Restaurant Inspections, by SAP Analytics
    Cloud](https://saphanajourney.com/sap-analytics-cloud/resources/visualizing-new-york-city-restaurant-inspections-using-sap-analytics-cloud/)
