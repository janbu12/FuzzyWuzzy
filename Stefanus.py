import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from streamlit_option_menu import option_menu

def satu(items : pd.core.frame.DataFrame):
    # Gathering
    itemsDf = items[["order_id", "freight_value", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]]

    # Cleaning
    itemsDf.drop_duplicates(subset = ["order_id"], keep = "first", inplace = True, ignore_index = True)
    itemsDf.drop(["order_id"], axis = 1, inplace = True)
    itemsDf.insert(2, "product_volume_cm", (itemsDf["product_length_cm"] * itemsDf["product_height_cm"] * itemsDf["product_width_cm"]))
    itemsDf.drop(["product_length_cm", "product_height_cm", "product_width_cm"], axis = 1, inplace = True)
    
    # Data Mining
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
    
    # Conclusion
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index          = True)
    st.pyplot(Scatter1)
    st.pyplot(Scatter2)
    st.write("Rata-rata berat barang  : 2108.657148732713")
    st.write("Rata-rata volume barang : 15273.488057169297")
    st.write("Perkiraan harga pengiriman barang : 18.40853503")
    st.write("Rata-rata harga pengiriman barang : 20.025485039001275")

    st.markdown("Dari data yang didapat dari tabel order_items, dapat diketahui bahwa rata-rata berat barang ialah ~2.108,65715 $g$ dan rata-rata volume barang adalah ~15.273,48806 $cm^{3}$ . \
                Dengan menggunakan algoritma pembelajaran mesin regresi kuantil, model akan dilatih dengan seluruh data berat dan volume barang yang ada. \
                Setelah model selesai dilatih, dengan memasukkan rata-rata berat dan volume barang, model regresi dapat memprediksi harga pengiriman barang. \
                Harga yang didapat dari model regresi tersebut ialah ~18,40853, di mana nilai tersebu tidak jauh dari rata-rata harga pengiriman barang yang sudah ada, yakni ~20,02548.")
    
    with st.expander("Kesimpulan"):
        st.write("Kesimpulan dari pertanyaan ini ialah:\
                 <li>Apabila ada suatu barang dengan berat dan volume yang mendekati rata-rata berat dan volume pada data tersebut, harga pengiriman yang harus dibayar berkisar pada 18 - 20 Brazilian Real.\
                 <li>Model regresi hasil proses ini dapat dipakai untuk menentukan harga pengiriman, dikarenakan data prediksi dan data real tidak memiliki perbedaan yang siginfikan.", unsafe_allow_html = True)
    
    # Deletion
    del itemsDf, correlation, Scatter1, Scatter2

def dua(items : pd.core.frame.DataFrame, reviews : pd.core.frame.DataFrame):
    # Gathering
    itemsDf   = items[["order_id", "price", "freight_value"]]
    reviewsDf = reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])

    # Cleaning
    itemsDf.drop_duplicates(["order_id"], keep = "first", inplace = True, ignore_index = True)
    reviewsDf.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    item_review_df = pd.concat([itemsDf, reviewsDf], axis = 1, join = "inner")
    item_review_df = item_review_df.iloc[:, [i for i, x in enumerate(item_review_df.columns) if i != 3]]
    item_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)

    # Data Mining
    correlation = item_review_df.corr()
    price_review_df   = item_review_df.groupby("review_score")["price"].mean()
    freight_review_df = item_review_df.groupby("review_score")["freight_value"].mean()

    sea.lineplot(x = price_review_df.keys(), y = price_review_df.values)
    sea.lineplot(x = price_review_df.keys(), y = price_review_df.values, style = price_review_df.keys(), markers =["o", "o", "o", "o", "o"], dashes = False)
    plt.title("Korelasi harga barang dan nilai review")
    plt.xlabel("Nilai Review")
    plt.ylabel("Harga Barang")
    Figure1 = plt.gcf()
    plt.close()

    sea.lineplot(x = freight_review_df.keys(), y = freight_review_df.values)
    sea.lineplot(x = freight_review_df.keys(), y = freight_review_df.values, style = freight_review_df.keys(), markers =["o", "o", "o", "o", "o"], dashes = False)
    plt.title("Korelasi harga pengiriman barang dan nilai review")
    plt.xlabel("Nilai Review")
    plt.ylabel("Harga Pengiriman Barang")
    Figure2 = plt.gcf()
    plt.close()

    # Conclusion
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index          = True)
    st.pyplot(Figure1)
    st.pyplot(Figure2)
    st.markdown('Apabila dilihat dari nilai korelasi antara harga barang dengan nilai review (-0,000007) dan nilai korelasi antara harga pengiriman barang dan nilai review (0,001911), \
                dapat diketahui bahwa harga barang dan harga pengiriman barang hampir tidak memiliki pengaruh sama sekali kepada nilai review. \
                Hal ini dapat dibuktikan juga pada kedua grafik diatas, tidak ada pola signifikan yang dapat menunjukan hubungan antara ketiga variabel.')
    with st.expander("Kesimpulan"):
        st.write("Kesimpulan dari pertanyaan ini ialah:\
                 <li>Harga barang dan harga pengiriman barang tidak memiliki pengaruh yang signifikan terhadap nilai review yang diberikan oleh pengguna.\
                 <li>Harga pengiriman barang (0,001911) memiliki pengaruh yang lebih besar dibandingkan harga barang (-0,000007) kepada nilai review, walaupun hampir tidak memiliki pengaruh.", unsafe_allow_html = True)

    # Deletion
    del itemsDf, reviewsDf, item_review_df, correlation, price_review_df, freight_review_df, Figure1, Figure2
