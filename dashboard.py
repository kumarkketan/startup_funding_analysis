import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.set_page_config(layout="wide", page_title="Start-up Analysis Dashboard")


df = pd.read_csv("clean_data.csv")

# Adding a Sidebar to webpage 
st.sidebar.title("Startup Funding Analysis")
pages = ["Overall Analysis", "Startups Analysis", "Investor Analysis"]
btn1 = st.sidebar.selectbox("Select Your Choice", pages)

# Key statistics
total = f"{round(df['Funding_Amount_in_cr'].sum(), 2)} Cr"
max_ = f"{round(df['Funding_Amount_in_cr'].max(), 2)} Cr"

# Top industries based on funding
top = (
    df.groupby("Industry_Vertical")["Funding_Amount_in_cr"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)
df_top_industries = pd.DataFrame(top).reset_index()  # Prepare DataFrame for plotting

# Top 10 funded startups
df_sorted = df.sort_values(by="Funding_Amount_in_cr", ascending=False).head(10)

# Conditional rendering based on selected page
if btn1 == pages[0]:  # Overall Analysis
    a, b = st.columns(2)
    with a:
        st.title("Indian Startup Analysis")
        st.write(''' Explore the vibrant Indian startup ecosystem with this comprehensive analysis platform. Gain insights into funding patterns, 
                 leading industries, and prominent investors driving innovation. Discover top-performing startups, funding milestones, and trends 
                 shaping India's entrepreneurial growth story.''')
    with b:
        st.image("Startup_Analysis.png")
    st.markdown(
    "<hr style='border: 1px solid #FF5733;'>", unsafe_allow_html=True
)
    st.markdown(
    "<h3 style='text-align: center;'>Key Performance Indicators</h3>", 
    unsafe_allow_html=True
)

#     st.markdown(
#     "<hr style='border: 1px solid #FF5733;'>", unsafe_allow_html=True
# )

    x, y,z = st.columns(3)
    with x:
        st.metric(label="Total Funding Raised", value=total)
    with y:
        st.metric(label="Maximum Funding Raised", value=max_)
    with z:
        st.metric(label="Maximum Funding Raised", value=max_)
    st.markdown(
    "<hr style='border: 1px solid #FF5733;'>", unsafe_allow_html=True
)
    # Display a bar chart for top industries by funding
    st.subheader("Top Industries by Funding")
    bar_chart = alt.Chart(df_top_industries).mark_bar().encode(
        x=alt.X("Funding_Amount_in_cr:Q", title="Total Funding (Cr)"),
        y=alt.Y("Industry_Vertical:N", sort="-x", title="Industry Vertical"),
        color=alt.Color("Industry_Vertical:N", legend=None),
    )

    st.altair_chart(bar_chart, use_container_width=True)
    st.markdown(
    "<hr style='border: 1px solid #FF5733;'>", unsafe_allow_html=True
)
    st.subheader("Top Funding Companies")
    st.dataframe(df_sorted.reset_index(drop=True))
    st.markdown(
    "<hr style='border: 1px solid #FF5733;'>", unsafe_allow_html=True
)


elif btn1 == pages[1]:  # Startups Analysis
    st.subheader("Startups Analysis")
    # Add content here for startups analysis if needed

elif btn1 == pages[2]:  # Investor Analysis
    # Sidebar input to choose an investor

    a, b = st.columns(2)
    with a:
        st.title("Invester Analysis")
        st.write('''Explore comprehensive insights into investment trends and performance across industries.
                  This dashboard provides an overview of investing companies, highlighting their total funding contributions, top-funded industries, and key metrics.\n
* Track Leading Investors: Gain insights into top investing companies and their contribution to various industries.
* Funding Trends: Visualize funding patterns over time and across sectors to identify market dynamics.
* Industry Highlights: Discover which industries attract the highest investments and analyze sector-specific funding. ''')
    st.write('-'*4) 
    with b:
        st.image("investment.png")
    btn2 = st.sidebar.selectbox("Choose your Investor", df["Invester_name"].unique())
    st.subheader(btn2)
    # Display total investment by selected investor
    total_investment = df.groupby("Invester_name")["Funding_Amount_in_cr"].sum().loc[btn2]
    h, i, j = st.columns(3)

    with h:
        # st.markdown("<h5 style='text-align: center; color: #4CAF50;'>💰 Total Investment</h5>", unsafe_allow_html=True)
        st.metric(label=f"Total Investment: {total} Cr", value=f"{total} Cr")

    with i:
        # st.markdown("<h5 style='text-align: center; color: #FF5733;'>📈 Maximum Investment</h5>", unsafe_allow_html=True)
        st.metric(label=f"Maximum Investment: {max_} Cr", value=f"{max_} Cr")

    with j:
        # st.markdown("<h5 style='text-align: center; color: #2196F3;'>📉 Minimum Investment</h5>", unsafe_allow_html=True)
        st.metric(label=f"Minimum Investment: {max_} Cr", value=f"{max_} Cr")

        # Show a line chart for funding by industry for the selected investor
    investor_funding = df[df["Invester_name"] == btn2].groupby("Industry_Vertical")["Funding_Amount_in_cr"].sum().reset_index()
        
        # Ensure there is data to display

    x,y=st.columns(2)
    with x:
        if not investor_funding.empty:
            st.write(f"Funding by Industry for {btn2}")
            bar_chart = alt.Chart(investor_funding).mark_bar().encode(
                    x=alt.X("Industry_Vertical:N", title="Industry Vertical"),
                    y=alt.Y("Funding_Amount_in_cr:Q", title="Funding Amount (Cr)"),
                    color=alt.value("#FF5733"),
                )
            st.altair_chart(bar_chart, use_container_width=True)
        else:
            st.write("No data available for the selected investor.")
    with y:
        # Group data to create the 'Invester' DataFrame
        Invester = pd.DataFrame(
                df.groupby(['Year', 'Invester_name'])['Funding_Amount_in_cr'].sum()
            ).reset_index()

            # Filter data for the selected investor
        invest = Invester.loc[Invester['Invester_name'] == btn2, ['Year', 'Funding_Amount_in_cr']]

            # Check if there is data to display
        if not invest.empty:
            st.write(f"Funding by Year for {btn2}")

                # Create a bar chart for the funding data
            line_chart = alt.Chart(invest).mark_line().encode(
                    x=alt.X("Year:O", title="Year", sort="-x"),  # Ordinal axis for Year
                    y=alt.Y("Funding_Amount_in_cr:Q", title="Funding Amount (Cr)"),
                    color=alt.value("#FF5733"),  # Static color for the bars
                )
            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.subheader(f"No data available for the selected investor: {btn2}")

