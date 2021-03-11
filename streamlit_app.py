import streamlit as st
import pandas as pd
import altair as alt

st.title("US Religious Beliefs 2014")

@st.cache  # add caching so we load the data only once
def load_data():
    religion_data = "data/data.sav"
    return pd.read_spss(religion_data)

df = load_data()

st.write("Let's look at raw data in the Pandas Data Frame.")

# st.write(df)

st.write("length is: {}".format(len(df)))

# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)
