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





# col=0 (advertisingsystem), 1 (PubAccId) , 2 (Relationship),  
def check(df,col,keyword):
    list=df[col][~df[col].str.contains(keyword)].tolist()
    if len(list)>0:
        return list
    else:
        return False

# Check if AvertisingSystem contains '.' or Relationship is not DIRECT or RESELLER
def return_input_error(input):
    if check(input,0,'\.'):
        st.sidebar.write('Check AdvertisingSystem:')
        st.sidebar.write(check(input,0,'\.'))
    if check(input,2,'DIRECT|RESELLER'):
        st.sidebar.write('Check Relationship:')
        st.sidebar.write(check(input,2,'DIRECT|RESELLER'))


# df[0] (advertisingsystem), df[1] (PubAccId) , df[2] (Relationship),  
def check_row(df,input_data,row):
    df_filtered=df[(df['AdvertisingSystem']==input_data[0][row])&(df['PubAccId']==input_data[1][row])&(df['Relationship']==input_data[2][row])]
    if df_filtered.shape[0]>0:
        return df_filtered
    else:
        return None
	
#download
def download(output_data):
    if output_data.shape[0]>0:    
        csv = output_data.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download ouput as CSV",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
	
        st.dataframe(output_data.reset_index(drop=True),2100,1000)

    else:
        st.write('')
        st.write('No output found')
	

	
	
	
placeholder = st.empty() 
col01, col02,col03 = placeholder.columns(3)
with col01:
    st.write('')
with col02:
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    authenticator = stauth.Authenticate(config['credentials'],config['cookie']['name'],config['cookie']['key'],config['cookie']['expiry_days'],config['preauthorized'])	
    name, authentication_status, username = authenticator.login('Login', 'main')
with col03:
    st.write('')




if st.session_state["authentication_status"]:

    domainname = st.sidebar.text_input('Write domain here', '')
    st.sidebar.write('The current domain:', domainname)



    col4, col5,col6 = container.columns((4, 7, 1))

    with col4:
        st.image("images.png", width=80)

    with col5:
       st.title("📊 IAB dataset")
    with col6:
       authenticator.logout('Logout', 'main')
    
	
    tab1, tab2, tab3 = container.tabs(["Main","Documentation", "Contact"])
    with tab1:
       

        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = bigquery.Client(credentials=credentials)



        if ('Time1' not in st.session_state) and ('Time2' not in st.session_state):
            query_time1="SELECT Date FROM `showheroes-bi.bi.bi_adstxt_join_sellersjson_with_count_domains` limit 1"
            df_time1= client.query(query_time1).to_dataframe()
            st.session_state['Time1']=df_time1['Date'][0

	

        @st.cache(max_entries=1)
        def load_data1(time): 
            query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt` where DomainName='tokattan.com'"
            query_job1 = client.query(query1)
            return client.query(query1).to_dataframe().fillna('-')


        st.write(load_data1('A'))

    with tab2: 
        col07, col08 = st.columns(2)
        with col07:
            with st.expander("Main dataset"):
                st.write("""Write something here """)
           #     st.image("https://static.streamlit.io/examples/dice.jpg")
        with col08:
            with st.expander("Invironment"):
                st.write("""Write something here. """)
       #         st.image("https://static.streamlit.io/examples/dice.jpg")
        col09, col10 = st.columns(2)
        with col09:
            with st.expander("Upload file"):
                st.write("""Write something here. """)
          #      st.image("https://static.streamlit.io/examples/dice.jpg")
        with col10:
            with st.expander("Write/paste option"):
                st.write("""Write something here. """)
         #       st.image("https://static.streamlit.io/examples/dice.jpg")
    with tab3:
        col11, col12 = st.columns(2)
        with col11:
            option = st.selectbox("Please choose type of contact",("Report an error", "Ask questions", "Comment"))
            text_input = st.text_input(label='Your name or email')
        with col12:
            form = st.form(key='my_form')
            text=form.text_area('Enter some text', '')
            submit_button = form.form_submit_button(label='Submit')
	
        if submit_button and text !='':
            st.success('Successfully submitted. Thank you for contacting us!', icon="✅")




elif st.session_state['authentication_status'] == False:
    col04, col05,col06 = st.columns(3)
    with col04:
        st.write('')
    with col05:
        st.error('Username/password is incorrect')
    with col06:
        st.write('')
elif st.session_state['authentication_status'] == None:
    col07, col08,col09 = st.columns(3)
    with col07:
        st.write('')
    with col08:
        st.warning('Please enter your username and password')
    with col09:
        st.write('')
