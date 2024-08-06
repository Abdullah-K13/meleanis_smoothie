# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("My Parents New Healthy Diner :cup_with_straw:")
st.write(
    """Choose the fruits you want to add to your custom Smoothie
    """
)


title = st.text_input("Name on Smoothies:")
st.write("The name on smoothie will be:", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(

    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:

    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
   # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+title+"""')"""
    time_to_insert = st.button('Submit Order')
    
    st.write(my_insert_stmt)
   # st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


