import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from streamlit_option_menu import option_menu
from collections import Counter
from geopy.distance import geodesic

def pertanyaan1_10122096(reviews):
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
    with st.container():
        st.dataframe(top_15_reasons_df.style.highlight_max(subset='jumlah', axis=0)
                     .highlight_min(subset='jumlah', axis=0, color='#dc3545'), 
                     use_container_width=True, hide_index=True)
        
    plt.figure(figsize=(10, 6))
    sea.countplot(x='review_score', hue='review_comment_title', data=top_15_reasons, palette='Set2')
    plt.title('15 Faktor Mengapa Review Score Rendah Berdasarkan Comment Title')
    plt.xlabel('Review Score')
    plt.ylabel('Count')
    plt.legend(title='Review Comment Title', bbox_to_anchor=(1, 1), loc='upper left')
    fig = plt.gcf()
    st.pyplot(fig)
    
    
    #Grafik berdasarkan kata2 
    with st.container():
        st.dataframe(common_negative_df_pt.style.highlight_max(subset='Jumlah', axis=0)
                     .highlight_min(subset='Jumlah', axis=0, color='#dc3545'), 
                     use_container_width=True, hide_index=True)
        
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

def pertanyaan2_10122096(delivered_orders, shipped_orders, approved_orders, order_item):
    st.header("Apakah kesamaan negara asal antara seller dan customer berpengaruh terhadap jumlah pembelian?")
    
    #Mengambil data orders dengan status terkirim, diproses, dikirim
    orders_concat = pd.concat([delivered_orders[delivered_orders["order_status"] != "canceled"], shipped_orders[shipped_orders['order_status'] != 'canceled']], ignore_index=True)
    orders_concat = pd.concat([orders_concat, approved_orders[approved_orders["order_status"] != "canceled"]], ignore_index=True)
    
    #Penggabungan dataframe untuk mengintegrasikan data customer dan seller ke dalam dataframe orders
    merge_order_for_state = pd.merge(orders_concat, order_item, on='order_id', how='inner')
    
    #Membuang data yang duplikasi, dan menyimpan data terakhirnya karena valuenya berbeda beda
    merge_order_for_state.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
    # Menghitung jumlah transaksi untuk setiap kombinasi dari negara bagian penjual dan negara bagian pelanggan
    transaction_count = merge_order_for_state.groupby(['seller_state', 'customer_state']).size().reset_index(name='transaction_count')

    # Mendapatkan lima kombinasi negara bagian penjual dan negara bagian pelanggan dengan jumlah transaksi terbanyak
    top_5_transactions = transaction_count.nlargest(5, 'transaction_count')

    # Mengubah data menjadi bentuk yang sesuai untuk digunakan dalam heatmap
    heatmap_data = top_5_transactions.pivot_table(index='seller_state', columns='customer_state', values='transaction_count')

    # Grafik Heatmap
    with st.container():
        st.dataframe(heatmap_data, use_container_width=True)

    plt.figure()
    sea.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='g')
    plt.title('Pengaruh Negara Asal antara Seller dan Customer State terhadap Jumlah Transaksi')
    plt.xlabel('Customer State')
    plt.ylabel('Seller State')
    fig = plt.gcf()
    st.pyplot(fig)
    
    with st.expander("Penjelasan Mengenai Kesaaman State Antara Customer dan Seller") :
         st.write("Terlihat dari heatmap diatas seller state SP dan customer state SP dengan jumlah transaksi 30.767 yang menunjukkan bahwa kesamaan daerah asal antara seller dan customer sangat berpengaruh terhadap jumlah pembelian barang")
    
    del orders_concat, merge_order_for_state, transaction_count, top_5_transactions, heatmap_data, fig

def pertanyaan3_10122096(df_geolocation):
    st.header("Berapakah rata-rata jauh pengiriman yang sudah diterima berdasarkan seller state?")
    
    rata_rata_jarak2 = df_geolocation.groupby('seller_state')['distance_KM'].mean().reset_index()
    rata_rata_jarak2 = rata_rata_jarak2.sort_values(ascending=True, by='distance_KM', ignore_index=True)
    
    with st.container():
        st.dataframe(rata_rata_jarak2.style.highlight_max(subset='distance_KM', axis=0)
                     .highlight_min(subset='distance_KM', axis=0, color='red'), 
                     use_container_width=True, hide_index=True)

    sea.set_theme()

    plt.figure(figsize=(10, 6))
    sea.barplot(data=rata_rata_jarak2, x='seller_state', y='distance_KM', palette='viridis', hue='seller_state')
    plt.xlabel('Seller State')
    plt.ylabel('Rata-rata Jarak (km)')
    plt.title('Rata-rata Jarak berdasarkan Seller State')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)

    del  rata_rata_jarak2, fig
    
    with st.expander("Penjelasan Mengenai Rata2 Jauh Pengiriman") :
        st.write("""dari grafik diatas bisa kita lihat bahwa SP merupakan seller state yang paling kecil rata-rata jarak pengirimannya, 
                 dan cocok dengan analasis pertanyaan sebelumnya tentang SP adalah seller state dengan tingkat populer yang tinggi 
                 berdasarkan kesamaan state customer, yang cukup menjadi salah satu alasan mengapa seller state SP tingkat pembelinya tinggi""")

def pertanyaan4_10122096(df_geolocation, order_reviews):
    st.header("Apakah jauh pengiriman berdampak pada waktu pengiriman dan review score?")
    reviewsSort = order_reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])
    reviewsSort.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
    orders_review_df = pd.merge(df_geolocation[['order_id', 'distance_KM','delivery_time']], reviewsSort, on="order_id", how="inner")
    
    orders_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)

    #Filter waktu pengiriman dengan data <= 15 karena sangat banyak
    orders_review_filtered = orders_review_df[(orders_review_df['delivery_time'] <= 15) & (orders_review_df['delivery_time'] > 0)]
    orders_review_filtered = orders_review_filtered.drop(columns='review_score')
    
    review_distance_df   = orders_review_df.groupby("review_score")["distance_KM"].mean()
    mean_distance_deliver_time_df = orders_review_filtered.groupby("delivery_time")["distance_KM"].mean()

    with st.container(border=True):
        col1, col2 = st.columns([0.5,0.5])
        with col1:
            st.write("Dataframe")
            st.dataframe(review_distance_df, use_container_width=True, height = 140)
    
        with col2:
            st.write("Tabel Korelasi")
            st.dataframe(orders_review_df.corr("spearman"), use_container_width=True, height = 140)
    
    plt.figure()
    sea.lineplot(x = review_distance_df.keys(), y = review_distance_df.values)
    sea.lineplot(x = review_distance_df.keys(), y = review_distance_df.values, style = review_distance_df.keys(), 
                markers =["o", "o", "o", "o", "o"], 
                dashes = False)
    plt.title("Korelasi jauh pengiriman dan nilai review")
    plt.xlabel("Nilai Review")
    plt.ylabel("Rata-rata Pengiriman (km)")
    fig = plt.gcf()
    st.pyplot(fig)

    with st.expander("Penjelasan Mengenai Dampak Jauh Pengiriman pada Nilai Review") :
         st.write("""walaupun memang grafik terlihat signifikan semakin kecil reviewnya maka rata2 jaraknya semakin jauh pula, 
                     tetapi pada tabel korelasi antara distance dan review score hanya (-0.064719) maka hampir tidak ada pengaruh sama sekali.""")

    with st.container(border=True):
        st.dataframe(mean_distance_deliver_time_df, use_container_width=True)
        st.write("Dengan total data: ",len(orders_review_filtered))
    
    plt.figure()
    sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values)
    sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values, 
                style = mean_distance_deliver_time_df.keys(), 
                markers =["o", "o", "o", "o", "o", "o","o","o","o","o","o","o","o","o","o",], 
                dashes = False, legend=False)
    plt.title("Korelasi jauh pengiriman dan waktu pengiriman")
    plt.xlabel("Waktu Pengiriman (hari)")
    plt.ylabel("Rata-rata Pengiriman (km)")
    fig = plt.gcf()
    st.pyplot(fig)
    
    with st.expander("Penjelasan Mengenai Dampak Jauh Pengiriman pada Waktu Pengiriman") :
        st.write("""Data waktu pengiriman yang diambil adalah 15 hari kebawah, dengan dari grafik dan tabel korelasi diatas dapat dilihat bahwa jarak pengiriman cukup berpegaruh terhadap waktu 
                    pegiriman dengan korelasi (0.615205) dan grafiknya menggambarkan kenaikan yang signifikan""")
    
    del reviewsSort, orders_review_filtered, review_distance_df, mean_distance_deliver_time_df, fig
