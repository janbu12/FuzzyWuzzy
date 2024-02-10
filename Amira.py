#import streamlit as st, matplotlib.pyplot as plt

def pertanyaan1_10122105(min_order):
    st.write("Apa 10 kategori produk dengan penjualan terendah?<h4>", unsafe_allow_html=True)
    categories_count_min_order = min_order["product_category_name"].value_counts(ascending=True)

    min_order = categories_count_min_order.head(10)
    st.dataframe(min_order)

    plt.figure(figsize=(10, 6))
    min_order.plot(kind='bar', color='lightgreen')
    plt.title('10 Kategori Produk dengan Penjualan Terendah')
    plt.xlabel('Product Category')
    plt.ylabel('Order Count')
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

    with st.expander("Kesimpulan"):
        st.write("Maka kesimpulan dari hasil diatas\
                 10 Kategori Produk dengan penjualan terendah adalah security_and_service, fashion_childrens_clothes, la_cuisine, cds_dvds_musicals, arts_and_craftmanship, fashion_sport, home_comfort_2, flowers, furniture_mattress_and_upholstery, music..")

    del categories_count_min_order, min_order
