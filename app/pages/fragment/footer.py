import streamlit as st
import os

def footer():
    # Requires {{ due to python formatting using {} for keys
    footer_txt="""
<style>
footer {{
    visibility: hidden;
}}
/*
footer:after {{
	content:'{msg}'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}}
*/
</style>
""".format(msg=os.getenv("GIT_SHA", "dev"))
    st.markdown(footer_txt, unsafe_allow_html=True)