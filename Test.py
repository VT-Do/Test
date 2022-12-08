import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from io import StringIO
import time
import extra_streamlit_components as stx
import smtplib

st.set_page_config(layout="wide")
container=st.container()




col4, col5,col6 = container.columns((4, 7, 1))
with col4:
    st.image("images.png", width=80)
with col5:
    st.title("📊 IAB dataset")
with col6:
    st.write('')
	
#@st.cache(max_entries=1)
def load_data10(): 
    query11="SELECT * except(Date) FROM `showheroes-bi.bi.bi_adstxt_join_sellersjson_with_count_domains`"
    query_job1 = client.query(query11)
    return client.query(query11).to_dataframe()




