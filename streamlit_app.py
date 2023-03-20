
import streamlit, pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My Parents new Healthy Diner at 207 oak street")


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_Data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_Data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLEroor as e:
  streamlit.error()




my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


my_cur.execute(" select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("Fruit list contains:")
streamlit.text(my_data_row)



streamlit.header("Fruit list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute(" select * from fruit_load_list")
    return my_cur.fetchall()

if  streamlit.button('Get Fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()
  streamlit.dataframe(my_data_row)



def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into FRUIT_LOAD_LIST values(""+new_fruit+"")")
    return "Thanks for adding " + new_fruit   
  
add_my_fruit = streamlit.text_input('What fruit would you like to add','jackfruit')
if  streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snowflake(add_my_fruit)
  streamlit.text (back_from_function)

streamlit.stop()
