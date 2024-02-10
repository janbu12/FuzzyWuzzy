import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sea, streamlit as st
def pertanyaan1_220170203(order_items):
    st.write("<h4>Berapakah rata-rata kategori terbesar dan terkecil dari jumlah poto yang dipublikasikan untuk produk<h4>",unsafe_allow_html=True)
    category_photo = order_items[["product_category_name","product_photos_qty"]]
    category_photo = category_photo.groupby("product_category_name")["product_photos_qty"].mean().sort_values(ascending = False)

    with st.container():
        plt.pie(category_photo.head(), labels = category_photo.head().keys())
        grf = plt.gcf()
        st.pyplot(grf)
        plt.close()
        
        plt.pie(category_photo.tail(), labels = category_photo.tail().keys())
        grf = plt.gcf()
        st.pyplot(grf)
        plt.close()

    with st.expander("Kesimpulan"):
        st.write("Kategori Dapat disimpulkan bahwa kategori terbesar dari jumlah foto yang di publikasikan adalah fashion shoes dengan rata rata 5.229008 adapun kategori terkecil dari jumlah foto yang dipublikasikan adalah home comfort 2 dengan rata rata 1.033333")

    del grf, category_photo
