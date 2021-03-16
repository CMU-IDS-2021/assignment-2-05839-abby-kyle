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
DATA_PATH = "assignment-2-05839-abby-kyle/data/"

# -----------------------------------------------------------------------------
# Primary Dataset
# -----------------------------------------------------------------------------

# The relative path to the primary dataset
PRIMARY_DATA_PATH  = DATA_PATH + "data.sav"

# The default height for our visualizations
DEFAULT_WIDTH = 800

# The default height for our visualizations
DEFAULT_HEIGHT = 550

# Colors from Vega color scheme for charts that should not be scaled
COLOR_SCHEME_BLUE = "#90c1dc"

st.set_page_config(layout="wide")

# -----------------------------------------------------------------------------
# Geography-Specific
# -----------------------------------------------------------------------------

RELIGION_DICT = {
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

STATE_DICT = {
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
    "Northeast": [
        "Maine",
        "Massachusetts",
        "Rhode Island",
        "Connecticut",
        "New Hampshire",
        "Vermont",
        "New York", 
        "Pennsylvania",
        "New Jersey",
        "Delaware",
        "Maryland"],
    "Southeast": [
        "West Virginia",
        "Virginia",
        "Kentucky",
        "Tennessee",
        "North Carolina",
        "South Carolina",
        "Georgia",
        "Alabama",
        "Mississippi",
        "Arkansas",
        "Louisiana",
        "Florida"],
    "Midwest": [
        "Ohio", 
        "Indiana", 
        "Michigan", 
        "Illinois", 
        "Missouri", 
        "Wisconsin", 
        "Minnesota", 
        "Iowa", 
        "Kansas",
        "Nebraska", 
        "South Dakota", 
        "North Dakota"],
    "Southwest": [
        "Texas", 
        "Oklahoma", 
        "New Mexico", 
        "Arizona"],
    "West": [
        "Colorado", 
        "Wyoming", 
        "Montana", 
        "Idaho", 
        "Washington", 
        "Oregon", 
        "Utah", 
        "Nevada", 
        "California", 
        "Alaska",
        "Hawaii"]
}

# -----------------------------------------------------------------------------
# Evolution-Specific
# -----------------------------------------------------------------------------

# For the datasets used in the 'evolution' chapter,
# we load a dataset for each question of interest
EVOLUTION_BELIEVE_GOD_PATH = DATA_PATH + "believe_god.csv"
EVOLUTION_BELIEVE_HEAVEN_PATH = DATA_PATH + "believe_heaven.csv"
EVOLUTION_BELIEVE_HELL_PATH = DATA_PATH + "believe_hell.csv"
EVOLUTION_RIGHT_AND_WRONG_PATH = DATA_PATH + "right_and_wrong.csv"
EVOLUTION_SCRIPTURE_PATH = DATA_PATH + "scripture.csv"

# Map the question text to the path to the data for that question
EVOLUTION_QUESTIONS = {
    "Do You Believe in God?": EVOLUTION_BELIEVE_GOD_PATH,
    "Do You Believe in Heaven?": EVOLUTION_BELIEVE_HEAVEN_PATH,
    "Do You Believe in Hell?": EVOLUTION_BELIEVE_HELL_PATH,
    "Where Do You Look for Guidance on Questions of Right and Wrong?": EVOLUTION_RIGHT_AND_WRONG_PATH,
    "The Holy Book for My Religion is...": EVOLUTION_SCRIPTURE_PATH
}

# The full text of the questions
EVOLUTION_FULL_QUESTIONS = {
    "Do You Believe in God?": "Do you believe in God or a universal spirit?",
    "Do You Believe in Heaven?": "Do you think there is a heaven, where people who have led good lives are eternally rewarded?",
    "Do You Believe in Hell?": "Do you think there is a hell, where people who have led bad lives and die without being sorry are eternally punished?",
    "Where Do You Look for Guidance on Questions of Right and Wrong?": "When it comes to questions of right and wrong, which of the following do you look to most for guidance?",
    "The Holy Book for My Religion is...": "Which comes closest to your view: the holy book of my religion is..."
}

# The minimum and maximum ages in the dataset
MIN_AGE = 24
MAX_AGE = 90

# -----------------------------------------------------------------------------
# Future-Specific
# -----------------------------------------------------------------------------

# The relative path to the patterns dataset
FUTURE_DATA_PATH = DATA_PATH + "future.csv"

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

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------

@st.cache 
def load_primary_data():
    return pd.read_spss(PRIMARY_DATA_PATH, convert_categoricals=False)

@st.cache
def load_evolution_data():
    frames = {}
    for question, path in EVOLUTION_QUESTIONS.items():
        frames[question] = pd.read_csv(path)
    return frames

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

    In 2014, the Pew Research Center [conducted a survey](https://www.pewforum.org/2015/05/12/americas-changing-religious-landscape/) in the United States to explore the nature of our beliefs at a greater depth than they had ever attempted before. All of the visualizations that follow are constructed from Pew's [original dataset](https://www.pewforum.org/dataset/pew-research-center-2014-u-s-religious-landscape-study/).

    Religious faith is a vast and complex topic. Our goal in the visualizations below is to distill (some of) the salient aspects of Pew's results into a comprehensible and approachable form. With that said, we must always bear in mind that religious belief, and belief in general, is replete with nuance. The insights we gain from this analysis may help us develop a _broad_ understanding of religious belief - "how do my beliefs compare with my 300 million neighbors", but they will no doubt fall short of providing us with _deep_ insights into the nature of personal belief.

    With that disclaimer out of the way, let's jump in!
    '''

    st.sidebar.header("Digging Deeper")
    st.sidebar.write(
        "We are only grazing the surface with our main graphics, " +
        "but you can keep exploring! Below you will find options " + 
        "for each section that will allow you to explore the data.")

# -----------------------------------------------------------------------------
# Chapter: Geography
# -----------------------------------------------------------------------------

# Prepares the Pandas dataframe for the US overlay chart
def prepare_states(df, religiondict, statedict):
    columnstodrop = [
        21.0, 22.0, 23.0, 24.0, 25.0, 30.0, 31.0, 32.0, 33.0, 34.0,
        35.0, 36.0, 37.0, 38.0, 39.0, 43.0, 44.0, 45.0, 46.0, 50.0,
        51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 59.0, 61.0, 62.0,
        63.0, 64.0, 65.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0,
        77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 88.0,
        90.0, 94.0, 96.0, 994.0, 999.0]
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
        color=alt.Color("Percent Religious:Q", scale=alt.Scale(scheme="redyellowblue", reverse=True))
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
        title= "How Religious are the United States?", 
    )

    uschart = uschart.configure_title(
        fontSize=30,
        font="Times New Roman")
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
    stchart = stchart.configure_title(
        fontSize=30,
        font="Times New Roman")
    return stchart


def render_geography_chapter(df):
    """
    Render the 'geography' chapter.
    """

    '''
    ---
    # The Geography of Belief

    The first aspect of religious belief we will look at is how it is shaped by **geography**. In the United States, despite our claims to "unity", are known for the degree of diversity that exists amongst our 50 constituent states. How does religious belief vary along geographic lines?

    Here we define religious to be an individual that claims to subscribe to a belief system that has some form
    of a or supernatural or higher power. The heat map indicates the percentage by state. You can hover over individual states to see the
    actual values as a percentage as well as the percentage in that state that subscribe to a subset of major religions. For more options, navigate to
    the sidebar under "The Geography of Belief".
    '''
    
    # Set pandas for first visual
    statereligion = prepare_states(df, RELIGION_DICT, STATE_DICT)

    # Render the states visualization
    st.write(render_states_viz(statereligion))

    '''
    The sidebar has a couple of interesting options available for this visualization. You can:

    - Render the raw data from which this graphic was generated
    - Explore the percentages of each state that subscribe to different religions and compare states against each other.
    '''

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
        if stateselect != []:
            st.subheader("Compare States")
            st.write("Here you can visually compare the different religions in each state as well as compare states against each other."
            + " Remeber you can select multiple states at the same time!")
            stateselectchart = stackedtablereligion(stateselect, statereligion)
            st.write(stateselectchart)

# -----------------------------------------------------------------------------
# Chapter: Connection
# -----------------------------------------------------------------------------

def create_belief_df(df):
    columnstodrop = [
        21.0, 22.0, 23.0, 24.0, 25.0, 30.0, 31.0, 32.0, 33.0, 34.0,
        35.0, 36.0, 37.0, 38.0, 39.0, 43.0, 44.0, 45.0, 46.0, 50.0,
        51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 59.0, 61.0, 62.0,
        63.0, 64.0, 65.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0,
        77.0, 78.0, 79.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 88.0,
        90.0, 94.0, 96.0, 994.0, 999.0]
    belief = {
        "qe1":   "Religion",
        "qb1a":  "Immigration",
        "qb1b":  "Women in Workforce",
        "qb1c":  "Children Out of Wedlock",
        "qb2a":  "Homosexuality",
        "qb2b":  "Government Aid",
        "qb2c":  "Environmental Regulations",
        "qb2d":  "Morality",
        "qb20":  "Government Size",
        "qb21":  "Abortion",
        "qb22":  "Gay Marriage",
        "qb30":  "Evolution",
        "qb31":  "Guidance in Life",
        "party": "Political Party"}
    
    imm = {
        1.0: "Positive Change",
        2.0:"Negative Change",
        3.0:"No Change",
        4.0:"Mixed Change",
        9.0:"Unsure"}

    hom = {
        1.0: "Accepted by Society",
        2.0: "Rejected by Society",
        3.0: "Both Equally",
        9.0: "Unsure"}

    govaid = {
        1.0: "More Harm than Good",
        2.0: "More Good than Harm",
        3.0: "Both Equally",
        9.0:"Unsure"}

    envr = {
        1.0: "Hurt the Economy",
        2.0: "Worth the cost",
        3.0: "Both Equally",
        9.0:"Unsure"}

    more = {
        1.0: "Situationally Dependent",
        2.0: "Absolute Standards for Right and Wrong",
        3.0: "Both Equally",
        9.0: "Unsure"}
    govsize = {
        1.0: "Small",
        2.0: "Large",
        3.0: "Depends",
        9.0: "Unsure"}

    ab = {
        1.0: "Legal",
        2.0: "Legal in Most Cases",
        3.0: "Illegal in Most Cases",
        4.0: "Illegal", 
        9.0:"Unsure"}
    gm = {
        1.0: "Strongly favor",
        2.0: "Favor",
        3.0: "Oppose",
        4.0: "Strongly Oppose",
        9.0: "Unsure"}

    evo = {
        1.0: "Agree",
        2.0: "Disagree",
        9.0: "Unsure"}

    gil = {
        1.0: "Religious Teachings",
        2.0: "Philosphy and Reason",
        3.0: "Practical Experience",
        4.0: "Scientific Information",
        9.0: "Unsure"}

    pp = {
        1.0: "Republican",
        2.0: "Democrat",
        3.0: "Independent", 
        4.0: "No Preference",
        5.0: "Other", 
        9.0: "Unsure"}

    #retrieve required columns, rename them, and drop unneeded rows
    beliefdf=df[[
        "qe1",
        "qb1a",
        "qb1b",
        "qb1c",
        "qb2a",
        "qb2b",
        "qb2c",
        "qb2d",
        "qb20",
        "qb21",
        "qb22",
        "qb30",
        "qb31",
        "party"]].copy()
    
    beliefdf = beliefdf.rename(columns=belief)
    for val in columnstodrop:
        beliefdf = beliefdf[beliefdf.Religion != val]
    
    # Update values for easy read
    beliefdf = beliefdf.replace({
        "Immigration" : imm,
        "Women in Workforce" : imm, 
        "Children Out of Wedlock" : imm, 
        "Religion": RELIGION_DICT, 
        "Homosexuality": hom, 
        "Government Aid": govaid,
        "Environmental Regulations": envr,
        "Morality": more,
        "Government Size": govsize, 
        "Abortion": ab,
        "Gay Marriage": gm,
        "Evolution": evo,
        "Guidance in Life": gil,
        "Political Party": pp})
    return beliefdf

def create_belief_compare_chart(bdf, issue, religionlist):
    # Update bdf for specific issue and set of religions
    belief = pd.get_dummies(bdf[issue]).copy()
    belief['Religion'] = bdf['Religion']
    belief = belief.groupby('Religion').sum()
    belief = belief.loc[religionlist, :]
    opinions = list(belief.columns)
    belief = belief.div(belief.sum(axis=1), axis=0) 
    belief = belief.reset_index()
    newbelief = belief.melt(id_vars=['Religion'], value_vars=opinions,
        var_name=issue, value_name='Percent')
    
    #make chart
    result = alt.Chart(newbelief).mark_bar().encode(
            x=alt.X(issue),
            y=alt.Y('Percent', scale=alt.Scale(domain=(0, 1)), axis=alt.Axis(format='%', title='Percentage')),
            color=alt.Color(issue,scale=alt.Scale(scheme="redyellowblue")),
            column='Religion:N',
            tooltip=[alt.Tooltip(issue), alt.Tooltip('Percent:Q', format='.2%')]
        ).properties(
            title=issue
        ).interactive()
    result = result.configure_title(
        fontSize=30,
        font="Times New Roman")
    return result

def render_connection_chapter(df):
    """
    Render the 'connection' chapter.
    """

    '''
    ---
    # How Our Beliefs Shape Us

    Our beliefs do not exist in a vacuum. They both pull and are pulled by other aspects of our identities. The next two chapters will examine how our beliefs relate to one another, and how they change with time.

    Everyone has some form of a belief system that they use to navigate their life. It is absolutly necessary in order to deal with
    the challenge of morality as well as simply 
    
    In this chapter, we explore religious belief and its **connection** with other consequential beliefs that we hold. How does our religious belief relate to our stance on politics? On contentious issues like immigration policy or environmental regulations? On questions of right and wrong? Of course, we all have some intuition for how these questions are related, but are they founded in the data? This chapter allows us to examine precisely this.
    '''  
    
    bdf = create_belief_df(df)

    st.write("Select a belief or issue from the list below. Then, select one or more religions you would like to look at."
    + " You will be able to look at the breakdown of each religion by stance and compare them to other religions.")
    beliefselect = st.radio(
        "Belief or Issue", (
            "Immigration", 
            "Women in Workforce", 
            "Children Out of Wedlock", 
            "Religion", 
            "Homosexuality",
            "Government Aid",
            "Environmental Regulations",
            "Morality",
            "Government Size", 
            "Abortion", 
            "Gay Marriage",
            "Evolution", 
            "Guidance in Life", 
            "Political Party"))

    if beliefselect != "":
        religionselect = st.multiselect("Religion", [
            "Protestant", 
            "Roman Catholic", 
            "Mormon",
            "Orthodox", 
            "Jewish", 
            "Muslim",
            "Buddist", 
            "Hindu",
            "Atheist", 
            "Agnostic",
            "Nothing",
            "Unitarian",
            "Jehovahs Witness",
            "Christian",
            "Unaffiliated"])
        if religionselect != []:
            beliefchart = create_belief_compare_chart(bdf, beliefselect, religionselect)
            st.write(beliefchart)
    
    '''
    The sidebar has a couple of interesting options available for this visualization. You can:

    - Render the raw data from which this graphic was generated. Note the data is presented by individual responder.
    '''

    # Sidebar
    st.sidebar.subheader("How Our Beliefs Shape Us")

    if st.sidebar.checkbox("Show the data for beliefs with respect to religion as a table."):
        st.subheader("Breakdown of Beliefs by Religion")
        st.write("Here you can look at individual respondents who answered a series of questions about the issues shown above. "
        +"Individuals are characterized by their claimed religious beliefs.")
        st.write(bdf.set_index('Religion'))


# -----------------------------------------------------------------------------
# Chapter: Evolution
# -----------------------------------------------------------------------------

def render_evolution_chapter():
    """
    Render the 'evolution' chapter.
    """

    '''
    ---
    # How Our Beliefs Evolve

    In the previous chapter we looked at how our religious beliefs are related to our perspectives on other, disparate topics. In this chapter, we approach the issue from a slightly different angle: how do our religious beliefs **evolve** with us? 

    As we grow older, our view of the world necessarily shifts. We have new experiences, learn new truths, discard falsehoods. How do our religious beliefs fare in this process?

    An important caveat here: the [2014 Pew Research Study](https://www.pewforum.org/2015/05/12/americas-changing-religious-landscape/) from which we collect our source data is not a longitudinal one - it covers a large sample of individuals at a single point in their lives. Therefore, we must note that in the visualization below we use the differing age of the respondents as a _proxy_ for the evolution of beliefs over time. However, bear in mind that the phenomena that we observe may instead be an artifact of _generational forces_ rather than strictly the result of beliefs shifting with age.
    '''

    '''
    To interact with the graphic, select a question of interest from the dropdown list below. Once a question is selected, you can see the distribution of responses to that question for the currently-selected age. Then, you can utilize the slider to change the selected age and observe how the distribution of responses changes.
    '''

    # Sidebar
    st.sidebar.subheader("How Our Beliefs Evolve")
    full_text = st.sidebar.checkbox("Show Full Question Text")
    show_data = st.sidebar.checkbox("Show the Data")

    # Load a map from question -> dataframe
    frames = load_evolution_data()

    # Select box allows users to select question of interest
    option = st.selectbox("Question", options=[k for k in frames.keys()])
    
    # Select the appropriate data to render based on the selection
    df = frames[option]
    df = df.drop(columns=["Unnamed: 0"])

    # Select the appropriate age based on the slider value
    age = st.slider(label="Age", min_value=MIN_AGE, max_value=MAX_AGE)
    tmp = df.loc[df["Age"] == age]
    
    # Reformat the data for plotting
    plot = pd.DataFrame()
    for c in filter(lambda x: x != "Age", tmp.columns):
        plot = plot.append(pd.DataFrame(np.matrix([c, tmp.iloc[0][c]])))    
    plot.columns = ["Response", "Percent"]

    viz = alt.Chart(plot).mark_bar(color=COLOR_SCHEME_BLUE).encode(
        x=alt.X("Response:N"),
        y=alt.Y("Percent:Q", scale=alt.Scale(domain=[0.0, 1.0])),
        tooltip=[alt.Tooltip('Percent:Q', format='.2%')]
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT
    ).properties(
        title=option
    ).interactive()

    viz = viz.configure_title(
        fontSize=30,
        font="Times New Roman")

    if full_text:
        st.write("The full text of the question with which respondents were prompted is:")
        st.write("'" + EVOLUTION_FULL_QUESTIONS[option] + "'")

    st.write(viz)

    '''
    The sidebar has a couple of interesting options available for this visualization. You can:

    - Render the original text of the question posed in the survey
    - Render the raw data from which this graphic was generated
    '''

    if show_data:
        '''
        In the table below you can explore all of the data used to generate the interactive plot above.
        '''
        st.write(df)

# -----------------------------------------------------------------------------
# Chapter: Future
# -----------------------------------------------------------------------------

def count_for_label_at_year(df, label, year):
    tmp = df[df["Religion"].str.contains(label)]
    tmp = tmp[tmp["Year"] == year]
    return tmp.iloc[0]["Count"]

def get_diff_for_label(df, label, metric):
  return int(df[df["Religion"].str.contains(label)][metric])

def preprocess_for_diff_viz(df):
    new = pd.DataFrame()
    for label in FUTURE_COLUMN_HEADERS:
        start = count_for_label_at_year(df, label, 0)
        stop = count_for_label_at_year(df, label, 99)
        diff = stop - start
        prop = int(((stop - start) / start)*100)
        new = new.append(pd.DataFrame(np.matrix([label, diff, prop])))
    new.columns = ["Religion", "Delta", "Prop"]
    return new

# Render the stacked area chart that illustrates growth
def render_future_area_viz(df):
    # Make a selection for interactive legend
    selection = alt.selection_multi(fields=["Religion"], bind="legend")

    # Make the chart
    future = alt.Chart(df).mark_area().encode(
        x="Year:Q",
        y=alt.Y("Count:Q", stack="normalize", axis=alt.Axis(labels=False)),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        color=alt.Color('Religion:N',scale=alt.Scale(scheme="redyellowblue")),
        tooltip=["Religion:N", "Count:Q"],
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT
    ).add_selection(
        selection
    ).properties(
        title="The Change in Religious Landscape Overtime"
    )
    future = future.configure_title(
        fontSize=30,
        font="Times New Roman")

    st.write(future)

# Render the bar chart that illustrates gain / loss for each religion
def render_future_diff_viz(df):
    # Do some preprocessing
    pre = preprocess_for_diff_viz(df)

    absolute_diff = st.sidebar.checkbox("Show Absolute Differences")
    
    order = [label for label in pre["Religion"]]

    column_label = "Delta" if absolute_diff else "Prop"
    if absolute_diff:
        order = sorted(order, key=lambda x: get_diff_for_label(pre, x, "Delta"))
        charttitle = "Religious Adherance Gains and Loses: Absolute"
    else:
        order = sorted(order, key=lambda x: get_diff_for_label(pre, x, "Prop"))
        charttitle = "Religious Adherance Gains and Loses: Percentage"

    # Render the chart
    chart = alt.Chart(pre).mark_bar().encode(
        x=alt.X("Religion:N", sort=order),
        y=alt.Y(column_label+":Q"),
        tooltip=[column_label],
        color=alt.condition(
            alt.datum.Delta > 0,
            alt.value(COLOR_SCHEME_BLUE) , # The positive color
            alt.value("red"))    # The negative color
    ).properties(
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT
    ).interactive(
    ).properties(
        title=charttitle
    )
    chart = chart.configure_title(
        fontSize=30,
        font="Times New Roman")

    if absolute_diff:
        '''
        With 'Absolute Differences' selected, the chart below shows the total gain loss for number of religious adherents in each faith.
        '''
    else:
        '''
        In this default view, the chart below shows the gain and loss for each belief system, as a percentage relative to the current number of adherenets.
        '''

    st.write(chart)

def render_future_chapter():
    """
    Render the 'future' chapter.
    """

    '''
    ---
    # The Shape of Our Future Beliefs 

    In our final chapter, we examine what the future of religious belief in the United States might look like.
    '''

    df = load_future_data()
    df = df.drop(columns=["Unnamed: 0"])

    st.sidebar.subheader("The Shape of our Future Beliefs")

    render_future_area_viz(df)

    '''
    While the visualization above concisely encodes the data on this particular question, it is somewhat difficult to determine the degree of the gain and loss for individual religious beliefs. The graphic below depicts both the relative and absolute gain and loss for each belief system, ordered from greatest loss to greatest gain.
    '''

    render_future_diff_viz(df)

    show_data = st.sidebar.checkbox("Show Data")

    if show_data:
        '''
        In the table below you can explore all of the data used to generate the interactive plot above.
        '''
        st.write(df)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    # Load the datasets
    df_primary = load_primary_data()
    
    render_introduction_content()

    # Chapter 1: Geography
    render_geography_chapter(df_primary)

    # Chapter 2: Connection
    render_connection_chapter(df_primary)

    # Chapter 3: Evolution
    render_evolution_chapter()

    # Chapter 4: Future
    render_future_chapter()

# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
