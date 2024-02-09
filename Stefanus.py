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

    sea.scatterplot(x = itemsDf["product_volume_cm"], y = itemsDf["freight_value"])
    plt.title("Scatterplot volume dan harga pengiriman barang")
    plt.xlabel("Volume Barang")
    plt.ylabel("Harga Pengiriman Barang")
    Scatter1 = plt.gcf()
    plt.close()

    sea.scatterplot(x = itemsDf["product_weight_g"], y = itemsDf["freight_value"])
    plt.title("Scatterplot berat dan harga pengiriman barang")
    plt.xlabel("Berat Barang")
    plt.ylabel("Harga Pengiriman Barang")
    Scatter2 = plt.gcf()
    plt.close()
    
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index=True)
    st.pyplot(Scatter1)
    st.pyplot(Scatter2)
    st.write("Rata-rata berat barang  : 2108.657148732713")
    st.write("Rata-rata volume barang : 15273.488057169297")
    st.write("Perkiraan harga pengiriman barang : 18.40853503")
    st.write("Rata-rata harga pengiriman barang : 20.025485039001275")

    with st.expander():
        st.markdown("Dari data yang didapat dari tabel order_items, dapat diketahui bahwa rata-rata berat barang ialah ~2.108,65715 $g$ dan rata-rata volume barang adalah ~15.273,48806 $cm^{3}$ . Dengan menggunakan algoritma pembelajaran mesin regresi kuantil, model akan dilatih dengan seluruh data berat dan volume barang yang ada. Setelah model selesai dilatih, dengan memasukkan rata-rata berat dan volume barang, model regresi dapat memprediksi harga pengiriman barang. Harga yang didapat dari model regresi tersebut ialah ~18,40853, di mana nilai tersebu tidak jauh dari rata-rata harga pengiriman barang yang sudah ada, yakni ~20,02548.")
    
    del itemsDf, correlation, Scatter1, Scatter2
