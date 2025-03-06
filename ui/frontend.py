import os
import streamlit as st
import requests
from dotenv import load_dotenv

st.title("Chop.it - URL Shortener")
load_dotenv()

# This can be updated to point to the FastAPI service
# by default it points to localhost at port 8000
# but can be configured to point to a remote server where API is hosted

baseurl = os.getenv("HOST", "http://localhost")+":"+os.getenv("PORT", "8000")+"/"
shorten_service_url = baseurl+"url/"
count_service_url = shorten_service_url+"count/"
retreive_service_url = shorten_service_url+"original/"


if 'original_url' not in st.session_state:
    st.session_state.original_url = ""
if 'short_url' not in st.session_state:
    st.session_state.short_url = ""
if 'use_custom_url' not in st.session_state:
    st.session_state.use_custom_url = False
if 'result_message' not in st.session_state:
    st.session_state.result_message = ""
if 'click_count' not in st.session_state:
    st.session_state.click_count = ""

# Functionality to shorten the URL
with st.expander("Shorten URL", expanded=True):
    
    # Input fields that maintain values through session state
    original_url = st.text_input("Enter the URL to shorten", key="original_url_input", value=st.session_state.original_url, placeholder="http://...")
    st.session_state.original_url = original_url
    
    use_custom_url = st.checkbox("Use custom short URL", key="custom_url_checkbox", value=st.session_state.use_custom_url)
    st.session_state.use_custom_url = use_custom_url
    
    short_url = ""
    if use_custom_url:
        short_url = st.text_input("Enter the custom URL", value=st.session_state.short_url, 
                    placeholder=f"Enter text to append to {shorten_service_url}",
                    help=f"Your shortened URL will be {shorten_service_url}[your-input]")
        st.session_state.short_url = short_url
    
    
    
    input = {"original_url": original_url, "short_url": short_url}
    if st.button("Shorten URL", key="shorten_button"):
        res = requests.post(shorten_service_url, json=input)
        if res.status_code==200:
            response_data = res.json()
            
            if response_data.get("message"):
                st.session_state.result_message = response_data["message"]
                st.write(st.session_state.result_message)
                
            if response_data.get("short_url"):
                st.session_state.shortened_url = f"{shorten_service_url}{response_data['short_url']}"
                st.success(f"Short URL: {st.session_state.shortened_url}")
                
        else:
            st.error("Error in shortening the URL")
            if res.json().get("message"):
                st.warning(res.json().get("message"))

# Functionality to retrieve the original URL given the short URL
with st.expander("Retrieve Short URL Information", expanded=True):
    # Initialize session state for retrieve section
    if 'retrieve_short_url' not in st.session_state:
        st.session_state.retrieve_short_url = ""
    if 'retrieved_original_url' not in st.session_state:
        st.session_state.retrieved_original_url = ""
    
    short_url = st.text_input("Enter the short URL", key="retrieve_input", 
                              placeholder="http://...",
                              value=st.session_state.retrieve_short_url, 
                              help=f"URL in format {shorten_service_url}[short-url]")
    unique_id = short_url.split("/")[-1]
    st.session_state.retrieve_short_url = short_url

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retrieve URL", key="retrieve_button"):
            res = requests.get(retreive_service_url+f"?short_url={unique_id}")
            if res.status_code==200:
                response_data = res.json()
                if response_data.get("message"):
                    st.write(response_data["message"])
                if response_data.get("original_url"):
                    st.session_state.retrieved_original_url = response_data["original_url"]
                    st.success(f"Long URL: {st.session_state.retrieved_original_url}")
            else:
                st.error("Error in retrieving the URL: URL not found")
                if res.json().get("message"):
                    st.warning(res.json().get("message"))
    
    with col2:
        if st.button("Click Count", key="count_button"):
            try:
                res = requests.get(count_service_url+f"?short_url={unique_id}")
                if res.status_code == 200:
                    st.session_state.click_count = res.json().get("count", "0")
                    st.success(f"Total clicks: {st.session_state.click_count}")
                else:
                    st.error("Could not retrieve click count")
            except Exception as e:
                st.error(f"Error: {str(e)}")
