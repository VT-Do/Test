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


# menu2=["A", "B"]
# choice2=st.sidebar.selectbox("Choose dataset", menu2)


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


query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 10000"
query_job1 = client.query(query1)
df1=client.query(query1).to_dataframe()


query2="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 10000"
query_job2 = client.query(query2)
df2=client.query(query2).to_dataframe()
	


if choice=="WEB":
	
	
	
	menu_AdversitingSytem=['All']+df1['AdvertisingSystem'].unique().tolist()
	choice_AdvertisingSystem=st.sidebar.selectbox("Advertising System", menu_AdversitingSytem)
	
	menu_PubAccId=['All']+df1['PubAccId'].unique().tolist()
	choice_PubAccId=st.sidebar.selectbox("Publisher Account ID", menu_PubAccId)
	
	menu_SellerDomain=['All']+df1['SellerDomain'].unique().tolist()
	choice_SellerDomain=st.sidebar.selectbox("Seller Domain", menu_SellerDomain)
	
	@st.cache
	def convert_df(df):
    	# IMPORTANT: Cache the conversion to prevent computation on every rerun
    		return df.to_csv().encode('utf-8')

	

	df1= df1[((df1['AdvertisingSystem'] ==choice_AdvertisingSystem ) | (choice_AdvertisingSystem=="All")) & ((df1['PubAccId'] ==choice_PubAccId ) | (choice_PubAccId=="All")) &((df1['SellerDomain'] ==choice_SellerDomain ) | (choice_SellerDomain=="All"))]
	df1=df1.fillna('-')
	
	csv = convert_df(df1)

	st.download_button(
    		label="Download data as CSV",
    		data=csv,
    		file_name='large_df.csv',
    		mime='text/csv',
		)
	
	st.dataframe(df1, width=None, height=1000)
	
elif choice=="APP":

	
	menu_AdversitingSytem=['All']+df2['AdvertisingSystem'].unique().tolist()
	choice_AdvertisingSystem=st.sidebar.selectbox("Advertising System", menu_AdversitingSytem)
	
	menu_PubAccId=['All']+df2['PubAccId'].unique().tolist()
	choice_PubAccId=st.sidebar.selectbox("Publisher Account ID", menu_PubAccId)
	
	menu_SellerDomain=['All']+df2['SellerDomain'].unique().tolist()
	choice_SellerDomain=st.sidebar.selectbox("Seller Domain", menu_SellerDomain)
		
		
	df2= df2[((df2['AdvertisingSystem'] ==choice_AdvertisingSystem ) | (choice_AdvertisingSystem=="All")) & ((df2['PubAccId'] ==choice_PubAccId ) | (choice_PubAccId=="All")) &((df2['SellerDomain'] ==choice_SellerDomain ) | (choice_SellerDomain=="All"))]
	df2=df2.fillna('-')
	
	
	st.dataframe(df2, width=None, height=1000)
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
	
