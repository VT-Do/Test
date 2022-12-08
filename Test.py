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

    domainname = st.sidebar.text_input('Insert domain here', '')
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
	
        @st.cache(max_entries=1)
        def load_data1(time): 
            query1="SELECT * FROM `showheroes-bi.bi.bi_adstxt` where DomainName='tokattan.com'"
            query_job1 = client.query(query1)
            return client.query(query1).to_dataframe().fillna('-')

        st.dataframe(load_data1('A').reset_index(drop=True),2100,1000)
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
