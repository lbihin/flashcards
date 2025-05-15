import numpy as np
import pandas as pd
import streamlit as st

ths, cards = st.columns(2)

with ths:
    
    st.write('THIS IS A TEXT')

with cards:
    st.write('THIS IS ANOTHER TEXT')