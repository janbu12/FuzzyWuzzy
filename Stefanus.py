import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from sklearn.linear_model import QuantileRegressor
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

    sea.scatterplot(x = itemsDf["product_weight_g"], y = itemsDf["freight_value"])
    plt.title("Scatterplot berat dan harga pengiriman barang")
    plt.xlabel("Berat Barang")
    plt.ylabel("Harga Pengiriman Barang")
    Scatter2 = plt.gcf()

    quantile_regressor = QuantileRegressor(solver = "highs")
    quantile_regressor.fit(itemsDf[["product_weight_g", "product_volume_cm"]].values, itemsDf["freight_value"])

    means = [[itemsDf["product_weight_g"].mean(), itemsDf["product_volume_cm"].mean()]]
    
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>')
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index=True)
    st.pyplot(Scatter1)
    st.pyplot(Scatter2)
    st.write("Rata-rata berat barang  :", itemsDf["product_weight_g"].mean())
    st.write("Rata-rata volume barang :", itemsDf["product_volume_cm"].mean())
    st.write("Perkiraan harga pengiriman barang :", quantile_regressor.predict(means))
