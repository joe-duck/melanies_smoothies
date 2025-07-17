# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)



cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()

name_on_order = st.text_input('Name on Smoothie')
st.write('The name of the Smoothie will be: ',name_on_order)
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingrediants', my_dataframe,max_selections=5)

if ingredients_list:
    
    
    ingredients_string = " ".join(ingredients_list)

    # for fruit_chosen in ingredients_list:
    #         ingredients_string += fruit_chosen 
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
    values('""" + ingredients_string + """','"""+name_on_order+"""')
    """
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothe has been ordered!', icon="✅")
smoothiefroot_response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=b3zrMMJ1evTmkmyeJifjqg971D5McVWohHjqIx6p&query=watermelon%20raw&SRFoodCategory=Fruits%20and%20Fruit%20Juices")
# st.text(smoothiefroot_response)
food = smoothiefroot_response.json()
response_json = smoothiefroot_response.json()
sf_df = st.dataframe(data=response_json["foods"][0]["foodNutrients"],use_container_width=True)
# st.json(smoothiefroot_response.json())


# Display the first food item
if "foods" in response_json and len(response_json["foods"]) > 0:
    st.subheader("First Food Item (from USDA API)")
    st.json(response_json["foods"][0]["foodNutrients"])
else:
    st.warning("No foods found in the API response.")
