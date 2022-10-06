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



if choice=="WEB":
	query="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 10000"
	query_job = client.query(query)
	df=client.query(query).to_dataframe()
	
	menu_AdversitingSytem=['All']+df['AdvertisingSystem'].unique().tolist()
	choice_AdvertisingSystem=st.sidebar.selectbox("Advertising System", menu_AdversitingSytem)
	
	menu_PubAccId=['All']+df['PubAccId'].unique().tolist()
	choice_PubAccId=st.sidebar.selectbox("Publisher Account ID", menu_PubAccId)
	
	menu_SellerDomain=['All']+df['SellerDomain'].unique().tolist()
	choice1=st.sidebar.selectbox("Seller Domain", menu_SellerDomain)
	
	st.dataframe(df, width=None, height=1000)
elif choice=="APP":
	query="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 10000"
	query_job = client.query(query)
	df=client.query(query).to_dataframe()
	
	menu_AdversitingSytem=['All']+set(df['AdvertisingSystem'].unique().tolist())
	choice_AdvertisingSystem=st.sidebar.selectbox("Advertising System", menu_AdversitingSytem)
	
	menu_PubAccId=['All']+df['PubAccId'].to_list()
	choice_PubAccId=st.sidebar.selectbox("Publisher Account ID", menu_PubAccId)
	
	menu_SellerDomain=['All']+df['SellerDomain'].unique().tolist()
	choice1=st.sidebar.selectbox("Seller Domain", menu_SellerDomain)
	
	df= df[(df['AdvertisingSystem'] == menu_AdversitingSytem) & (df['PubAccId'] == menu_PubAccId ) ]
	
	
	st.dataframe(df, width=None, height=1000)
	st.write('You selected:', menu_AdversitingSytem)
	
else:
	# Store the initial value of widgets in session state
	if "visibility" not in st.session_state:
    		st.session_state.visibility = "visible"
    		st.session_state.disabled = False

	col1, col2 = st.columns(2)

	with col1:
    		st.checkbox("Disable selectbox widget", key="disabled")
    		st.radio("Set selectbox label visibility 👉",key="visibility",options=["visible", "hidden", "collapsed"],)

	with col2:
    		option = st.selectbox("How would you like to be contacted?",("Email", "Home phone", "Mobile phone"),label_visibility=st.session_state.visibility,disabled=st.session_state.disabled,)
