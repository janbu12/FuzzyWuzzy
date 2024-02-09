import streamlit as st
import matplotlib.pyplot as plt

def pertanyaan1_10122105(order_items):
    st.write("Apa 10 kategori produk dengan penjualan terendah?")
    categories_count_min_order = order_items["product_category_name"].value_counts(ascending=True)

    min_order = categories_count_min_order.head(10)
    del categories_count_min_order
    
    st.write(min_order)

    plt.figure(figsize=(10, 6))
    min_order.plot(kind='bar', color='lightgreen')
    plt.title('10 Kategori Produk dengan Penjualan Terendah')
    plt.xlabel('Product Category')
    plt.ylabel('Order Count')
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()
    st.pyplot()

    with st.expander("Kesimpulan"):
        st.write("Maka kesimpulan dari hasil di atas 10 Kategori Produk dengan penjualan terendah adalah security_and_service, fashion_childrens_clothes, la_cuisine, cds_dvds_musicals, arts_and_craftmanship, fashion_sport, home_comfort_2, flowers, furniture_mattress_and_upholstery, music..")
