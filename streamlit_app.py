
import streamlit, pandas
streamlit.title("My Parents new Healthy Diner at 207 oak street")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
