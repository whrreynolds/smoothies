# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize your smoothie :balloon:")
st.write(
    f"""Choose the fruits you want in your custom smoothie!:

    """
)

#option = st.selectbox(
#    "What is your fav fruit?",
#    ("Banana", "Strawberries", "PeachesSMOOTHIES.PUBLIC"),
#)

#st.write("You selected:", option)


title = st.text_input("Name on Smoothie","")
st.write("The name   order will be: ", title)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose Up to 5 Ingredients:",
    my_dataframe
    ,max_selections= 5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '        
        st.write(ingredients_string)
        st.subheader(fruit_chosen + 'Nut Infro')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_sf = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+title + """')"""
    #st.write(my_insert_stmt)

    time_to_insert = st.button(label="Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


