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
    
    
def pertanyaan3_10122096(orders, order_item, sellers, customers):
    st.header("Apakah kesamaan negara asal antara seller dan customer berpengaruh terhadap jumlah pembelian?")
    
    #Mengambil data orders dengan status terkirim, diproses, dikirim
    orders= pd.merge(orders[orders['order_status'] != 'cancelled'], customers, on='customer_id', how="inner")
    order_item = pd.merge(order_item, sellers, on='seller_id', how="inner")
    
    #Penggabungan dataframe untuk mengintegrasikan data customer dan seller ke dalam dataframe orders
    merge_order_for_state = pd.merge(orders, order_item, on='order_id', how='inner')
    
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
         st.write("Terlihat dari heatmap diatas seller state SP dan customer state SP dengan jumlah transaksi 30.767 yang menunjukkan bahwa kesamaan daerah asal antara seller dan customer sangat berpengaruh terhadap jumlah pembelian barang")
    
    del orders, sellers, merge_order_for_state, transaction_count, top_5_transactions, heatmap_data
    
    
def hitung_jarak(row):
    customer_coords = (row['geolocation_lat_x'], row['geolocation_lng_x'])
    seller_coords = (row['geolocation_lat_y'], row['geolocation_lng_y'])
    return geodesic(customer_coords, seller_coords).kilometers

def pertanyaan1_10122096(order_item, sellers, orders, customers, geolocation):
    st.header("Berapakah rata-rata jauh pengiriman yang sudah diterima berdasarkan seller state?")
    geolocation = geolocation.rename(columns={'geolocation_zip_code_prefix': 'code_prefix'})
    sellers = sellers.rename(columns={'seller_zip_code_prefix':'code_prefix'})
    customers = customers.rename(columns={'customer_zip_code_prefix':'code_prefix'})
    
    order_items = pd.merge(order_item, sellers, on='seller_id', how="inner")
    
    # order_items_geo = pd.merge(order_items, geolocation, on="code_prefix", how="inner")
    # order_items_geo.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    # order_items_geo = order_items_geo.drop(columns=['geolocation_zip_code_prefix','geolocation_city','geolocation_state','seller_city'])
    # orders = pd.merge(orders[orders['order_status']=='delivered'], customers, on='customer_id', how="inner")
    # orders_geo =  pd.merge(orders, geolocation, left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="inner")
    # orders_geo.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    # orders_geo = orders_geo.drop(columns=['geolocation_zip_code_prefix','geolocation_city','geolocation_state','customer_city','order_status',
    #                                     'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date',
    #                                     'order_estimated_delivery_date', 'customer_unique_id'])
    # merge_orders = pd.merge(orders_geo, order_items_geo, on="order_id", how="inner")
    # merge_orders['distance_KM'] = merge_orders.apply(hitung_jarak, axis=1)
    
    # rata_rata_jarak2 = merge_orders.groupby('seller_state')['distance_KM'].mean().reset_index()
    # rata_rata_jarak2 = rata_rata_jarak2.sort_values(ascending=True, by='distance_KM', ignore_index=True)
    
    # st.dataframe(rata_rata_jarak2)
        
    # sea.set_theme()

    # plt.figure(figsize=(10, 6))
    # sea.barplot(data=rata_rata_jarak2, x='seller_state', y='distance_KM', palette='viridis', hue='seller_state')
    # plt.xlabel('Seller State')
    # plt.ylabel('Rata-rata Jarak (km)')
    # plt.title('Rata-rata Jarak berdasarkan Seller State')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # fig = plt.gcf()
    # st.pyplot(fig)
    # del  rata_rata_jarak2
    
    # with st.expander("Penjelasan Mengenai Rata2 Jauh Pengiriman") :
    #     st.write("""dari grafik diatas bisa kita lihat bahwa SP merupakan seller state yang paling kecil rata-rata jarak pengirimannya, 
    #              dan cocok dengan analasis pertanyaan sebelumnya tentang SP adalah seller state dengan tingkat populer yang tinggi 
    #              berdasarkan kesamaan state customer, yang cukup menjadi salah satu alasan mengapa seller state SP tingkat pembelinya tinggi""")
    
    
def pertanyaan4_10122096(merge_orders_df, order_reviews):
    st.header("Apakah jauh pengiriman berdampak pada waktu pengiriman dan review score?")
    reviewsSort = order_reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])
    reviewsSort.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
    orders_review_df = pd.merge(merge_orders_df[['order_id', 'distance_KM','delivery_time']], reviewsSort, on="order_id", how="inner")
    
    orders_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)

    #Filter waktu pengiriman dengan data <= 15 karena sangat banyak
    orders_review_filtered = orders_review_df[(orders_review_df['delivery_time'] <= 15) & (orders_review_df['delivery_time'] > 0)]
    orders_review_filtered = orders_review_filtered.drop(columns='review_score')
    
    review_distance_df   = orders_review_df.groupby("review_score")["distance_KM"].mean()
    mean_distance_deliver_time_df = orders_review_filtered.groupby("delivery_time")["distance_KM"].mean()

    st.dataframe(review_distance_df)
    st.write("Tabel Korelasi")
    st.write(orders_review_df.corr("spearman"))
    
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
    
    plt.figure()
    sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values)
    sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values, 
                style = mean_distance_deliver_time_df.keys(), 
                markers =["o", "o", "o", "o", "o", "o","o","o","o","o","o","o","o","o","o",], 
                dashes = False)
    plt.title("Korelasi jauh pengiriman dan waktu pengiriman")
    plt.xlabel("Waktu Pengiriman (hari)")
    plt.ylabel("Rata-rata Pengiriman (km)")
    fig = plt.gcf()
    st.pyplot(fig)
    
    with st.expander("Penjelasan Mengenai Dampak Jauh Pengiriman pada Nilai Review dan Waktu Pengiriman") :
        st.write("""<li>Korelasi Jauh Pengiriman pada Nilai Review</li>
                        walaupun memang grafik terlihat signifikan semakin kecil reviewnya maka rata2 jaraknya semakin jauh pula, 
                        tetapi pada tabel korelasi antara distance dan review score hanya (-0.064719) maka hampir tidak ada pengaruh sama sekali.
                    <li>Korelasi Jauh Pengiriman pada Waktu Pengiriman</li>
                        dari grafik dan tabel korelasi diatas dapat dilihat bahwa jarak pengiriman cukup berpegaruh terhadap waktu 
                        pegiriman dengan korelasi (0.615205) dan grafiknya menggambarkan kenaikan yang signifikan""", unsafe_allow_html=True)
    
    del reviewsSort, orders_review_filtered, review_distance_df, mean_distance_deliver_time_df
    


        
#Data Gathering        
df_order_item = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_items_dataset.csv")
df_order_review = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_reviews_dataset.csv")
df_orders = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/orders_dataset.csv")
df_sellers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/sellers_dataset.csv")
df_customers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/customers_dataset.csv")
df_geolocation = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/geolocation_dataset.csv")
products = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/products_dataset.csv")
product_category_name_translation = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/product_category_name_translation.csv")
order_payments = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_payments_dataset.csv")
order_reviews = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_reviews_dataset.csv")


st.markdown("""
    <header>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    </header>
    <style>
        html, body, h1, h2, h3, p, b, nav-link [class*="css"] {font-family: 'Poppins', sans-serif;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar :
    selected = option_menu('NIM',['blablabal1','10122096', 'blablabla'],
    icons =["person-circle","person-workspace","person-badge-fill"],
    menu_icon="person-lines-fill",
    default_index=0,
    styles={
        "nav": {"font-family": 'Poppins'},
        "menu-title": {"font-family": 'Poppins', "font-weight": "700"},
        "nav-link-selected": {"font-weight": "700", "background-color": "#dc3545"},
        "icon": {"font-size": "20px"},
        "nav-link": {"--hover-color": "#dc3545"}
        }
    )
    
if (selected == '10122096') :
    #Geolocation analysis
    st.header(f"Dashboard Analisis E-Commerce oleh Mizan")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
    with tab1:
        pertanyaan1_10122096(df_order_item, df_sellers, df_orders, df_customers, df_geolocation)
        
    with tab2:
        pertanyaan2_10122096(df_order_review)
        
    with tab3:
        pertanyaan3_10122096(df_orders, df_order_item, df_sellers, df_customers)
        
    # with tab4:
    #     pertanyaan4_10122096(merge_orders_df, order_reviews)
        
elif (selected == 'blablabal1'):
    st.header(f"Dashboard Analisis E-Commerce oleh blablabal1")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])

elif (selected == 'blablabla'):
    st.header(f"Dashboard Analisis E-Commerce oleh blablabla")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
