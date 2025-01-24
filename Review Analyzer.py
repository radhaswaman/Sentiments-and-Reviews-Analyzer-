import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st
import pathlib
import textwrap
import time

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.environ['GOOGLE_API_KEY'] = "your api key"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')
#response = model.generate_content("If I give you reviews would would able to classify them as positive negative or neutral ?").text
#print(response)
ds = pd.read_csv("D:\Python Projects\Data_sets\Mod_Reviews_data.csv",encoding='latin1')
#print(ds.head())
"""a = ds['REVIEW_CONTENT'][0]
print(a)
b = str( ' Classify ' + '"' + str(a) + '"' + ' as positive negative or neutral . Give output only in one word . nan is neutral')
print(b)
response = model.generate_content(b).text
print(response)
ds.loc[0,'Review_result'] = response"""
#print(ds['Review_result'].value_counts())
start = 1545
"""while True:
  try : 
    for i in range(start,5000):
      Reviews = ds['REVIEW_CONTENT'][i]
      b = str( ' Classify ' + '"' + str(Reviews) + '"' + ' as Positive,  Negative or Neutral . Give output only in one word .' )
      response = model.generate_content(b).text
      ds.loc[i,'Review_result'] = response
      print(ds['Review_result'][i],i)
  except:
    print("Error") 
    start=i+1
    continue;
  else :
    break;"""
#ds = ds.to_csv('Data_sets\Mod_Reviews_data.csv',index=False)
a = ds[ds['Review_result']=='Negative'].index.values
print(ds['REVIEW_CONTENT'][a])
