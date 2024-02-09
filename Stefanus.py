import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from streamlit_option_menu import option_menu

def satu(items : pd.core.frame.DataFrame):
    #Gathering
    itemsDf = items[["order_id", "freight_value", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]]

    #Cleaning
    itemsDf.drop_duplicates(subset = ["order_id"], keep = "first", inplace = True, ignore_index = True)
    itemsDf.drop(["order_id"], axis = 1, inplace = True)
    itemsDf.insert(2, "product_volume_cm", (itemsDf["product_length_cm"] * itemsDf["product_height_cm"] * itemsDf["product_width_cm"]))
    itemsDf.drop(["product_length_cm", "product_height_cm", "product_width_cm"], axis = 1, inplace = True)
    
    #Data Mining
    correlation = itemsDf.corr("pearson")

    fig1 = sea.scatterplot(x = itemsDf["product_volume_cm"], y = itemsDf["freight_value"])
    fig1.title("Scatterplot volume dan harga pengiriman barang")
    fig1.xlabel("Volume Barang")
    fig1.ylabel("Harga Pengiriman Barang")
    Scatter1 = fig1.gcf()

    fig2 = sea.scatterplot(x = itemsDf["product_weight_g"], y = itemsDf["freight_value"])
    fig2.title("Scatterplot berat dan harga pengiriman barang")
    fig2.xlabel("Berat Barang")
    fig2.ylabel("Harga Pengiriman Barang")
    Scatter2 = fig2.gcf()
    
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index=True)
    st.pyplot(Scatter1)
    st.pyplot(Scatter2)
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.write("Rata-rata berat barang  : 2108.657148732713")
    st.write("Rata-rata volume barang : 15273.488057169297")
    st.write("Perkiraan harga pengiriman barang : 18.40853503")
    st.write("Rata-rata harga pengiriman barang : 20.025485039001275")

    del itemsDf, correlation, Scatter1, Scatter2, fig1, fig2
