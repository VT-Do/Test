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





	

choice =st.sidebar.radio("Select invironment",('WEB','APP'), horizontal=True)


    if choice2=='Upload':
        uploaded_file = st.sidebar.file_uploader("Choose a .csv file")

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
	
            try:
                upload_input=pd.read_csv(uploaded_file,header=None)
                n=upload_input.shape[0]
	
	        # Clean
                upload_input[0]=upload_input[0].str.replace(' ', '').str.replace('\t','').str.lower()   
                upload_input[1]=upload_input[1].astype('string').str.replace(' ', '').str.replace('\t','').str.lower()
                upload_input[2]=upload_input[2].str.replace(' ', '').str.replace('\t','').str.upper()
	    
                return_input_error(upload_input)
                st.sidebar.dataframe(upload_input)
		
            except Exception as ex:
                st.sidebar.error('Please check the input format')
                uploaded_file=None
        

    elif choice2=='Type/Paste':
        list_lines= st.sidebar.text_area('Put lines here', 'Ex: google.com, 12335, DIRECT')
     
        try:
            input=pd.read_table(StringIO(list_lines),sep=",", header=None)
	
            # Clean
            input[0]=input[0].str.replace(' ','').str.replace('\t','').str.lower()
            input[1]=input[1].astype('string').str.replace(' ','').str.replace('\t','').str.lower()
            input[2]=input[2].str.replace(' ','').str.replace('\t','').str.upper()
            input=input.drop_duplicates()
            if list_lines !='Ex: google.com, 12335, DIRECT' and list_lines.strip()!='':
                return_input_error(input)
                st.sidebar.write('Input data',input)
        except:
            st.sidebar.error('Please check the input format')
            list_lines=''



col4, col5,col6 = container.columns((4, 7, 1))

with col4:
    st.image("images.png", width=80)
with col5:
    st.title("📊 IAB dataset")
with col6:
    st.write('')
