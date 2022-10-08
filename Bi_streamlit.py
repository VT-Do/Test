import pandas as pd
import numpy as np
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

st.set_page_config(page_title="BI-team", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 350px;
        margin-left: -350px;
    }
     
    """,
    unsafe_allow_html=True,
)
# streamlit_app.py





choice = st.sidebar.radio(
    "Select dataset",
    ('WEB','APP','TEST'))

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)


# st. set_page_config(layout="wide")

col1, col2,col3 = st.columns(3)

with col1:
   st.image("images.png", width=80)

with col2:
   st.title("📊 IAB dataset")
with col3:
   st.write('')


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

@st.cache
def load_data1(): 
	query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 10000"
	query_job1 = client.query(query1)
	return client.query(query1).to_dataframe()



@st.cache
def load_data2():
	query2="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 10000"
	query_job2 = client.query(query2)
	return client.query(query2).to_dataframe()
