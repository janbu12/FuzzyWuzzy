import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sea
pd.options.mode.chained_assignment = None

def satu(items : pd.core.frame.DataFrame):
    # Gathering
    itemsDf = items[["order_id", "freight_value", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]]

    # Cleaning
    itemsDf.drop_duplicates(subset = ["order_id"], keep = "first", inplace = True, ignore_index = True)
    itemsDf.drop(["order_id"], axis = 1, inplace = True)
    itemsDf.insert(2, "product_volume_cm", (itemsDf["product_length_cm"] * itemsDf["product_height_cm"] * itemsDf["product_width_cm"]))
    itemsDf.drop(["product_length_cm", "product_height_cm", "product_width_cm"], axis = 1, inplace = True)
    
    # Data Mining
    correlation = itemsDf.corr("pearson")

    #Visualization
    sea.scatterplot(x = itemsDf["product_volume_cm"], y = itemsDf["freight_value"])
    plt.title("Scatterplot volume dan harga pengiriman barang")
    plt.xlabel("Volume Barang")
    plt.ylabel("Harga Pengiriman Barang")
    Scatter1 = plt.gcf()
    plt.close()

    sea.scatterplot(x = itemsDf["product_weight_g"], y = itemsDf["freight_value"])
    plt.title("Scatterplot berat dan harga pengiriman barang")
    plt.xlabel("Berat Barang")
    plt.ylabel("Harga Pengiriman Barang")
    Scatter2 = plt.gcf()
    plt.close()
    
    # Conclusion
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index          = True)
    st.pyplot(Scatter1)
    st.pyplot(Scatter2)
    st.write("<center>Rata-rata berat barang  : 2108.657148732713")
    st.write("Rata-rata volume barang : 15273.488057169297")
    st.write("Perkiraan harga pengiriman barang : 18.40853503")
    st.write("Rata-rata harga pengiriman barang : 20.025485039001275</center>")

    st.markdown("Dari data yang didapat dari tabel order_items, dapat diketahui bahwa rata-rata berat barang ialah ~2.108,65715 $g$ dan rata-rata volume barang adalah ~15.273,48806 $cm^{3}$ . \
                Dengan menggunakan algoritma pembelajaran mesin regresi kuantil, model akan dilatih dengan seluruh data berat dan volume barang yang ada. \
                Setelah model selesai dilatih, dengan memasukkan rata-rata berat dan volume barang, model regresi dapat memprediksi harga pengiriman barang. \
                Harga yang didapat dari model regresi tersebut ialah ~18,40853, di mana nilai tersebu tidak jauh dari rata-rata harga pengiriman barang yang sudah ada, yakni ~20,02548.")
    
    with st.expander("Kesimpulan"):
        st.write("Kesimpulan dari pertanyaan ini ialah:\
                 <li>Apabila ada suatu barang dengan berat dan volume yang mendekati rata-rata berat dan volume pada data tersebut, harga pengiriman yang harus dibayar berkisar pada 18 - 20 Brazilian Real.\
                 <li>Model regresi hasil proses ini dapat dipakai untuk menentukan harga pengiriman, dikarenakan data prediksi dan data real tidak memiliki perbedaan yang siginfikan.", unsafe_allow_html = True)
    
    # Deletion
    del itemsDf, correlation, Scatter1, Scatter2

def dua(items : pd.core.frame.DataFrame, reviews : pd.core.frame.DataFrame):
    # Gathering
    itemsDf   = items[["order_id", "price", "freight_value"]]
    reviewsDf = reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])

    # Cleaning
    itemsDf.drop_duplicates(["order_id"], keep = "first", inplace = True, ignore_index = True)
    reviewsDf.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    item_review_df = pd.concat([itemsDf, reviewsDf], axis = 1, join = "inner")
    item_review_df = item_review_df.iloc[:, [i for i, x in enumerate(item_review_df.columns) if i != 3]]
    item_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)

    # Data Mining
    correlation = item_review_df.corr()
    price_review_df   = item_review_df.groupby("review_score")["price"].mean()
    freight_review_df = item_review_df.groupby("review_score")["freight_value"].mean()

    # Visualization
    sea.lineplot(x = price_review_df.keys(), y = price_review_df.values)
    sea.lineplot(x = price_review_df.keys(), y = price_review_df.values, style = price_review_df.keys(), markers =["o", "o", "o", "o", "o"], dashes = False)
    plt.title("Korelasi harga barang dan nilai review")
    plt.xlabel("Nilai Review")
    plt.ylabel("Harga Barang")
    Figure1 = plt.gcf()
    plt.close()
    
    sea.lineplot(x = freight_review_df.keys(), y = freight_review_df.values)
    sea.lineplot(x = freight_review_df.keys(), y = freight_review_df.values, style = freight_review_df.keys(), markers =["o", "o", "o", "o", "o"], dashes = False)
    plt.title("Korelasi harga pengiriman barang dan nilai review")
    plt.xlabel("Nilai Review")
    plt.ylabel("Harga Pengiriman Barang")
    Figure2 = plt.gcf()
    plt.close()

    # Conclusion
    st.write('<h4>Berapa kemungkinan harga pengiriman suatu barang yang memiliki berat, panjang, tinggi, dan lebar rata-rata dari seluruh data barang yang sudah ada?</h4>', unsafe_allow_html = True)
    st.dataframe(correlation,
                 use_container_width = True,
                 hide_index          = True)
    st.pyplot(Figure1)
    st.pyplot(Figure2)
    st.markdown('Apabila dilihat dari nilai korelasi antara harga barang dengan nilai review (-0,000007) dan nilai korelasi antara harga pengiriman barang dan nilai review (0,001911), \
                dapat diketahui bahwa harga barang dan harga pengiriman barang hampir tidak memiliki pengaruh sama sekali kepada nilai review. \
                Hal ini dapat dibuktikan juga pada kedua grafik diatas, tidak ada pola signifikan yang dapat menunjukan hubungan antara ketiga variabel.')
    with st.expander("Kesimpulan"):
        st.write("Kesimpulan dari pertanyaan ini ialah:\
                 <li>Harga barang dan harga pengiriman barang tidak memiliki pengaruh yang signifikan terhadap nilai review yang diberikan oleh pengguna.\
                 <li>Harga pengiriman barang (0,001911) memiliki pengaruh yang lebih besar dibandingkan harga barang (-0,000007) kepada nilai review, walaupun hampir tidak memiliki pengaruh.", unsafe_allow_html = True)

    # Deletion
    del itemsDf, reviewsDf, item_review_df, correlation, price_review_df, freight_review_df, Figure1, Figure2

def tiga(items : pd.core.frame.DataFrame, reviews : pd.core.frame.DataFrame):
    # Gathering
    itemsDf   = items[["order_id", "product_category_name"]]
    reviewsDf = reviews[["order_id", "review_score", "review_answer_timestamp"]].sort_values(["order_id", "review_answer_timestamp"])

    # Cleaning
    itemsDf.drop_duplicates(["order_id"], keep = "first", inplace = True, ignore_index = True)
    reviewsDf.drop_duplicates(["order_id"], keep = "last", inplace = True, ignore_index = True)
    item_review_df = pd.concat([itemsDf, reviewsDf], axis = 1, join = "inner")
    item_review_df = item_review_df.iloc[:, [i for i, x in enumerate(item_review_df.columns) if i != 2]]
    item_review_df.drop(["order_id", "review_answer_timestamp"], axis = 1, inplace = True)
    item_review_df.sort_values(["review_score"], ascending = False, inplace = True)

    # Data Mining
    review_score_5 = item_review_df[item_review_df["review_score"] == 5]
    review_score_4 = item_review_df[item_review_df["review_score"] == 4]
    review_score_3 = item_review_df[item_review_df["review_score"] == 3]
    review_score_2 = item_review_df[item_review_df["review_score"] == 2]
    review_score_1 = item_review_df[item_review_df["review_score"] == 1]

    review_score_5 = review_score_5.groupby("product_category_name")["product_category_name"].count().sort_values(ascending = False)
    review_score_4 = review_score_4.groupby("product_category_name")["product_category_name"].count().sort_values(ascending = False)
    review_score_3 = review_score_3.groupby("product_category_name")["product_category_name"].count().sort_values(ascending = False)
    review_score_2 = review_score_2.groupby("product_category_name")["product_category_name"].count().sort_values(ascending = False)
    review_score_1 = review_score_1.groupby("product_category_name")["product_category_name"].count().sort_values(ascending = False)

    review_explode_most  = [0.15, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    review_explode_least = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3]

    # Visualization
    plt.subplot(1, 2, 1)
    plt.pie(review_score_5.head(10).values,
            review_explode_most,
            review_score_5.head(10).keys(),
            sea.color_palette("Blues"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_5.head(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.subplot(1, 2, 2)
    plt.pie(review_score_5.tail(10).values,
            review_explode_least,
            review_score_5.tail(10).keys(),
            sea.color_palette("YlOrBr"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_5.tail(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.suptitle("10 Kategori Dengan Nilai Review 5 Terbanyak (Kiri) dan Tersedikit (Kanan)", y = 0.82)
    Figure1 = plt.gcf()
    plt.close()

    plt.subplot(1, 2, 1)
    plt.pie(review_score_4.head(10).values,
            review_explode_most,
            review_score_4.head(10).keys(),
            sea.color_palette("Blues"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_4.head(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.subplot(1, 2, 2)
    plt.pie(review_score_4.tail(10).values,
            review_explode_least,
            review_score_4.tail(10).keys(),
            sea.color_palette("YlOrBr"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_4.tail(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.suptitle("10 Kategori Dengan Nilai Review 4 Terbanyak (Kiri) dan Tersedikit (Kanan)", y = 0.82)
    Figure2 = plt.gcf()
    plt.close()

    plt.subplot(1, 2, 1)
    plt.pie(review_score_3.head(10).values,
            review_explode_most,
            review_score_3.head(10).keys(),
            sea.color_palette("Blues"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_3.head(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.subplot(1, 2, 2)
    plt.pie(review_score_3.tail(10).values,
            review_explode_least,
            review_score_3.tail(10).keys(),
            sea.color_palette("YlOrBr"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_3.tail(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.suptitle("10 Kategori Dengan Nilai Review 3 Terbanyak (Kiri) dan Tersedikit (Kanan)", y = 0.82)
    Figure3 = plt.gcf()
    plt.close()

    plt.subplot(1, 2, 1)
    plt.pie(review_score_2.head(10).values,
            review_explode_most,
            review_score_2.head(10).keys(),
            sea.color_palette("Blues"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_2.head(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.subplot(1, 2, 2)
    plt.pie(review_score_2.tail(10).values,
            review_explode_least,
            review_score_2.tail(10).keys(),
            sea.color_palette("YlOrBr"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_2.tail(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.suptitle("10 Kategori Dengan Nilai Review 2 Terbanyak (Kiri) dan Tersedikit (Kanan)", y = 0.82)
    Figure4 = plt.gcf()
    plt.close()

    plt.subplot(1, 2, 1)
    plt.pie(review_score_1.head(10).values,
            review_explode_most,
            review_score_1.head(10).keys(),
            sea.color_palette("Blues"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_1.head(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.subplot(1, 2, 2)
    plt.pie(review_score_1.tail(10).values,
            review_explode_least,
            review_score_1.tail(10).keys(),
            sea.color_palette("YlOrBr"),
            autopct = "%1.1f%%",
            pctdistance = 1.25,
            labeldistance = None,
            shadow = True,
            radius = 1.05)
    plt.legend(review_score_1.tail(10).keys(),
               title = "Product Categories",
               loc =  "center left",
               bbox_to_anchor = (0, -1.1, 0.5, 1))

    plt.suptitle("10 Kategori Dengan Nilai Review 1 Terbanyak (Kiri) dan Tersedikit (Kanan)", y = 0.82)
    Figure5 = plt.gcf()
    plt.close()

    # Conclusion
    st.write("<h4>Bagaimana persebaran kategori barang pada setiap nilai review?</h4>", unsafe_allow_html = True)
    st.pyplot(Figure1)
    st.markdown("Pada grafik, dapat terlihat bahwa kategori tempat tidur, kamar mandi, dan meja merupakan kategori produk yang memiliki nilai review 5 terbanyak, \
                sedangkan kategori layanan dan keamanan merupakan kategori dengan nilai review 5 tersedikit.")
    st.pyplot(Figure2)
    st.markdown("Pada grafik, dapat terlihat bahwa kategori tempat tidur, kamar mandi, dan meja merupakan kategori produk yang memiliki nilai review 4 terbanyak, \
                sedangkan kategori kenyamanan rumah merupakan kategori dengan nilai review 4 tersedikit.")
    st.pyplot(Figure3)
    st.markdown("Pada grafik, dapat terlihat bahwa kategori tempat tidur, kamar mandi, dan meja merupakan kategori produk yang memiliki nilai review 3 terbanyak, \
                sedangkan kategori seni dan keahlian merupakan kategori dengan nilai review 3 tersedikit.")
    st.pyplot(Figure4)
    st.markdown("Pada grafik, dapat terlihat bahwa kategori kesehatan dan kecantikan merupakan kategori produk yang memiliki nilai review 2 terbanyak, \
                sedangkan kategori mode dan olahraga merupakan kategori dengan nilai review 2 tersedikit.")
    st.pyplot(Figure5)
    st.markdown("Pada grafik, dapat terlihat bahwa kategori kesehatan dan kecantikan merupakan kategori produk yang memiliki nilai review 1 terbanyak, \
                sedangkan kategori masakan merupakan kategori dengan nilai review 1 tersedikit.")
    with st.expander("Kesimpulan"):
        st.write("Kesimpulan dari pertanyaan ini ialah:\
                 <li>Kategori tempat tidur, kamar mandi, dan meja serta kategori kesehatan dan kecantikan merupakan kategori yang memiliki banyak data dalam setiap nilai review, sehingga ada kemungkinan bahwa kedua kategori ini merupakan kategori yang banyak dibeli.\
                 <li>Penjualan barang dengan kategori tempat tidur, kamar mandi, dan meja kemungkinan memiliki standar yang tinggi dikarenakan banyaknya jumlah data yang memiliki nilai review 3 keatas.\
                 <li>Penjualan barang dengan kategori kesehatan dan kecantikan kemungkinan memiliki standar yang rendah dikarenakan banyaknya jumlah data yang memiliki nilai review 1 dan 2.\
                 <li>Kategori layanan dan keamanan, kenyamanan rumah, seni dan keahlian, mode dan olahraga, serta masakan merupakan kategori-kategori dengan jumlah nilai review yang sedikit, sehingga ada kemungkinan bahwa kategori-kategori ini tidak terlalu banyak dibeli.", unsafe_allow_html = True)
    
    # Deletion
    del itemsDf, reviewsDf, item_review_df, review_score_5, review_score_4, review_score_3, review_score_2, review_score_1, review_explode_most, review_explode_least, Figure1, Figure2, Figure3, Figure4, Figure5
