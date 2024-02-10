import streamlit as st, matplotlib.pyplot as plt, seaborn as sea

def pertanyaan1_10122104(order_items):
    st.write("<h4>Kategori barang apa yang paling banyak dibeli?<h4>", unsafe_allow_html=True)
    categories_count = order_items["product_category_name"].value_counts()
    st.markdown("Tabel Kategori Produk Yang sering dibeli")
    st.dataframe(categories_count.head(7), use_container_width = True)

    with st.container():
        myexplode = [0.2 ,0 ,0 ,0 ,0 ,0 ,0]
        plt.pie(categories_count.head(7).values, labels = categories_count.head(7).keys(), explode=myexplode, shadow=True, colors=sea.color_palette('Set3'), autopct='%1.2f%%', startangle=90)
        plt.title(label="Kategori Produk yang paling banyak di pesan")
        grafik1 = plt.gcf() 
        st.pyplot(grafik1)
        plt.close()

    with st.expander("Kesimpulan"):
        st.write("Maka dari hasil diatas\
                 Kategori Produk yang sering dipesan adalah bed_bath_table.")
    
    del categories_count, myexplode, grafik1

def pertanyaan2_10122104(delivered_orders):
    st.write("<h4>Apakah barang yang datang ke costumer melebihi tanggal estimasinya dapat mempengaruhi pembatalan pesanan?<h4>", unsafe_allow_html=True)
    st.write("<li><b>PART 1</b>", unsafe_allow_html=True)
    batal               = (delivered_orders[delivered_orders["order_status"] == "canceled"])
    batal['is_delayed'] = batal['order_delivered_customer_date'] > batal['order_estimated_delivery_date']
    batal.drop(columns = batal.columns[0], inplace=True)
    st.markdown("Tabel Pesanan Yang statusnya dibatalkan")
    st.dataframe(batal.head(), use_container_width = True)
    
    with st.container():
        grup1 = batal.groupby('is_delayed').size()
        st.markdown("Tabel Jumlah pesanan Yang Statusnya dibatalkan dan Mengalami keterlambatan ")
        st.dataframe(grup1, use_container_width = True)
    labels    = ['Not delayed', 'Delayed']
    myexplode = [0.2,0]
    colors    = sea.color_palette('Set3')

    plt.pie(grup1, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True, explode=myexplode)
    plt.title('Pembatalan Pesanan')
    grafik2 = plt.gcf()
    plt.close()
    st.pyplot(grafik2)
    st.markdown("Pada grafik pertama dimulai dari menelusuri status pesanan yang dibatalkan lalu memfilter\
                tanggal kedatangan barang di kostumer yang melebihi tanggal estimasi")

    del batal, grup1, labels, myexplode, colors, grafik2

    st.write("<li><b>PART 2</b>", unsafe_allow_html=True)
    batal               = delivered_orders
    batal["is_delayed"] = batal['order_delivered_customer_date'] > batal['order_estimated_delivery_date']
    batal               = batal[batal["is_delayed"]]
    batal.drop(columns = batal.columns[0], inplace=True)
    st.markdown("Tabel Yang mengalami keterlambatan melebihi tanggal estimasi sampai")
    st.dataframe(batal.head(), use_container_width = True)
    
    with st.container():
        grup2 = batal.groupby('order_status').size()
        st.markdown("Tabel Jumlah dari pesanan Yang Statusnya dibatalkan akibat keterlambatan")
        st.dataframe(grup2, use_container_width = True)

    labels    = ['canceled', 'delivered']
    myexplode = [0.10,0]
    colors    = ['blue','pink']

    plt.pie(grup2, labels=labels, colors=colors, autopct='%1.2f%%',  shadow=True, explode=myexplode)
    plt.title('Barang Yang Datang Melebihi Tanggal Estimasi Dan di Cancel')
    grafik3 = plt.gcf()
    plt.close()
    st.pyplot(grafik3)
    st.markdown("Pada grafik kedua dimulai dari memfilter tanggal kedatangan barang yang melebihi tanggal\
                estimasi lalu memfilter status pesanan yang dibatalkan")

    del batal, grup2, labels, myexplode, colors, grafik3

    with st.expander("Kesimpulan"):
        st.write("Maka dari hasil kedua grafik diatas meskipun memiliki persentase yang berbeda\
                 hasilnya keterlambatan kedatangan barang kepada konsumen melebihi tanggal estimasi\
                  tidak mempengaruhi secara besar dalam pembatalan pesanan.")
