import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from streamlit_option_menu import option_menu
import google.generativeai as genai
import os
from functools import lru_cache
ds = pd.read_csv("Mod_Reviews_data.csv")
Price_review = ds[['PRICE_RATING','Review_result']]

@lru_cache()
def configure_model():
  os.environ['GOOGLE_API_KEY'] = "your api key"
  genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
  model = genai.GenerativeModel('gemini-pro')
  return model

model = configure_model()

# Web App Title
st.markdown('''
# **Reviews Analyser**
---
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

with st.sidebar:
    selected = option_menu(
        menu_title="2. Select a page",
        options = ['Overview','Text analytics','Graphs','Example Review', 'Summarize'],
        default_index=0
    )
if selected == 'Overview':
    st.subheader(" Overview") 
    df = pd.read_csv(uploaded_file)
    pr = ProfileReport(df,dark_mode=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)
    st.write('Upload a file')
if selected == 'Text analytics':
    st.subheader(" Text analytics")
    st.write("### Review Results")
    st.write(ds['Review_result'].value_counts())
    st.write("### Review Result for its price")
    st.write(ds[['PRICE_RATING','Review_result']].value_counts())
    st.write("### Graph of distribution of reviews")
    st.bar_chart(ds['Review_result'].value_counts(),width=50)
    st.write("Negative Reviews :")
    a = ds[ds['Review_result']=='Negative'].index.values
    st.write(ds['REVIEW_CONTENT'][a])
    st.write("Positive Reviews :")
    b = ds[ds['Review_result']=='Positive'].index.values
    st.write(ds['REVIEW_CONTENT'][b])
if selected == 'Graphs':
    st.subheader(" Graphs of the following dataset")
    st.write("### Graph of Price Rating")
    st.bar_chart(ds['PRICE_RATING'].value_counts())
    st.write("### Graph of Value Rating")
    st.bar_chart(ds['VALUE_RATING'].value_counts())
    st.write("### Graph of Quality Rating")
    st.bar_chart(ds['QUALITY_RATING'].value_counts())
    st.write("### Graph of number of product sold to states")
    st.bar_chart(ds['STATES'].value_counts())
    st.write("### Graph of distribution of prices")
    st.bar_chart(ds['PRICE'].value_counts())
if selected == 'Example Review': 
    st.subheader("Analysing the review")
    Review = st.text_input("Enter a review") 
    os.environ['GOOGLE_API_KEY2'] = "your api key"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY2'])
    model = genai.GenerativeModel('gemini-pro')
    if Review:
        response = model.generate_content(' Classify ' + '"' + str(Review) + '"' + ' as positive negative or neutral . Give output only in one word ').text
        st.success(response)
    else:
        st.warning("Please enter the review text")

if selected == 'Summarize': 
  st.subheader("Summarize")
  Review = st.text_area("Enter a review") 

  if Review:
    # Call the summarization function
    prompt = "Summarize the following review: " + Review
    response = model.generate_content(prompt).text
    st.success("**Summary:** " + response)
    
    # Optionally, keep the sentiment classification
    response = model.generate_content(' Classify the given product review into one of neutral, positive or negative. Give answer only in one word:' + str(Review)).text
    st.success("**Sentiment:** " + response)
  else:
    st.warning("Please enter the review text")
