import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Supabase Bağlantısı
SUPABASE_URL = "https://gbdrcqqccflukduzvsse.supabase.co"  # Supabase'den aldığın URL adresi
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdiZHJjcXFjY2ZsdWtkdXp2c3NlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAwODUwODksImV4cCI6MjEwNTY2MTA4OX0.Y2AxkqdHzofkOY3qwgOCTGWyV263UWHJGrA19fL-0hk"       


# Supabase Bağlantısını Başlat
@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="ASDİM İmalat Takip", layout="wide")
st.title("🏗️ ASDİM İMALAT TAKİP SİSTEMİ")

menu = st.sidebar.radio("Menü Seçimi", ["📋 İmalat Listesi", "➕ Yeni Sipariş / Föy Ekle"])

DURUM_LISTESI = [
    "İmalata Alınacak",
    "İmalattaki Kabinler",
    "Sevke Hazır",
    "Sevk Edilen",
    "Onay Bekleyenler",
    "İptal Olanlar"
]

# --- 3. İMALAT LİSTESİ ---
if menu == "📋 İmalat Listesi":
    st.subheader("Mevcut İmalat Takip Listesi")
    
    # Verileri Çek
    response = supabase.table("imalat_takip").select("*").execute()
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        
        durum_filtre = st.multiselect("Duruma Göre Filtrele", DURUM_LISTESI, default=DURUM_LISTESI)
        filtered_df = df[df['durum'].isin(durum_filtre)]
        
        st.dataframe(
            filtered_df[[
                'foy_no', 'firma_adi', 'referans', 'durum', 'siparis_tarihi', 
                'teslimat_tarihi', 'genislik', 'derinlik', 'kaplama_tipi', 
                'tavan', 'taban', 'aciklama'
            ]],
            use_container_width=True
        )
    else:
        st.info("Henüz kayıtlı bir sipariş bulunmuyor.")

# --- 4. YENİ SİPARİŞ EKLE ---
elif menu == "➕ Yeni Sipariş / Föy Ekle":
    st.subheader("Yeni Sipariş / İmalat Föyü Kaydı")
    
    with st.form("siparis_formu"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📌 Sipariş Genel Bilgileri")
            foy_no = st.number_input("Föy No", min_value=1, step=1)
            firma_adi = st.text_input("Firma Adı")
            referans = st.text_input("Referans")
            siparis_tarihi = st.date_input("Sipariş Tarihi")
            teslimat_tarihi = st.date_input("Teslimat Tarihi")
            durum = st.selectbox("Başlangıç Durumu", DURUM_LISTESI)

        with col2:
            st.markdown("### 🚪 Kabin Detayları")
            genislik = st.number_input("Genişlik (mm)", step=10)
            derinlik = st.number_input("Derinlik (mm)", step=10)
            kaplama_tipi = st.text_input("Kaplama Tipi")
            ana_desen = st.text_input("Ana Desen")
            aksesuar = st.text_input("Aksesuar")
            kupeste_adedi = st.number_input("Küpeşte Adedi", min_value=0, step=1)

        with col3:
            st.markdown("### ⚙️ Süspansiyon & Aksam")
            taban = st.text_input("Taban")
            tavan = st.text_input("Tavan")
            kaset = st.text_input("Kaset")
            ayna = st.text_input("Ayna")
            calisma_sekli = st.text_input("Çalışma Şekli")
            aciklama = st.text_area("Açıklama / Notlar")

        submit = st.form_submit_button("💾 Siparişi Kaydet")
        
        if submit:
            yeni_kayit = {
                "foy_no": int(foy_no),
                "firma_adi": firma_adi,
                "referans": referans,
                "siparis_tarihi": str(siparis_tarihi),
                "teslimat_tarihi": str(teslimat_tarihi),
                "durum": durum,
                "genislik": int(genislik),
                "derinlik": int(derinlik),
                "kaplama_tipi": kaplama_tipi,
                "ana_desen": ana_desen,
                "aksesuar": aksisuar if 'aksisuar' in locals() else aksesuar,
                "kupeste_adedi": int(kupeste_adedi),
                "taban": taban,
                "tavan": tavan,
                "kaset": kaset,
                "ayna": ayna,
                "calisma_sekli": calisma_sekli,
                "aciklama": aciklama
            }
            supabase.table("imalat_takip").insert(yeni_kayit).execute()
            st.success(f"Föy No {foy_no} başarıyla bulut veritabanına kaydedildi!")