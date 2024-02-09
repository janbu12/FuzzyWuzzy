import streamlit as st
from streamlit_option_menu import option_menu

# Import Pertanyaan
from Mizan import *
from Stefanus import *
from Cissy import *

@st.cache_data
def load_data(url) :
    df = pd.read_csv(url)
    return df

# Karena data terlalu besar untuk dicleaning & merging, jadi dibuat csv yang sudah dicleaningnya untuk membatasi limit ram usage
order_reviews          = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_reviews.csv")
delivered_orders       = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/delivered_orders.csv")
shipped_orders         = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/shipped_orders.csv")
approved_orders        = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/approved_orders.csv")
order_items            = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_items.csv")
df_geolocation_merging = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/Geolocation_merging.csv")

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
    selected = option_menu('NIM',
                           ['10122079', '10122096', '10122104', '10122105', '10122114', '220170203'],
                           icons = ["person-circle", "person-workspace", "person-badge-fill", "person-circle", "person-workspace", "person-badge-fill"],
                           menu_icon = "person-lines-fill",
                           default_index = 0,
                           styles={"nav" : {"font-family" : 'Poppins'},
                                   "menu-title" : {"font-family" : 'Poppins', "font-weight" : "700"},
                                   "nav-link-selected" : {"font-weight" : "700", "background-color" : "#dc3545"},
                                   "icon" : {"font-size" : "20px"},
                                   "nav-link" : {"--hover-color" : "#dc3545"}})
    
if (selected == '10122079') :
    st.header(f"Dashboard Analisis E-Commerce oleh Hana")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
elif (selected == '10122096'):
    st.header(f"Dashboard Analisis E-Commerce oleh Mizan")
    tab1 ,tab2, tab3, tab4 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4"])

    with tab1:
        #Dibutuhkan untuk mengambil data review title dan messagenya
        order_reviews_notClean = load_data("https://raw.githubusercontent.com/janbu12/FuzzyWuzzy/main/dataset/order_reviews_dataset.csv")
        pertanyaan1_10122096(order_reviews_notClean)
        del order_reviews_notClean
        
    with tab2:
        pertanyaan2_10122096(delivered_orders, shipped_orders, approved_orders, order_items)
        
    with tab3:
        pertanyaan3_10122096(df_geolocation_merging)

    with tab4:
        pertanyaan4_10122096(df_geolocation_merging, order_reviews)
        
elif (selected == '10122104'):
    st.header(f"Dashboard Analisis E-Commerce oleh Dyandra Cissy")
    tab1, tab2 = st.tabs(["Pertanyaan 1", "Pertanyaan 2"])
    
elif (selected == '10122105'):
    st.header(f"Dashboard Analisis E-Commerce oleh Amira")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
elif (selected == '10122114'):
    st.header(f"Dashboard Analisis E-Commerce oleh Stefanus Gratilio")
    tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3"])

    with tab1:
        satu(order_items)

    with tab2:
        dua(order_items, order_reviews)

    with tab3:
        tiga(order_items, order_reviews)
    
elif (selected == '220170203'):
    st.header(f"Dashboard Analisis E-Commerce oleh Desi")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4", "Pertanyaan 5"])
    
