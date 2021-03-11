import pandas as pd
import altair as alt
import streamlit as st

# Data Source:
# https://www.pewforum.org/2015/05/12/americas-changing-religious-landscape/

DATA_URL = "https://raw.githubusercontent.com/CMU-IDS-2021/assignment-2-05839-abby-kyle/blob/3e8788299556fb818fab1c48d26e72badc5612c4/data/data.sav"

st.title("Let's analyze some religion data.")

# add caching so we load the data only once
@st.cache  
def load_data():
    path = "data/data.sav"
    return pd.read_spss(path)

def main():
    df = load_data()
    st.write(df)

if __name__ == "__main__":
    main()