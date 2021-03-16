# evolution.py 
#
# Preprocessing for the 'evolution' chapter.

import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# General Constants
# -----------------------------------------------------------------------------

# The relative path to the data directory
DATA_PATH = "data/"

# The location of the data 
DATA_FILE = DATA_PATH + "data.sav"

# The minimum and maximum age in the dataset
MIN_AGE = 24
MAX_AGE = 90

# Maps input df label -> age
AGE_MAP = {
    8.0:  55, 
    9.0:  60,
    1.0:  24,
    7.0:  50, 
    10.0: 65,
    6.0:  45, 
    11.0: 70,
    3.0:  30,
    5.0:  40,
    2.0:  25,
    4.0:  35,
    12.0: 75,
    13.0: 80,
    14.0: 85,
    15.0: 90
}

# The key that identifies 'age' in the input dataset
AGE_KEY = "agerec"

# -----------------------------------------------------------------------------
# Believe in God
# -----------------------------------------------------------------------------

# The output filename for the processed data
BELIEVE_IN_GOD_FILENAME = "believe_god.csv"

# The identifier for the question in the input dataframe
BELIEVE_IN_GOD_Q = "qg1"

# Map response label -> response text
BELIEVE_IN_GOD_RESPONSE_MAP = {
    1.0: "Yes",
    2.0: "No",
    9.0: "Don't Know",
    3.0: "Other"
}

# -----------------------------------------------------------------------------
# Believe in Heaven
# -----------------------------------------------------------------------------

# The output filename for the processed data
BELIEVE_IN_HEAVEN_FILENAME = "believe_heaven.csv"

# The identifier for the question in the input dataframe
BELIEVE_IN_HEAVEN_Q = "qg5"

# Map response label -> response text
BELIEVE_IN_HEAVEN_RESPONSE_MAP = {
    1.0: "Yes",
    2.0: "No",
    9.0: "Don't Know",
    3.0: "Other"
}

# -----------------------------------------------------------------------------
# Believe in Hell
# -----------------------------------------------------------------------------

# The output filename for the processed data
BELIEVE_IN_HELL_FILENAME = "believe_hell.csv"

# The identifier for the question in the input dataframe
BELIEVE_IN_HELL_Q = "qg6"

# Map response label -> response text
BELIEVE_IN_HELL_RESPONSE_MAP = {
    1.0: "Yes",
    2.0: "No",
    9.0: "Don't Know",
    3.0: "Other"
}

# -----------------------------------------------------------------------------
# Right and Wrong
# -----------------------------------------------------------------------------

# The output filename for the processed data
RIGHT_AND_WRONG_FILENAME = "right_and_wrong.csv"

# The identifier for the question in the input dataframe
RIGHT_AND_WRONG_Q = "qb31"

# Map response label -> response text
RIGHT_AND_WRONG_RESPONSE_MAP = {
    1.0: "Religious Teaching / Beliefs",
    2.0: "Philosophy and Reason",
    3.0: "Practical Experience / Common Sense",
    4.0: "Scientific Information",
    9.0: "Don't Know"
}

# -----------------------------------------------------------------------------
# Scripture
# -----------------------------------------------------------------------------

# The output filename for the processed data
SCRIPTURE_FILENAME = "scripture.csv"

# The identifier for the question in the input dataframe
SCRIPTURE_Q = "qg7"

# Map response label -> response text
SCRIPTURE_RESPONSE_MAP = {
    1.0: "The Word of God",
    2.0: "The Work of Men",
    3.0: "Other",
    9.0: "Don't Know"
}

# -----------------------------------------------------------------------------
# Generic Processor
# -----------------------------------------------------------------------------

def get_lower_bound(df, age):
  while age not in df["Age"].values:
    age = age - 1
  return age

def get_upper_bound(df, age):
  while age not in df["Age"].values:
    age = age + 1
  return age

def processor(df, question, response_map):
    """
    :param df The input dataframe
    :param question The original question number label
    that identifies the question in the input dataframe
    :param response_map The dictionary that maps the 
    response labels in input dataframe to readable labels
    """

    # Prepare the dataframe with known values
    prep = pd.DataFrame()
    for age_key in AGE_MAP.keys():
        # Isolate the age we care about
        tmp = df[df[AGE_KEY] == age_key]

        # Compute the proportions for that age
        props = [AGE_MAP[age_key]]
        for response_key in response_map:
            prop = len(tmp[tmp[question] == response_key]) / len(tmp)
            props.append(prop)

        prep = prep.append(pd.DataFrame(np.matrix(props)))

    # Setup the columns for the processed dataframe
    columns = ["Age"]
    columns.extend(response_map.values())
    prep.columns = columns

    # Now, perform interpolation
    for age in range(MIN_AGE, MAX_AGE):
        if age not in prep["Age"].values:
            lower_bound_x = get_lower_bound(prep, age)
            upper_bound_x = get_upper_bound(prep, age)

            columns = [age]
            for response in filter(lambda x: x != "Age", prep.columns):
                lower_bound_y = prep[prep["Age"] == lower_bound_x].iloc[0][response]
                upper_bound_y = prep[prep["Age"] == upper_bound_x].iloc[0][response]

                # Perform the interpolation
                interpolated = np.interp(age, [lower_bound_x, upper_bound_x], [lower_bound_y, upper_bound_y])
                columns.append(interpolated)
            
            tmp = pd.DataFrame(np.matrix(columns))
            tmp.columns = prep.columns
            prep = prep.append(tmp)
    
    # Sort the values
    prep["Age"] = prep["Age"].astype(int)
    prep.sort_values(by="Age", inplace=True)

    # Return the prepared dataframe
    return prep

# -----------------------------------------------------------------------------
# Believe in God
# -----------------------------------------------------------------------------

def process_believe_god(df):
    print("[+] Processing 'believe in god'...")
    prepped = processor(df, BELIEVE_IN_GOD_Q, BELIEVE_IN_GOD_RESPONSE_MAP)
    prepped.to_csv(DATA_PATH + BELIEVE_IN_GOD_FILENAME)
    print("[+] Done!")

# -----------------------------------------------------------------------------
# Believe in Heaven
# -----------------------------------------------------------------------------

def process_believe_heaven(df):
    print("[+] Processing 'believe in heaven'...")
    prepped = processor(df, BELIEVE_IN_HEAVEN_Q, BELIEVE_IN_HEAVEN_RESPONSE_MAP)
    prepped.to_csv(DATA_PATH + BELIEVE_IN_HEAVEN_FILENAME)
    print("[+] Done!")

# -----------------------------------------------------------------------------
# Believe in Hell
# -----------------------------------------------------------------------------

def process_believe_hell(df):
    print("[+] Processing 'believe in hell'...")
    prepped = processor(df, BELIEVE_IN_HELL_Q, BELIEVE_IN_HELL_RESPONSE_MAP)
    prepped.to_csv(DATA_PATH + BELIEVE_IN_HELL_FILENAME)
    print("[+] Done!")

# -----------------------------------------------------------------------------
# Right and Wrong
# -----------------------------------------------------------------------------

def process_right_and_wrong(df):
    print("[+] Processing 'right and wrong'...")
    prepped = processor(df, RIGHT_AND_WRONG_Q, RIGHT_AND_WRONG_RESPONSE_MAP)
    prepped.to_csv(DATA_PATH + RIGHT_AND_WRONG_FILENAME)
    print("[+] Done!")

# -----------------------------------------------------------------------------
# Scripture
# -----------------------------------------------------------------------------

def process_right_and_wrong(df):
    print("[+] Processing 'scripture'...")
    prepped = processor(df, SCRIPTURE_Q, SCRIPTURE_RESPONSE_MAP)
    prepped.to_csv(DATA_PATH + SCRIPTURE_FILENAME)
    print("[+] Done!")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    df = pd.read_spss(DATA_FILE, convert_categoricals=False)
    process_believe_god(df)
    process_believe_heaven(df)
    process_believe_hell(df)
    process_right_and_wrong(df)

# -----------------------------------------------------------------------------
# Script Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
