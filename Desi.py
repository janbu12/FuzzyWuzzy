import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sea, streamlit as st
def pertanyaan1_220170203(order_items):
    st.write("<h4>Berapakah rata rata kategori terbesar dan terkecil dari jumlah foto yang dipublikasikan untuk produk?<h4>", unsafe_allow_html=True)
    category_photo = category_photo.groupby("product_category_name")["product_photos_qty"].mean().sort_values(ascending = False)
    display(category_photo.head())
    display(category_photo.tail())
with st.container():
    plt.pie(category_photo.head(), labels = category_photo.head().keys())
    plt.show()
    plt.pie(category_photo.tail(), labels = category_photo.tail().keys())
    plt.show()
    grf = plt.gcf()
    plt.close()
    st.pyplot(grf)

del grf

with st.expander("Kesimpulan"):
        st.write("Kategori terbesar dari jumlah foto yangdi publikasikan adalah fashion shoes dengan rata rata 5.229008 adapun kategori terkecil dari jumlah foto yang dipublikasikan adalah home comfort 2 dengan rata rata 1.033333") 