# streamlist_app.py
# Streamlit application.
#
# Abby Vorhaus, Kyle Dotterrer

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

# The relative path to the directory in which data is stored
DATA_PATH = "data/"

# The relative path to the primary dataset
PRIMARY_DATA_PATH  = DATA_PATH + "data.sav"
# The relative path to the patterns dataset
FUTURE_DATA_PATH = DATA_PATH + "future.csv"

# The default height for our visualizations
DEFAULT_WIDTH = 800
# The default height for our visualizations
DEFAULT_HEIGHT = 550

# The df column headers for patterns dataset
FUTURE_COLUMN_HEADERS = [
    "Buddhist", 
    "Catholic", 
    "Evangel Prot", 
    "Hindu", 
    "Hist Black Prot", 
    "Jehovahs Witness", 
    "Jewish", 
    "Mainline Prot", 
    "Mormon", 
    "Muslim", 
    "Orthodox Christian", 
    "Unaffiliated"]

# The df column headers after we transform
FUTURE_TRANSFORMED_COLUMN_HEADERS = [
    "Year",
    "Religion",
    "Proportion"]

religiondict = {
    1.0: "Protestant",
    2.0: "Roman Catholic",
    3.0: "Mormon",
    4.0: "Orthodox",
    5.0: "Jewish",
    6.0: "Muslim",
    7.0: "Buddist",
    8.0: "Hindu",
    9.0: "Atheist",
    10.0: "Agnostic",
    12.0: "Nothing",
    13.0: "Christian", 
    14.0: "Unitarian",
    15.0: "Jehovah's Witness",
    99.0: "Unaffiliated"
}

statedict = {
    1.0: "Alabama",
    2.0: "Alaska",
    4.0: "Arizona",
    5.0: "Arkansas",
    6.0: "California",
    8.0: "Colorado",
    9.0: "Connecticut",
    10.0: "Delaware",
    11.0: "District of Columbia",
    12.0: "Florida",
    13.0: "Georgia",
    15.0: "Hawaii",
    16.0: "Idaho",
    17.0: "Illinois",
    18.0: "Indiana",
    19.0: "Iowa",
    20.0: "Kansas",
    21.0: "Kentucky",
    22.0: "Louisiana",
    23.0: "Maine",
    24.0: "Maryland",
    25.0: "Massachusetts",
    26.0: "Michigan",
    27.0: "Minnesota",
    28.0: "Mississippi",
    29.0: "Missouri",
    30.0: "Montana",
    31.0: "Nebraska",
    32.0: "Nevada",
    33.0: "New Hampshire",
    34.0: "New Jersey",
    35.0: "New Mexico",
    36.0: "New York",
    37.0: "North Carolina",
    38.0: "North Dakota",
    39.0: "Ohio",
    40.0: "Oklahoma",
    41.0: "Oregon",
    42.0: "Pennsylvania",
    44.0: "Rhode Island",
    45.0: "South Carolina",
    46.0: "South Dakota",
    47.0: "Tennessee",
    48.0: "Texas",
    49.0: "Utah",
    50.0: "Vermont",
    51.0: "Virginia",
    53.0: "Washington",
    54.0: "West Virginia",
    55.0: "Wisconsin",
    56.0: "Wyoming"
}

regiondict = {
    'Northeast': ["Maine", "Massachusetts", "Rhode Island", "Connecticut", "New Hampshire", "Vermont", "New York", 
    "Pennsylvania", "New Jersey", "Delaware", "Maryland"],
    'Southeast': ["West Virginia", "Virginia", "Kentucky", "Tennessee", "North Carolina", "South Carolina", "Georgia",
    "Alabama", "Mississippi", "Arkansas", "Louisiana", "Florida"],
    'Midwest': ["Ohio", "Indiana", "Michigan", "Illinois", "Missouri", "Wisconsin", "Minnesota", "Iowa", "Kansas",
    "Nebraska", "South Dakota", "North Dakota"],
    'Southwest': ["Texas", "Oklahoma", "New Mexico", "Arizona"],
    'West': ["Colorado", "Wyoming", "Montana", "Idaho", "Washington", "Oregon", "Utah", "Nevada", "California", "Alaska",
    "Hawaii"]
}

st.set_page_config(layout="wide")

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------

 # Add caching so we load the data only once
@st.cache 
def load_primary_data():
    return pd.read_spss(PRIMARY_DATA_PATH, convert_categoricals=False)

@st.cache
def load_future_data():
    # Read the original data
    return pd.read_csv(FUTURE_DATA_PATH)

# -----------------------------------------------------------------------------
# Top-Level
# -----------------------------------------------------------------------------

def render_introduction_content():
    """
    Render the introductory content.
    """

    '''
    # The Shape of Belief

    ### Beliefs are one of the most important things in human life. They determine _the way we think_; _how we act_; _who we are_. 

    In the history of human endeavor, few belief systems have exerted a greater impact on our collective consciousness than religious faith. Many of our traditions date back millennia and have evolved symbiotically with us through the years, simultaneously shaping and being shaped by our collective will. 
    '''
    st.sidebar.header("Digging Deeper")
    st.sidebar.write("We are only grazing the surface with our main graphics, but you can keep exploring! Below you will find options for each section that will allow you to explore the data.")

# -----------------------------------------------------------------------------
# Chapter: Geography
# -----------------------------------------------------------------------------

# Prepares the Pandas dataframe for the US overlay chart
def prepare_states(df, religiondict, statedict):
    columnstodrop = [21.0, 22.0, 23.0, 24.0, 25.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0,
                 43.0, 44.0, 45.0,46.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,59.0,61.0,62.0,63.0,64.0,65.0,
                 70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,81.0,82.0,83.0,84.0,85.0,86.0,88.0,90.0,94.0,
                 96.0, 994.0,999.0]
    statesbase=df[["qe1"]].copy()
    statebase = df[["state"]].copy()
    
    # Make Dummy variables so groupby works, format as needed
    statesbase = pd.get_dummies(statesbase.qe1)
    statesbase = statesbase.drop(columns = columnstodrop)
    statesbase = statesbase.rename(columns = religiondict)
    statesbase["State"] = statebase
    statesbase = statesbase.groupby("State").sum()

    # Percent breakdown by religions
    statesvreligion = statesbase.div(statesbase.sum(axis=1), axis=0) 
    
    # Percentage of population religious in some capacity
    statesreligious = statesvreligion.drop(columns = ["Atheist", "Nothing", "Unaffiliated"]).sum(axis=1)
    statesvreligion["Percent Religious"] = statesreligious
    
    # Get state names but keep ids
    statesvreligion = statesvreligion.reset_index()
    statesvreligion["id"] = statesvreligion["State"]
    statesvreligion = statesvreligion.set_index("State")
    statesvreligion = statesvreligion.rename(index = statedict)
    statesvreligion = statesvreligion.reset_index()
    return statesvreligion

# Build a heat map based on how religious each state in the US is
def render_states_viz(statesvreligion):
    states = alt.topo_feature(data.us_10m.url, "states")
    uschart = alt.Chart(states).mark_geoshape().encode(
        tooltip=["State:N", 
            alt.Tooltip("Percent Religious:Q", format=".2%"), 
            alt.Tooltip("Protestant:Q", format=".2%"),
            alt.Tooltip("Roman Catholic:Q", format=".2%"),
            alt.Tooltip("Orthodox:Q", format=".2%"),
            alt.Tooltip("Muslim:Q", format=".2%"),
            alt.Tooltip("Hindu:Q", format=".2%"),
            alt.Tooltip("Buddist:Q", format=".2%"),
            alt.Tooltip("Jewish:Q", format=".2%"),
            alt.Tooltip("Mormon:Q", format=".2%"),
            alt.Tooltip("Agnostic:Q", format=".2%"),
            alt.Tooltip("Atheist:Q", format=".2%")],
        color=alt.Color("Percent Religious:Q", scale=alt.Scale(scheme="inferno", reverse=True))
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(
            statesvreligion, 
            "id", 
            [
                "Percent Religious",
                "State",
                "Protestant",
                "Roman Catholic",
                "Mormon",
                "Orthodox",
                "Jewish",
                "Muslim", 
                "Buddist", 
                "Hindu", 
                "Atheist", 
                "Agnostic"
            ]),
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
    ).project(
        type="albersUsa"
    ).properties(
        title= {
            "text": ["How Religious are the United States?"], 
            "subtitle": ["A breakdown of how religious each state is and what religions they subscribe to. All values are percentages"],
        }
    )

    uschart = uschart.configure_title(fontSize=30)
    return uschart

def stackedtablereligion(selectlist, df):
    stackedbars = df.drop(columns = ["Percent Religious", "id"]).set_index("State")
    colnames = list(stackedbars.columns)
    #set up data
    data = stackedbars.loc[selectlist, :]
    data = data.reset_index()
    data = data.melt(id_vars=['State'], value_vars=colnames,
            var_name='Religion', value_name='Percent')
    #Make the stacked bar chart
    stchart = alt.Chart(data).mark_bar().encode(
            x=alt.X('sum(Percent)', scale=alt.Scale(domain=(0, 1)), axis=alt.Axis(format='%', title='Percentage')),
            y='State',
            color=alt.Color('Religion:N',scale=alt.Scale(scheme="redyellowblue")),
            tooltip=['State:N', 'Religion:N', alt.Tooltip('Percent:Q', format='.2%')],
        ).properties(
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
        ).properties(
            title="Religions by State"
        ).interactive()
    return stchart


def render_geography_chapter(df):
    """
    Render the 'geography' chapter.
    """

    '''
    ---
    # The Geography of Belief

    Let's first look at how religious states are. Here we define religious to be an individual that claims to subscribe to a belief system that has some form
    of a or supernatural or higher power. The heat map indicates the percentage by state. You can hover over individual states to see the
    actual values as a percentage as well as the percentage in that state that subscribe to a subset of major religions. For more options, navigate to
    the sidebar under "The Geography of Belief".
    '''
    
    # Set pandas for first visual
    statereligion = prepare_states(df, religiondict, statedict)

    # Render the states visualization
    st.write(render_states_viz(statereligion))

    #-------------------------------------------------------------------
    # Sidebar
    #-------------------------------------------------------------------
    st.sidebar.subheader("The Geography of Belief")

    # Selectively render the data for the states visualization
    if st.sidebar.checkbox("Show the religious data for each state as a table"):
        st.subheader( "Breakdown of States and their Religious Make-up")
        st.write("By clicking on the column titles, you can "
        + "discover which religions are most prominent in " 
        + "different states and find states and regions that "
        + "have larger populations of certain sects. For "
        + "example, if you click on 'Mormon' you will find that"
        + " Utah and the surrounding states have the highest "
        + "percent of Mormons with respect to the other "
        + "religions. All values are percentages.")
        statedf = statereligion.drop(
            columns = ["Percent Religious", "id"]).set_index("State").apply(lambda x: x*100)
        st.write(statedf)

    if st.sidebar.checkbox("Compare States"):
        st.sidebar.write("Compare the religious breakdowns for each state. You can select multiple options.")
        stateselect = st.sidebar.multiselect("State", statereligion, key='State')
        #regionselect = st.sidebar.multiselect("Region", ["Midwest", "Northeast", "Southeast", "Southwest", "West"])
        if stateselect != []:
            st.subheader("Compare States")
            st.write("Here you can visually compare the different religions in each state as well as compare states against each other."
            + " Remeber you can select multiple states at the same time!")
            stateselectchart = stackedtablereligion(stateselect, statereligion)
            st.write(stateselectchart)
        #if regionselect != []:
        #    st.subheader("Compare Regions")
        #    st.write("Here you can visually compare the different religions in each regions as well as compare regions against each other."
        #    + "Remeber you can select multiple states at the same time!")
        #    regionselectchart = stackedtablereligion(regionselect, statereligion, True)
        #    st.write(regionselectchart)

# -----------------------------------------------------------------------------
# Chapter: Connection
# -----------------------------------------------------------------------------

def render_connection_chapter(df):
    """
    Render the 'connection' chapter.
    """

    '''
    ---
    # How Our Beliefs Shape Us
    '''
    # Sidebar
    st.sidebar.subheader("How Our Beliefs Shape Us")

# -----------------------------------------------------------------------------
# Chapter: Evolution
# -----------------------------------------------------------------------------

def render_evolution_chapter(df):
    """
    Render the 'evolution' chapter.
    """

    '''
    ---
    # How Our Beliefs Evolve With Us
    '''

    df1 = pd.DataFrame(np.matrix([1, 2]))
    df2 = pd.DataFrame(np.matrix([3, 4]))

    option = st.selectbox("Label", options=["Foo", "Bar"])

    if option == "Foo":
        st.write(df1)
    else:
        st.write(df2)

# -----------------------------------------------------------------------------
# Chapter: Future
# -----------------------------------------------------------------------------

def count_for_label_at_year(df, label, year):
    tmp = df[df["Religion"].str.contains(label)]
    tmp = tmp[tmp["Year"] == year]
    return tmp.iloc[0]["Count"]

def get_diff_for_label(df, label):
  return int(df[df["Religion"].str.contains(label)]["Delta"])

def preprocess_for_diff_viz(df):
    new = pd.DataFrame()
    for label in FUTURE_COLUMN_HEADERS:
        start = count_for_label_at_year(df, label, 0)
        stop = count_for_label_at_year(df, label, 99)
        diff = stop - start
        new = new.append(pd.DataFrame(np.matrix([label, diff])))
    new.columns = ["Religion", "Delta"]
    return new

# Render the stacked area chart that illustrates growth
def render_future_area_viz(df):
    # Make a selection for interactive legend
    selection = alt.selection_multi(fields=["Religion"], bind="legend")

    # Make the chart
    future = alt.Chart(df).mark_area().encode(
        x="Year:T",
        y=alt.Y("Count:Q", stack="normalize"),
        color="Religion:N",
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT
    ).add_selection(
        selection
    )

    return future

# Render the bar chart that illustrates gain / loss for each religion
def render_future_diff_viz(df):
    # Do some preprocessing
    pre = preprocess_for_diff_viz(df)

    order = [label for label in pre["Religion"]]
    order = sorted(order, key=lambda x: get_diff_for_label(pre, x))

    # Render the chart
    chart = alt.Chart(pre).mark_bar().encode(
        x=alt.X("Religion:N", sort=order),
        y="Delta:Q",
        color=alt.condition(
            alt.datum.Delta > 0,
            alt.value("green") , # The positive color
            alt.value("red"))    # The negative color
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT
    )

    return chart

def render_future_chapter(df):
    """
    Render the 'future' chapter.
    """

    '''
    ---
    # The Shape of Our Future Beliefs 

    Narrative
    '''

    st.write(render_future_area_viz(df))
    st.write(render_future_diff_viz(df))
    st.write(df)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    # Load the datasets
    df_primary = load_primary_data()
    df_future = load_future_data()
    
    render_introduction_content()

    # Chapter 1: Geography
    render_geography_chapter(df_primary)

    # Chapter 2: Connection
    render_connection_chapter(df_primary)

    # Chapter 3: Evolution
    render_evolution_chapter(df_primary)

    # Chapter 4: Future
    render_future_chapter(df_future)

# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
