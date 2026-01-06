import streamlit as st
import numpy as np

# Rapor Başlığı: Mutfaktaki Görünmez İsrafın İzinde
st.set_page_config(page_title="Mutfak Karar Destek", layout="centered")

# CSS ile Görsel Sabitleme (Beyaz kutu sorununu önlemek için)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1, h2, h3, p, label { color: black !important; font-weight: bold !important; }
    .stSelectbox, .stButton { border: 2px solid black !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍽️ Mutfaktaki Görünmez İsrafın İzinde")
st.write("### Akıllı Porsiyon Karar Destek Sistemi")

# Model Başlangıç Ağırlıkları (Dinamik Karar Ağacı Mantığı [cite: 54])
if 'weights' not in st.session_state:
    st.session_state.weights = np.array([300.0, 50.0, 15.0])

st.divider()

# --- BAĞIMSIZ DEĞİŞKENLER [cite: 46] ---
st.write("### 📋 1. Adım: Veri Girişi")

kisi = st.selectbox("👤 Kaç Kişi Yemek Yiyecek?", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=3)
ogun = st.selectbox("🕒 Hangi Öğün Hazırlanıyor?", ["Kahvaltı", "Öğle", "Akşam"])
mevsim = st.selectbox("🍂 Mevsim Etkisi Nedir?", ["Kış", "İlkbahar", "Yaz", "Sonbahar"])
dunden_kalan = st.selectbox("🥘 Dünden Kalan Yemek (Porsiyon)", [0.0, 0.5, 1.0, 1.5, 2.0], index=0)

# --- ALGORİTMİK TAHMİN ---
ogun_map = {"Kahvaltı": 1, "Öğle": 2, "Akşam": 3}
mevsim_map = {"Kış": 1, "İlkbahar": 2, "Yaz": 3, "Sonbahar": 4}
state = np.array([kisi, ogun_map[ogun], mevsim_map[mevsim]])

# Ağırlık Katsayıları ile Hesaplama [cite: 55]
tahmin_baz = np.dot(state, st.session_state.weights)

# "Tasarruf" Değeri Kapsamında Baskılama Etkisi [cite: 147, 149]
if dunden_kalan > 0:
    tahmin_final = tahmin_baz * 0.80 
    st.error(f"⚠️ DÜNDEN KALAN YEMEK NEDENİYLE %20 TASARRUF BASKILAMASI UYGULANDI! [cite: 148]")
else:
    tahmin_final = tahmin_baz

st.write(f"## ✅ ÖNERİLEN MİKTAR: {int(tahmin_final)} gram")

# --- GERİ BİLDİRİM VE ÖĞRENME (Aşama 3 [cite: 62]) ---
st.divider()
st.write("### 🔄 2. Adım: Geri Bildirim")
gercek = st.selectbox("Gerçek tüketim ne kadar oldu?", list(range(0, 4100, 100)), index=int(tahmin_final//100))

if st.button("SİSTEMİ GÜNCELLE VE EĞİT"):
    hata = tahmin_final - float(gercek)
    # Katsayıların güncellenmesi (Geri besleme döngüsü [cite: 62])
    st.session_state.weights -= 0.03 * hata * (state / np.max(state))
    st.success("H3 HİPOTEZİ: Model güncellendi, israf bilinci kaydedildi! [cite: 40]")
    st.balloons()
