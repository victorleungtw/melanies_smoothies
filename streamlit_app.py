# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """*Choose the fruits you want in your custom smoothie!*:icecream:
    """
)

Name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:',Name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()

my_df = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_df, use_container_width=True, hide_index= True)

Ingredient_list = st.multiselect('Choose upto 5 ingredients:', my_df, max_selections = 5)

if Ingredient_list:
    ingredients_string = ''
    
    for fruit_chosen in Ingredient_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)

INST_STMT = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+Name_on_order+"""');"""


submit = st.button('Submit Order')

if submit:
    session.sql(INST_STMT).collect()
    st.success('Your Smoothie ordered successfully, '+ Name_on_order+'!', icon = "✅")
#New Section to display fruityvice nutrition information
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
