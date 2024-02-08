import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from streamlit_option_menu import option_menu
from collections import Counter
from geopy.distance import geodesic
from Mizan import pertanyaan1_10122096, pertanyaan2_10122096, pertanyaan3_10122096, pertanyaan4_10122096

@st.cache_data
def load_data(url) :
    df = pd.read_csv(url)
    return df
# def pertanyaan1_10122096(orders, reviews):
#     st.header("Apakah Lama Pengiriman berpengaruh terhadap review score?")
    
#     #Mengambil data yang sudah terkirim
#     merge_reviews_deliver_order = pd.merge(orders[orders["order_status"] == "delivered"], reviews, on='order_id', how='inner')
    
#     #Mengubah tipe data pada kolom menjadi datetime
#     merge_reviews_deliver_order['order_delivered_customer_date'] = pd.to_datetime(merge_reviews_deliver_order['order_delivered_customer_date'])
#     merge_reviews_deliver_order['order_delivered_carrier_date'] = pd.to_datetime(merge_reviews_deliver_order['order_delivered_carrier_date'])
    
#     #Membuat Kolom dari hasil perkurangan  antara tanggal terkirim dan tanggal dikirim
#     merge_reviews_deliver_order['delivery_time'] = merge_reviews_deliver_order['order_delivered_customer_date'] - merge_reviews_deliver_order['order_delivered_carrier_date']
    
#     data = pd.DataFrame({
#         'review_score': merge_reviews_deliver_order['review_score'],
#         'delivery_time': merge_reviews_deliver_order['delivery_time']
#     })
    
#     #Grouping berdasarkan review_score
#     data = data.groupby('review_score')['delivery_time'].mean().dt.days
    
#     #Grafik Pengaruh dengan plot 
#     st.dataframe(data)
#     fig, ax = plt.subplots()
#     ax.plot(data.index, data, marker='o')
#     ax.set_title('Pengaruh Waktu Pengiriman terhadap Ulasan')
#     ax.set_xlabel('Review Score')
#     ax.set_ylabel('Waktu Rata-rata Pengiriman (hari)')
#     ax.set_xticks(data.index)
    
#     st.pyplot(fig)
    
#     #Expander Grafik
#     with st.expander("Penjelasan Pengaruh Waktu Pengiriman terhadap Ulasan ") :
#         st.write('Terlihat dari grafik diatas bahwa lama pengiriman cukup berpengaruh terhadap review score, hal yang bisa dilakukan adalah tahap processing ke shipped harus lebih diperbaiki untuk memperpendek jarak waktu dari kurir pada customer') 
#     del data, merge_reviews_deliver_order


# def pertanyaan1_10122096(reviews):
#     st.header("Apakah highlight yang membuat customer memberikan review score yang kecil?")
    
#     # Mendapatkan baris dengan nilai review_score kurang dari atau sama dengan 3
#     low_scores = reviews[reviews['review_score'] <= 3]
#     # Mendapatkan 15 judul komentar teratas yang paling sering muncul dalam DataFrame low_scores
#     top_15_comment_titles = low_scores['review_comment_title'].value_counts().nlargest(15).index
#     # Mendapatkan baris dari DataFrame low_scores di mana review_comment_title termasuk dalam 15 judul komentar teratas
#     top_15_reasons = low_scores[low_scores['review_comment_title'].isin(top_15_comment_titles)]
#     # Daftar kata-kata negatif dalam bahasa Portugis
#     negative_words_pt = ['ruim', 'lento', 'danificado', 'decepcionado', 'decepcionante', 'problema', 'chato', 'péssimo', 'horroroso', 'terrível', 'frustrante', 'errado', 'defeito']
#     # Mendapatkan baris dari DataFrame low_scores di mana panjang review_comment_message setidaknya 4 karakter
#     low_scores_len = low_scores[low_scores['review_comment_message'].str.len() >= 4]
#     # Mendapatkan frasa-frasa negatif yang diekstraksi dari kolom review_comment_message dalam DataFrame low_scores_len
#     negative_phrases_pt = low_scores_len['review_comment_message'].apply(lambda x: [word.lower() for word in x.split() if word.lower() in negative_words_pt])
#     negative_phrases_pt = [phrase for sublist in negative_phrases_pt for phrase in sublist]
#     # Menghitung frekuensi kemunculan setiap kata negatif
#     negative_freq_pt = Counter(negative_phrases_pt)
#     # Mendapatkan lima kata negatif yang paling umum berserta jumlah kemunculannya
#     common_negative_pt = negative_freq_pt.most_common(5)
#     # Membuat DataFrame dari common_negative_pt
#     common_negative_df_pt = pd.DataFrame(common_negative_pt, columns=['Kata', 'Jumlah'])
#     # Mendapatkan jumlah kemunculan setiap kombinasi review_score dan review_comment_title
#     top_15_reasons_df = top_15_reasons.groupby(['review_score', 'review_comment_title']).size().reset_index(name='jumlah')
#     #Grafik berdasarkan title    
#     st.dataframe(top_15_reasons_df)
#     plt.figure(figsize=(10, 6))
#     sea.countplot(x='review_score', hue='review_comment_title', data=top_15_reasons, palette='Set2')
#     plt.title('15 Faktor Mengapa Review Score Rendah Berdasarkan Comment Title')
#     plt.xlabel('Review Score')
#     plt.ylabel('Count')
#     plt.legend(title='Review Comment Title', bbox_to_anchor=(1, 1), loc='upper left')
#     fig = plt.gcf()
#     st.pyplot(fig)
    
    
#     #Grafik berdasarkan kata2 
#     st.dataframe(common_negative_df_pt)
#     fig, ax = plt.subplots()
#     ax.barh(common_negative_df_pt['Kata'], common_negative_df_pt['Jumlah'])
#     ax.set_title('5 Kata Negatif Terbanyak Dalam Review Score Rendah Berdasarkan Review Message')
#     ax.set_xlabel('Jumlah')
#     ax.set_ylabel('Kata')
    
#     st.pyplot(fig)
    
#     #Expander Grafik
#     with st.expander("Penjelasan Mengenai Alasan Highlight Score Rendah") :
#         st.write("""<list>
#                         <li>Produto errado = Produk yang salah
#                         <li>Produto com defeito = Produk cacat
#                         <li>Nao recomendo = Tidak merekomendasikan
#                         <li>Pessimo = Sangat buruk
#                         <li>Producto nao entregue = Produk tidak terkirim
#                         <li>Ruim = Buruk
#                         <li>Nao recebi = Tidak diterima
#                 </list>""", unsafe_allow_html=True) 
#         st.write("""<list>
#                         <li> Problema = Bermasalah
#                         <li> Defeito = Cacat
#                         <li> Errado = Salah
#                         <li> Ruim = Buruk
#                         <li> Pessimo = Sangat Buruk
#                     </list>""", unsafe_allow_html=True)
#         st.write("Dari grafik diatas dapat dilihat bahwa kata bermasalah sebanyak 303, cacat(154), dengan title Produk cacat(22), Produk salah(30), dll, walaupun terbilang sedikit, tetap saja harapannya perusahaan dapat memperbaiki produk yang salah, cacat, bahkan tidak terkirim, dll.")

#     del low_scores, top_15_comment_titles, negative_words_pt, low_scores_len, negative_phrases_pt, negative_freq_pt, common_negative_pt, top_15_reasons_df, common_negative_df_pt

# def pertanyaan2_10122096(delivered_orders, shipped_orders, approved_orders, order_item):
#     st.header("Apakah kesamaan negara asal antara seller dan customer berpengaruh terhadap jumlah pembelian?")
    
#     #Mengambil data orders dengan status terkirim, diproses, dikirim
#     orders_concat = pd.concat([delivered_orders[delivered_orders["order_status"] != "canceled"], shipped_orders[shipped_orders['order_status'] != 'canceled']], ignore_index=True)
#     orders_concat = pd.concat([orders_concat, approved_orders[approved_orders["order_status"] != "canceled"]], ignore_index=True)
    
#     #Penggabungan dataframe untuk mengintegrasikan data customer dan seller ke dalam dataframe orders
#     merge_order_for_state = pd.merge(orders_concat, order_item, on='order_id', how='inner')
    
#     #Membuang data yang duplikasi, dan menyimpan data terakhirnya karena valuenya berbeda beda
#     merge_order_for_state.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
#     # Menghitung jumlah transaksi untuk setiap kombinasi dari negara bagian penjual dan negara bagian pelanggan
#     transaction_count = merge_order_for_state.groupby(['seller_state', 'customer_state']).size().reset_index(name='transaction_count')

#     # Mendapatkan lima kombinasi negara bagian penjual dan negara bagian pelanggan dengan jumlah transaksi terbanyak
#     top_5_transactions = transaction_count.nlargest(5, 'transaction_count')

#     # Mengubah data menjadi bentuk yang sesuai untuk digunakan dalam heatmap
#     heatmap_data = top_5_transactions.pivot_table(index='seller_state', columns='customer_state', values='transaction_count')

#     # Grafik Heatmap
#     st.dataframe(heatmap_data)

#     plt.figure()
#     sea.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='g')
#     plt.title('Pengaruh Negara Asal antara Seller dan Customer State terhadap Jumlah Transaksi')
#     plt.xlabel('Customer State')
#     plt.ylabel('Seller State')
#     fig = plt.gcf()
#     st.pyplot(fig)
    
#     with st.expander("Penjelasan Mengenai Kesaaman State Antara Customer dan Seller") :
#          st.write("Terlihat dari heatmap diatas seller state SP dan customer state SP dengan jumlah transaksi 30.767 yang menunjukkan bahwa kesamaan daerah asal antara seller dan customer sangat berpengaruh terhadap jumlah pembelian barang")
    
#     del orders_concat, merge_order_for_state, transaction_count, top_5_transactions, heatmap_data, fig

# def pertanyaan3_10122096(df_geolocation):
#     st.header("Berapakah rata-rata jauh pengiriman yang sudah diterima berdasarkan seller state?")
    
#     rata_rata_jarak2 = df_geolocation.groupby('seller_state')['distance_KM'].mean().reset_index()
#     rata_rata_jarak2 = rata_rata_jarak2.sort_values(ascending=True, by='distance_KM', ignore_index=True)

#     st.dataframe(rata_rata_jarak2)

#     sea.set_theme()

#     plt.figure(figsize=(10, 6))
#     sea.barplot(data=rata_rata_jarak2, x='seller_state', y='distance_KM', palette='viridis', hue='seller_state')
#     plt.xlabel('Seller State')
#     plt.ylabel('Rata-rata Jarak (km)')
#     plt.title('Rata-rata Jarak berdasarkan Seller State')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     fig = plt.gcf()
#     st.pyplot(fig)

#     del  rata_rata_jarak2, fig
    
#     with st.expander("Penjelasan Mengenai Rata2 Jauh Pengiriman") :
#         st.write("""dari grafik diatas bisa kita lihat bahwa SP merupakan seller state yang paling kecil rata-rata jarak pengirimannya, 
#                  dan cocok dengan analasis pertanyaan sebelumnya tentang SP adalah seller state dengan tingkat populer yang tinggi 
#                  berdasarkan kesamaan state customer, yang cukup menjadi salah satu alasan mengapa seller state SP tingkat pembelinya tinggi""")

# def pertanyaan4_10122096(df_geolocation, order_reviews):
#     st.header("Apakah jauh pengiriman berdampak pada waktu pengiriman dan review score?")
#     reviewsSort = order_reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])
#     reviewsSort.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    
#     orders_review_df = pd.merge(df_geolocation[['order_id', 'distance_KM','delivery_time']], reviewsSort, on="order_id", how="inner")
    
#     orders_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)

#     #Filter waktu pengiriman dengan data <= 15 karena sangat banyak
#     orders_review_filtered = orders_review_df[(orders_review_df['delivery_time'] <= 15) & (orders_review_df['delivery_time'] > 0)]
#     orders_review_filtered = orders_review_filtered.drop(columns='review_score')
    
#     review_distance_df   = orders_review_df.groupby("review_score")["distance_KM"].mean()
#     mean_distance_deliver_time_df = orders_review_filtered.groupby("delivery_time")["distance_KM"].mean()

#     st.dataframe(review_distance_df)
#     st.write("Tabel Korelasi")
#     st.write(orders_review_df.corr("spearman"))
    
#     plt.figure()
#     sea.lineplot(x = review_distance_df.keys(), y = review_distance_df.values)
#     sea.lineplot(x = review_distance_df.keys(), y = review_distance_df.values, style = review_distance_df.keys(), 
#                 markers =["o", "o", "o", "o", "o"], 
#                 dashes = False)
#     plt.title("Korelasi jauh pengiriman dan nilai review")
#     plt.xlabel("Nilai Review")
#     plt.ylabel("Rata-rata Pengiriman (km)")
#     fig = plt.gcf()
#     st.pyplot(fig)
    
#     plt.figure()
#     sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values)
#     sea.lineplot(x = mean_distance_deliver_time_df.keys(), y = mean_distance_deliver_time_df.values, 
#                 style = mean_distance_deliver_time_df.keys(), 
#                 markers =["o", "o", "o", "o", "o", "o","o","o","o","o","o","o","o","o","o",], 
#                 dashes = False, legend=False)
#     plt.title("Korelasi jauh pengiriman dan waktu pengiriman")
#     plt.xlabel("Waktu Pengiriman (hari)")
#     plt.ylabel("Rata-rata Pengiriman (km)")
#     fig = plt.gcf()
#     st.pyplot(fig)
    
#     with st.expander("Penjelasan Mengenai Dampak Jauh Pengiriman pada Nilai Review dan Waktu Pengiriman") :
#         st.write("""<li>Korelasi Jauh Pengiriman pada Nilai Review</li>
#                         walaupun memang grafik terlihat signifikan semakin kecil reviewnya maka rata2 jaraknya semakin jauh pula, 
#                         tetapi pada tabel korelasi antara distance dan review score hanya (-0.064719) maka hampir tidak ada pengaruh sama sekali.
#                     <li>Korelasi Jauh Pengiriman pada Waktu Pengiriman</li>
#                         dari grafik dan tabel korelasi diatas dapat dilihat bahwa jarak pengiriman cukup berpegaruh terhadap waktu 
#                         pegiriman dengan korelasi (0.615205) dan grafiknya menggambarkan kenaikan yang signifikan""", unsafe_allow_html=True)
    
#     del reviewsSort, orders_review_filtered, review_distance_df, mean_distance_deliver_time_df, fig
    
    
df_order_item = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_items_dataset.csv")
df_order_review = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_reviews_dataset.csv")
order_reviews = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/order_reviews_dataset.csv")
df_orders = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/orders_dataset.csv")
df_sellers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/sellers_dataset.csv")
df_customers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/customers_dataset.csv")
#karena data terlalu besar untuk dicleaning & merging, jadi dibuat csv yang sudah dicleaningnya untuk membatasi limit ram usage
df_geolocation_merging = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/Geolocation_merging.csv")
products = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/products_dataset.csv")
product_category_name_translation = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/product_category_name_translation.csv")

#Cleaning

#Type Alteration
df_order_item["shipping_limit_date"] = df_order_item["shipping_limit_date"].astype("datetime64[ns]")

df_order_review["review_creation_date"]    = df_order_review["review_creation_date"].astype("datetime64[ns]")
df_order_review["review_answer_timestamp"] = df_order_review["review_answer_timestamp"].astype("datetime64[ns]")

df_orders["order_purchase_timestamp"]      = df_orders["order_purchase_timestamp"].astype("datetime64[ns]")
df_orders["order_approved_at"]             = df_orders["order_approved_at"].astype("datetime64[ns]")
df_orders["order_delivered_carrier_date"]  = df_orders["order_delivered_carrier_date"].astype("datetime64[ns]")
df_orders["order_delivered_customer_date"] = df_orders["order_delivered_customer_date"].astype("datetime64[ns]")
df_orders["order_estimated_delivery_date"] = df_orders["order_estimated_delivery_date"].astype("datetime64[ns]")

#Tabel Merging
products = products.join(product_category_name_translation.set_index("product_category_name"), "product_category_name", validate = "m:1")
products["product_category_name"] = products["product_category_name_english"]
products.drop("product_category_name_english", axis = 1, inplace = True)
products.rename(columns = {"product_name_lenght" : "product_name_length", "product_description_lenght" : "product_description_length"}, inplace = True)
del product_category_name_translation

order_items = df_order_item.join(products.set_index("product_id"), "product_id", validate = "m:1")
order_items.drop("product_id", axis = 1, inplace = True)
del products

order_items = order_items.join(df_sellers.set_index("seller_id"), "seller_id", validate = "m:1")
order_items.drop("seller_id", axis = 1, inplace = True)
del df_sellers

orders = df_orders.join(df_customers.set_index("customer_id"),"customer_id", validate = "1:1")
orders.drop(["customer_id", "customer_unique_id"], axis = 1, inplace = True)
del df_customers

#Null Value Removal
order_items.dropna(axis = 0, how = "any", inplace = True, ignore_index = True)

df_order_review.drop(["review_comment_title", "review_comment_message"], axis = 1, inplace = True)

canceled_orders    = orders[orders["order_status"] == "canceled"]
created_orders     = orders[orders["order_status"] == "created"]
shipped_orders     = orders[orders["order_status"] == "shipped"]
unavailable_orders = orders[orders["order_status"] == "unavailable"]
invoiced_orders    = orders[orders["order_status"] == "invoiced"]
processing_orders  = orders[orders["order_status"] == "processing"]
approved_orders    = orders[orders["order_status"] == "approved"]

orders.drop(orders[orders["order_status"] == "canceled"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "created"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "unavailable"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "invoiced"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "processing"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "shipped"].index, inplace = True)
orders.drop(orders[orders["order_status"] == "approved"].index, inplace = True)

orders.dropna(axis = 0, how = "any", inplace = True, ignore_index = True)
delivered_orders = orders
del orders

approved_orders = pd.concat([approved_orders, unavailable_orders, invoiced_orders, processing_orders], ignore_index = True)
approved_orders.drop(["order_delivered_carrier_date", "order_delivered_customer_date"], axis = 1, inplace = True)
del unavailable_orders, invoiced_orders, processing_orders

created_orders.drop(["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date"], axis = 1, inplace = True)
shipped_orders.drop("order_delivered_customer_date", axis = 1, inplace = True)

delivered = canceled_orders[canceled_orders["order_delivered_customer_date"].notnull()]
shipped   = canceled_orders[(canceled_orders["order_delivered_carrier_date"].notnull()) & (canceled_orders["order_delivered_customer_date"].isnull())]
approved  = canceled_orders[(canceled_orders["order_approved_at"].notnull()) & (canceled_orders["order_delivered_customer_date"].isnull()) & (canceled_orders["order_delivered_carrier_date"].isnull())]
created   = canceled_orders[(canceled_orders["order_approved_at"].isnull()) & (canceled_orders["order_delivered_carrier_date"].isnull()) & (canceled_orders["order_delivered_customer_date"].isnull())]

shipped.drop("order_delivered_customer_date", axis = 1, inplace = True)
approved.drop(["order_delivered_customer_date", "order_delivered_carrier_date"], axis = 1, inplace = True)
created.drop(["order_delivered_customer_date", "order_delivered_carrier_date", "order_approved_at"], axis = 1, inplace = True)

delivered_orders = pd.concat([delivered_orders, delivered], ignore_index = True)
shipped_orders   = pd.concat([shipped_orders, shipped], ignore_index = True)
approved_orders  = pd.concat([approved_orders, approved], ignore_index = True)
created_orders   = pd.concat([created_orders, created], ignore_index = True)

del canceled_orders, delivered, shipped, approved, created

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
    selected = option_menu('Menu',['10122079','10122096', '10122104', '10122105','10122114', '220170203'],
    icons =["easel2", "graph-up"],
    menu_icon="cast",
    default_index=0,
    styles={
        "nav": {"font-family": 'Poppins'},
        "menu-title": {"font-family": 'Poppins', "font-weight": "700"},
        "nav-link-selected": {"font-weight": "700", "background-color": "#dc3545"},
        "icon": {"font-size": "20px"},
        "nav-link": {"--hover-color": "#dc3545"}
    })
    
if (selected == '10122079') :
    st.header(f"Dashboard Analisis E-Commerce oleh Hana")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
    with tab1:
        pertanyaan1_10122096(order_reviews)
        
    with tab2:
        pertanyaan2_10122096(delivered_orders, shipped_orders, approved_orders, order_items)
        
    with tab3:
        pertanyaan3_10122096(df_geolocation_merging)

    with tab4:
        pertanyaan4_10122096(df_geolocation_merging, df_order_review)

elif (selected == '10122096'):
    st.header(f"Dashboard Analisis E-Commerce oleh Mizan")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
elif (selected == '10122104'):
    st.header(f"Dashboard Analisis E-Commerce oleh Cissy")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
elif (selected == '10122105'):
    st.header(f"Dashboard Analisis E-Commerce oleh Amira")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
elif (selected == '10122114'):
    st.header(f"Dashboard Analisis E-Commerce oleh Stefanus")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
elif (selected == '220170203'):
    st.header(f"Dashboard Analisis E-Commerce oleh Desi")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
