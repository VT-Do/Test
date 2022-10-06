import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

st.set_page_config(page_title="The Ramsey Highlights", layout="wide")
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
    ('WEB','APP'))

menu1=["WEB", "APP"]
choice1=st.sidebar.selectbox("Choose dataset", menu1)

menu2=["A", "B"]
choice2=st.sidebar.selectbox("Choose dataset", menu2)

SellerDomain = st.sidebar.text_input("SellerDomain", "All")

# st. set_page_config(layout="wide")

col1, col2,col3 = st.columns(3)

with col1:
   st.image("images.png", width=80)

with col2:
   st.title("📊 IAB dataset")
with col3:
   st.write('')

# option = st.selectbox('Please choose the dataset',	('WEB', 'APP'))

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

#if 'sidebar_state' not in st.session_state:
	#st.session_state.sidebar_state = 'expanded'
	
AdvertisingSystem = st.sidebar.text_area('AdvertisingSystem', '''
    All
    ''')
# st.write('Sentiment:', run_sentiment_analysis(txt))

PubAccId = st.sidebar.text_area('PubAccId', '''
    All
    ''')

if choice=="WEB":
	query="SELECT * FROM `showheroes-bi.bi.bi_adstxt_join_sellerjson_with_count_domains` limit 1000"
	query_job = client.query(query)
	df=client.query(query).to_dataframe()
	st.dataframe(df, width=None, height=1000)
elif choice=="APP":
	query="SELECT * FROM `showheroes-bi.bi.bi_appadstxt_join_sellersjson_with_count_domains` limit 1000"
	query_job = client.query(query)
	df=client.query(query).to_dataframe()
	st.dataframe(df, width=None, height=1000)
