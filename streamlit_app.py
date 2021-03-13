import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

religiondict = {1.0 : "Protestant", 2.0 : "Roman Catholic", 3.0 : "Mormon", 4.0:"Orthodox", 5.0:"Jewish", 6.0:"Muslim", 7.0:"Buddist",
                8.0:"Hindu", 9.0:"Atheist", 10.0:"Agnostic", 12.0:"Nothing", 13.0:"Christian", 
                14.0:"Unitarian", 15.0:"Jehovah's Witness", 99.0:"Don't Know"}
statedict = {1.0:'Alabama',2.0:'Alaska',4.0:'Arizona',5.0:'Arkansas',6.0:'California',8.0:'Colorado',9.0:'Connecticut',
             10.0: 'Delaware',11.0:'District of Columbia', 12.0:'Florida',13.0:'Georgia',15.0:'Hawaii',16.0:'Idaho',17.0:'Illinois',18.0:'Indiana',
             19.0:'Iowa',20.0:'Kansas',21.0:'Kentucky',22.0:'Louisiana',23.0:'Maine',24.0:'Maryland',25.0:'Massachusetts',
             26.0:'Michigan',27.0:'Minnesota',28.0:'Mississippi',29.0:'Missouri',30.0:'Montana',31.0:'Nebraska',32.0:'Nevada',
             33.0:'New Hampshire',34.0:'New Jersey',35.0:'New Mexico',36.0:'New York',37.0:'North Carolina',
             38.0:'North Dakota',39.0:'Ohio',40.0:'Oklahoma',41.0:'Oregon',42.0:'Pennsylvania',44.0:'Rhode Island',
             45.0:'South Carolina',46.0:'South Dakota',47.0:'Tennessee',48.0:'Texas',49.0:'Utah',50.0:'Vermont',
            51.0:'Virginia',53.0:'Washington',54.0:'West Virginia',55.0:'Wisconsin',56.0:'Wyoming'}

@st.cache  # add caching so we load the data only once
def load_data():
    religion_data = "data/data.sav"
    return pd.read_spss(religion_data)

#Preps the Pandas dataframe for the US overlay chart
def getStatesVReligion(df, religiondict, statedict):
    columnstodrop = [21.0, 22.0, 23.0, 24.0, 25.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0,
                 43.0, 44.0, 45.0,46.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,59.0,61.0,62.0,63.0,64.0,65.0,
                 70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,81.0,82.0,83.0,84.0,85.0,86.0,88.0,90.0,94.0,
                 96.0, 994.0,999.0]
    statesbase=df[['qe1']].copy()
    statebase = df[['state']].copy()
    #Make Dummy variables so groupby works, format as needed
    statesbase = pd.get_dummies(statesbase.qe1)
    statesbase = statesbase.drop(columns = columnstodrop)
    statesbase = statesbase.rename(columns = religiondict)
    statesbase["State"] = statebase
    statesbase = statesbase.groupby("State").sum()
    #percent breakdown by religions
    statesvreligion = statesbase.div(statesbase.sum(axis=1), axis=0) 
    #percentage of population religious in some capacity
    statesreligious = statesvreligion.drop(columns = ['Atheist', 'Nothing', "Don't Know"]).sum(axis=1)
    statesvreligion["Percent Religious"] = statesreligious
    #Get state names but keep ids
    statesvreligion = statesvreligion.reset_index()
    statesvreligion['id'] = statesvreligion['State']
    statesvreligion = statesvreligion.set_index('State')
    statesvreligion = statesvreligion.rename(index = statedict)
    statesvreligion = statesvreligion.reset_index()
    return statesvreligion

#Build a heat map based on how religious each state in the US is
def usReligionChart(statesvreligion, states):
    uschart = alt.Chart(states).mark_geoshape().encode(
        tooltip=['State:N', alt.Tooltip('Percent Religious:Q', format='.2%'), alt.Tooltip('Protestant:Q', format='.2%'),
            alt.Tooltip('Roman Catholic:Q', format='.2%'), alt.Tooltip('Orthodox:Q', format='.2%'),
            alt.Tooltip('Muslim:Q', format='.2%'), alt.Tooltip('Hindu:Q', format='.2%'),
            alt.Tooltip('Buddist:Q', format='.2%'), alt.Tooltip('Jewish:Q', format='.2%'),
            alt.Tooltip('Mormon:Q', format='.2%'), alt.Tooltip('Agnostic:Q', format='.2%'),
            alt.Tooltip('Atheist:Q', format='.2%')],
        color=alt.Color('Percent Religious:Q', scale=alt.Scale(scheme="inferno", reverse=True))
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(statesvreligion, 'id', ['Percent Religious', 'State', 'Protestant', 'Roman Catholic', 'Mormon',
                                                'Orthodox', 'Jewish', 'Muslim', 'Buddist', 'Hindu', 'Atheist', 'Agnostic']),
    ).properties(
        width=650,
        height=400,
    ).project(
        type='albersUsa'
    ).properties(
        title= {"text": ["How Religious is the United States?"], 
        "subtitle": ["A breakdown of how religious states and what religions they subscribe to. All values are percentages."],
           }
    )

    uschart.configure_title(
        fontSize=25,
        font='Times New Roman',
    )
    return uschart


#Build the visualizations
#load data
df = load_data()
#Set pandas for first visual
statereligion = getStatesVReligion(df, religiondict, statedict)
#Create the religion heat map
states = alt.topo_feature(data.us_10m.url, 'states')
uschart = usReligionChart(statereligion, states)

#Create the Web App
st.title("US Religious Beliefs 2014")
st.write("Let's first look at how religious states are. This was determined by taking the data" +
    "from a 2014 Religious Landscape study conducted by Pew Research Center.")
st.write(uschart)
# st.write(df)



# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)
