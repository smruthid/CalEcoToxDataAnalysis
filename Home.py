import streamlit as st

st.set_page_config(
    page_title="CSEN 377 Data Visualization Team 6 Final Project",
)

st.sidebar.success("Select a visualization to explore.")

st.markdown(
"""
    ## Explore toxins and their effects on California wildlife
   
    Chemicals are widely used in industry and commercial practices. Farms use
    pesticides, and factories use catalysts and produce waste. 

    Unfortunately, as a result of these activities, these chemicals also enter
    the ecosystem. This can be unavoidable (pesticides that are sprayed will
    be carried away by wind currents) or deliberate (illegal dumping of unwanted 
    byproducts). 

    What animals are affected by this contamination? *How* are they affected?

    CalEcoTox contains a vast quantity of data that can help researchers answer
    this question, but it can be difficult to work with. 

    Our visualizations give a high-level view of the toxicity data hosted by
    CalEcoTox. It is our hope that this allows users to more easily understand
    dangerous chemicals and how wildlife is affected.
"""
)
