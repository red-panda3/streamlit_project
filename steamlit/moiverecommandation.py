import streamlit as st
st.title("Moive Recommandation")
import pandas as pd
import pickle
def recommend(moive):
  moive_index=moives[moives['title']==moive].index[0]
  distance=similarity[moive_index]
  moive_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
  recom=[]
  for i in moive_list:
    recom.append(moives.iloc[i[0]].title)
  return recom  
similarity=pickle.load(open(r"C:/data/similarity.pkl", "rb"))    
moives=pickle.load(open(r"C:/data/df.pkl", "rb"))
moives_list=moives['title'].values
option = st.selectbox(
    "Choose an option:",
    moives_list
)
if st.button('Recommend'):
    recommadation=recommend(option)
    for i in recommadation:
     st.write(i)
    