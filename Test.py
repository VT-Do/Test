import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO
import streamlit_authenticator as stauth
import yaml
import time
import extra_streamlit_components as stx
import smtplib


st.set_page_config(layout="wide")
container=st.container()

domainname = st.sidebar.text_input('Put a domain here', '')
st.sidebar.write('The current domain', domainname)

col4, col5,col6 = container.columns((4, 7, 1))

with col4:
    st.image("images.png", width=80)
with col5:
    st.title("📊 IAB dataset")
with col6:
    st.write('')

    
    
query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains`
WHERE PubAccId ='1356'"
df= client.query(query1).to_dataframe().fillna('-')

st.write('Result')
st.write(df)
