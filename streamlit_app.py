
import streamlit as st
from snowflake.snowpark.functions import col
import requests  

# Connect to Snowflake using Streamlit secrets
cnx = st.connection("snowflake")
session = cnx.session()

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on Smoothie:")

# Retrieve fruit names from Snowflake
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .collect()
)

# Convert Snowpark rows into a Python list
ingredients_list = [row["FRUIT_NAME"] for row in fruit_df]

# Display multiselect
selected_ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    ingredients_list,
    max_selections=5,
    st.subheader(fruit_df + 'Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
)

if st.button("Submit Order"):

    if not name_on_order.strip():
        st.warning("Please enter your name.")

    elif not selected_ingredients:
        st.warning("Please select at least one ingredient.")

    else:
        ingredients_string = " ".join(selected_ingredients)

        # Use parameter binding rather than concatenating user input
        session.sql(
            """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
            """,
            params=[ingredients_string, name_on_order.strip()]
        ).collect()

        st.success(
            f"Hello {name_on_order}! Your smoothie is ordered! 🥤"
        )




