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

df_order_item = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_items_dataset.csv")
df_order_review = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_reviews_dataset.csv")
order_reviews = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_reviews_dataset.csv")
df_orders = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/orders_dataset.csv")
df_sellers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/sellers_dataset.csv")
df_customers = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/customers_dataset.csv")
#karena data terlalu besar untuk dicleaning & merging, jadi dibuat csv yang sudah dicleaningnya untuk membatasi limit ram usage
df_geolocation_merging = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/Geolocation_merging.csv")
products = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/products_dataset.csv")
product_category_name_translation = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/product_category_name_translation.csv")

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
    icons =["person-circle","person-workspace","person-badge-fill", "person-circle","person-workspace","person-badge-fill"],
    menu_icon="person-lines-fill",
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
    
elif (selected == '10122096'):
    st.header(f"Dashboard Analisis E-Commerce oleh Mizan")
    tab1,tab2,tab3,tab4= st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4"])

    with tab1:
        pertanyaan1_10122096(order_reviews)
        
    with tab2:
        pertanyaan2_10122096(delivered_orders, shipped_orders, approved_orders, order_items)
        
    with tab3:
        pertanyaan3_10122096(df_geolocation_merging)

    with tab4:
        pertanyaan4_10122096(df_geolocation_merging, df_order_review)
        
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
    
