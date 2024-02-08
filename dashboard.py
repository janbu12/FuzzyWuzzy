import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from streamlit_option_menu import option_menu
from collections import Counter
from geopy.distance import geodesic
@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df
def pertanyaan1_10122096(orders, reviews):
    st.header("Apakah Lama Pengiriman berpengaruh terhadap review score?")
    
    #Mengambil data yang sudah terkirim
    merge_reviews_deliver_order = pd.merge(orders[orders["order_status"] == "delivered"], reviews, on='order_id', how='inner')
    
    #Mengubah tipe data pada kolom menjadi datetime
    merge_reviews_deliver_order['order_delivered_customer_date'] = pd.to_datetime(merge_reviews_deliver_order['order_delivered_customer_date'])
    merge_reviews_deliver_order['order_delivered_carrier_date'] = pd.to_datetime(merge_reviews_deliver_order['order_delivered_carrier_date'])
    
    #Membuat Kolom dari hasil perkurangan  antara tanggal terkirim dan tanggal dikirim
    merge_reviews_deliver_order['delivery_time'] = merge_reviews_deliver_order['order_delivered_customer_date'] - merge_reviews_deliver_order['order_delivered_carrier_date']
    
    data = pd.DataFrame({
        'review_score': merge_reviews_deliver_order['review_score'],
        'delivery_time': merge_reviews_deliver_order['delivery_time']
    })
    
    #Grouping berdasarkan review_score
    data = data.groupby('review_score')['delivery_time'].mean().dt.days
    
    #Grafik Pengaruh dengan plot 
    st.dataframe(data)
    fig, ax = plt.subplots()
    ax.plot(data.index, data, marker='o')
    ax.set_title('Pengaruh Waktu Pengiriman terhadap Ulasan')
    ax.set_xlabel('Review Score')
    ax.set_ylabel('Waktu Rata-rata Pengiriman (hari)')
    ax.set_xticks(data.index)
    
    st.pyplot(fig)
    
    #Expander Grafik
    with st.expander("Penjelasan Pengaruh Waktu Pengiriman terhadap Ulasan ") :
        st.write('Terlihat dari grafik diatas bahwa lama pengiriman cukup berpengaruh terhadap review score, hal yang bisa dilakukan adalah tahap processing ke shipped harus lebih diperbaiki untuk memperpendek jarak waktu dari kurir pada customer') 
    del data, merge_reviews_deliver_order


def pertanyaan2_10122096(reviews):
    st.header("Apakah highlight yang membuat customer memberikan review score yang kecil?")
    
    # Mendapatkan baris dengan nilai review_score kurang dari atau sama dengan 3
    low_scores = reviews[reviews['review_score'] <= 3]
    # Mendapatkan 15 judul komentar teratas yang paling sering muncul dalam DataFrame low_scores
    top_15_comment_titles = low_scores['review_comment_title'].value_counts().nlargest(15).index
    # Mendapatkan baris dari DataFrame low_scores di mana review_comment_title termasuk dalam 15 judul komentar teratas
    top_15_reasons = low_scores[low_scores['review_comment_title'].isin(top_15_comment_titles)]
    # Daftar kata-kata negatif dalam bahasa Portugis
    negative_words_pt = ['ruim', 'lento', 'danificado', 'decepcionado', 'decepcionante', 'problema', 'chato', 'péssimo', 'horroroso', 'terrível', 'frustrante', 'errado', 'defeito']
    # Mendapatkan baris dari DataFrame low_scores di mana panjang review_comment_message setidaknya 4 karakter
    low_scores_len = low_scores[low_scores['review_comment_message'].str.len() >= 4]
    # Mendapatkan frasa-frasa negatif yang diekstraksi dari kolom review_comment_message dalam DataFrame low_scores_len
    negative_phrases_pt = low_scores_len['review_comment_message'].apply(lambda x: [word.lower() for word in x.split() if word.lower() in negative_words_pt])
    negative_phrases_pt = [phrase for sublist in negative_phrases_pt for phrase in sublist]
    # Menghitung frekuensi kemunculan setiap kata negatif
    negative_freq_pt = Counter(negative_phrases_pt)
    # Mendapatkan lima kata negatif yang paling umum berserta jumlah kemunculannya
    common_negative_pt = negative_freq_pt.most_common(5)
    # Membuat DataFrame dari common_negative_pt
    common_negative_df_pt = pd.DataFrame(common_negative_pt, columns=['Kata', 'Jumlah'])
    # Mendapatkan jumlah kemunculan setiap kombinasi review_score dan review_comment_title
    top_15_reasons_df = top_15_reasons.groupby(['review_score', 'review_comment_title']).size().reset_index(name='jumlah')
    #Grafik berdasarkan title    
    st.dataframe(top_15_reasons_df)
    plt.figure(figsize=(10, 6))
    sea.countplot(x='review_score', hue='review_comment_title', data=top_15_reasons, palette='Set2')
    plt.title('15 Faktor Mengapa Review Score Rendah Berdasarkan Comment Title')
    plt.xlabel('Review Score')
    plt.ylabel('Count')
    plt.legend(title='Review Comment Title', bbox_to_anchor=(1, 1), loc='upper left')
    fig = plt.gcf()
    st.pyplot(fig)
    
    
    #Grafik berdasarkan kata2 
    st.dataframe(common_negative_df_pt)
    fig, ax = plt.subplots()
    ax.barh(common_negative_df_pt['Kata'], common_negative_df_pt['Jumlah'])
    ax.set_title('5 Kata Negatif Terbanyak Dalam Review Score Rendah Berdasarkan Review Message')
    ax.set_xlabel('Jumlah')
    ax.set_ylabel('Kata')
    
    st.pyplot(fig)
    
    #Expander Grafik
    with st.expander("Penjelasan Mengenai Alasan Highlight Score Rendah") :
        st.write("""<list>
                        <li>Produto errado = Produk yang salah
                        <li>Produto com defeito = Produk cacat
                        <li>Nao recomendo = Tidak merekomendasikan
                        <li>Pessimo = Sangat buruk
                        <li>Producto nao entregue = Produk tidak terkirim
                        <li>Ruim = Buruk
                        <li>Nao recebi = Tidak diterima
                </list>""", unsafe_allow_html=True) 
        st.write("""<list>
                        <li> Problema = Bermasalah
                        <li> Defeito = Cacat
                        <li> Errado = Salah
                        <li> Ruim = Buruk
                        <li> Pessimo = Sangat Buruk
                    </list>""", unsafe_allow_html=True)
        st.write("Dari grafik diatas dapat dilihat bahwa kata bermasalah sebanyak 303, cacat(154), dengan title Produk cacat(22), Produk salah(30), dll, walaupun terbilang sedikit, tetap saja harapannya perusahaan dapat memperbaiki produk yang salah, cacat, bahkan tidak terkirim, dll.")

    del low_scores, top_15_comment_titles, negative_words_pt, low_scores_len, negative_phrases_pt, negative_freq_pt, common_negative_pt, top_15_reasons_df, common_negative_df_pt

def pertanyaan3_10122096(orders, order_item, customers, sellers):
    st.header("Apakah kesamaan negara asal antara seller dan customer berpengaruh terhadap jumlah pembelian?")
    
    #Mengambil data orders dengan status terkirim, diproses, dikirim
    orders_df = orders[(orders['order_status'] == 'delivered') | (orders['order_status'] == 'shipped') | (orders['order_status'] == 'processing')]
    
    #Penggabungan dataframe untuk mengintegrasikan data customer dan seller ke dalam dataframe orders
    order_item_df = pd.merge(order_item, sellers, on='seller_id', how='inner')
    merge_order_for_state = pd.merge(orders_df, customers, on='customer_id', how='inner')
    merge_order_for_state = pd.merge(merge_order_for_state, order_item_df, on='order_id', how='inner')
    
    #Membuang data yang duplikasi, dan menyimpan data terakhirnya karena valuenya berbeda beda
    merge_order_for_state.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
    # Menghitung jumlah transaksi untuk setiap kombinasi dari negara bagian penjual dan negara bagian pelanggan
    transaction_count = merge_order_for_state.groupby(['seller_state', 'customer_state']).size().reset_index(name='transaction_count')
    # Mendapatkan lima kombinasi negara bagian penjual dan negara bagian pelanggan dengan jumlah transaksi terbanyak
    top_5_transactions = transaction_count.nlargest(5, 'transaction_count')
    # Mengubah data menjadi bentuk yang sesuai untuk digunakan dalam heatmap
    heatmap_data = top_5_transactions.pivot_table(index='seller_state', columns='customer_state', values='transaction_count')
    # Grafik Heatmap
    st.dataframe(heatmap_data)
    
    sea.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='g')
    plt.title('Pengaruh Negara Asal antara Seller dan Customer State terhadap Jumlah Transaksi')
    plt.xlabel('Customer State')
    plt.ylabel('Seller State')
    fig = plt.gcf()
    st.pyplot(fig)
    
    with st.expander("Penjelasan Mengenai Kesaaman State Antara Customer dan Seller") :
         st.write("Terlihat dari heatmap diatas seller state SP dan customer state SP dengan jumlah transaksi 31,065 yang menunjukkan bahwa kesamaan daerah asal antara seller dan customer sangat berpengaruh terhadap jumlah pembelian barang")

    del orders_df, merge_order_for_state, transaction_count, top_5_transactions, heatmap_data, order_item_df

def pertanyaan4_10122096(orders, order_item, customers, sellers, geolocation):
    order_items = pd.merge(order_item, sellers, on='seller_id', how='inner')
    order_items.drop_duplicates(['order_id'], keep='last', inplace=True, ignore_index = True)
    order_items = order_items.drop(columns=['order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value', 'seller_city'])
    # order_items = pd.merge(order_items, df_geolocation, left_on='seller_zip_code_prefix', 
    #                     right_on='geolocation_zip_code_prefix',
    #                     how="inner", )
    st.dataframe(order_items)
    
df_order_item = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_items_dataset.csv")
df_order_review = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_reviews_dataset.csv")
df_orders = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/orders_dataset.csv")
df_sellers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/sellers_dataset.csv")
df_customers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/customers_dataset.csv")
df_geolocation = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/geolocation_dataset.csv")

with st.sidebar :
    selected = option_menu('Menu',['10122096', 'blablabla'],
    icons =["easel2", "graph-up"],
    menu_icon="cast",
    default_index=0)
    
if (selected == '10122096') :
    st.header(f"Dashboard Analisis E-Commerce oleh Mizan")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
    with tab1:
        pertanyaan1_10122096(df_orders, df_order_review)
        
    with tab2:
        pertanyaan2_10122096(df_order_review)
        
    with tab3:
        pertanyaan3_10122096(df_orders, df_order_item, df_customers, df_sellers)

    with tab4:
        pertanyaan4_10122096(df_orders, df_order_item, df_customers, df_sellers, df_geolocation)

elif (selected == 'blablabla'):
    st.header(f"Dashboard Analisis E-Commerce oleh blablabla")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
