import pandas as pd
import numpy as np
import streamlit as st
import requests
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
    
	
    tab1, tab2, tab3 = container.tabs(["From Ads.txt","Crawl from website", "Verified relationship"])
    with tab1:
       

        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = bigquery.Client(credentials=credentials)
	
        @st.cache(max_entries=1)
        def load_data1(time): 
            query1 = """SELECT * FROM `showheroes-bi.bi.bi_adstxt` WHERE  DomainName="{}" """.format(domainname)
            query_job1 = client.query(query1)
            return client.query(query1).to_dataframe().fillna('-')

        st.dataframe(load_data1('A').reset_index(drop=True),1900,2000)
    with tab2: 
        text=[]
        if domainname !='':
            response = requests.get('https://'+domainname+'/ads.txt')
            data = response.text
            for i, line in enumerate(data.split('\n')):
                if line.count(',')==3 :
                    text.append(line.split(','))
                elif line.count(',')==2:
                    test=line.split(',')
                    test.append('')
                    text.append(test)
        
        
            # print(f'{i}   {line}')
            df=pd.DataFrame(text, columns = ['Domain', 'Account Id','Relationship','Certification Authority ID'])

            df['Relationship']=df['Relationship'].str.replace(' ','')
            df['Relationship']=df['Relationship'].str.replace('\"','')
            df['Relationship'] = df['Relationship'].str.upper()
	
            # df['Domain']=df['Domain'].str.replace('\"','')
            df['Domain'] = df['Domain'].str.lower()
	
            st.dataframe(df.reset_index(drop=True),1800,1800)
	
    with tab3:
        @st.cache(max_entries=1)
        def load_data2(time): 
            query2 = "SELECT DomainName,AdvertisingSystem, PubAccId,Relationship,SellerDomain,SellerType FROM `showheroes-bi.bi.bi_adstxt_join_sellersjson` where ((SellerDomain is not null) or (SellerName is not null) or (SellerType is not null)) and (DomainName=SellerDomain)"
            query_job2 = client.query(query2)
            return client.query(query2).to_dataframe().fillna('-')

        st.dataframe(load_data2('A').reset_index(drop=True),1800,1800)



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
