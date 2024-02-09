import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sea

def pertanyaan1_10122079(order_items):
    st.write("<h4>10 Kategori Produk Dengan Penjualan tertinggi?<h4>", unsafe_allow_html=True)
    categories_count_max_order = order_items["product_category_name"].value_counts()
    max_order = categories_count_max_order.head(10)
    del categories_count_max_order

    
    with st.container():
    plt.figure(figsize=(10, 6))
    max_order.plot(kind='bar', color='lightblue')
    plt.title('10 Kategori Produk dengan Penjualan Tertinggi')
    plt.xlabel('Product Category')
    plt.ylabel('Order Count')
    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()
    plt.show()


    with st.expander("Kesimpulan"):
    st.write("Ini adalah 10 Kategori produk dengan penjualan tertinggi 
    Bed bath table, 
    Health beauty, 
    Sports leisure, 
    Furniture decor, 
    Computer accessories, 
    Housewares, 
    Watches gifts, 
    Telephon, 
    Garden Tools, 
    Auto")
