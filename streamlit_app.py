# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("*Choose the fruits you want in your custom smoothie!* :icecream:")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get the fruit options and convert to a format Streamlit understands (Pandas)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# Convert Snowpark DF to Pandas so we can use the column in the multiselect
pd_df = my_dataframe.to_pandas()

# Multiselect widget
ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    pd_df['FRUIT_NAME'], 
    max_selections=5
)

if ingredient_list:
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '

    # Build the Insert Statement
    # We move this inside the IF block so it only creates when ingredients exist
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # Create the Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

# Optional: Fruityvice Nutrition Section (Requires 'requests' library)
# import requests
# if ingredient_list:
#     for fruit in ingredient_list:
#         st.subheader(fruit + ' Nutrition Information')
#         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
#         st.dataframe(data=fruityvice_response.json(), use_container_width=True)
