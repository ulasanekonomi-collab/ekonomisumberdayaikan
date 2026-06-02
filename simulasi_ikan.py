import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Simulasi Ekonomi Perikanan", layout="wide")
st.title("Simulasi Ekonomi Sumber Daya Ikan (Bioeconomics)")
st.write("Dibangun berdasarkan Model Gordon-Schaefer")

# --- PANEL INPUT DI SIDEBAR ---
st.sidebar.header("Parameter Biologi")
r = st.sidebar.slider("Laju Pertumbuhan Intrinsik (r)", 0.1, 1.0, 0.5, step=0.05)
K = st.sidebar.slider("Daya Dukung Lingkungan (K)", 1000, 10000, 5000, step=500)
q = st.sidebar.slider("Koefisien Tangkap (q)", 0.001, 0.05, 0.01, step=0.001)

st.sidebar.header("Parameter Ekonomi")
p = st.sidebar.slider("Harga Jual Ikan (p)", 10, 200, 100, step=10)
c = st.sidebar.slider("Biaya per Unit Effort (c)", 100, 2000, 500, step=100)

# --- PERHITUNGAN MATEMATIS ---
# Menghindari error jika biaya terlalu tinggi sehingga perikanan tidak layak
if c >= p * q * K:
    st.error("Biaya operasional terlalu tinggi dibandingkan potensi pendapatan (c >= pqK). Perikanan tidak layak secara ekonomi.")
else:
    # Titik Kritis Effort (E)
    E_MSY = r / (2 * q)
    E_OAE = (r / q) * (1 - (c / (p * q * K)))
    E_MEY = E_OAE / 2

    # Membuat rentang Effort (E) untuk sumbu X grafik
    E_max = E_OAE * 1.2 # Lebihkan sedikit dari OAE untuk visualisasi
    E = np.linspace(0, E_max, 200)

    # Persamaan Kurva
    Yield = q * E * K * (1 - (q * E) / r)
    TR = p * Yield
    TC = c * E

# --- MEMBUAT TAB UNTUK SKENARIO ---
    tab1, tab2 = st.tabs(["1. Simulasi Gordon-Schaefer (Biologi)", "2. Simulasi Bioeconomics (Ekonomi)"])

    # ==========================================
    # TAB 1: GORDON-SCHAEFER
    # ==========================================
    with tab1:
        st.subheader("Kurva Sustainable Yield")
        
        # Petunjuk Pembelajaran Tab 1
        with st.expander("📖 Petunjuk Pembelajaran & Eksperimen (Klik untuk membuka)", expanded=False):
            st.markdown("""
            **Tujuan:** Menganalisis interaksi antara tingkat eksploitasi dan daya dukung lingkungan, serta memahami konsep batas kelestarian alam.
            
            **Langkah Eksperimen:**
            1. **Baseline:** Biarkan *slider* pada nilai awal. Puncak parabola adalah **MSY** (batas maksimal alam menyediakan sumber daya secara lestari).
            2. **Simulasi Kerusakan Lingkungan:** Geser *slider* **Daya Dukung Lingkungan (K)** ke kiri (turun). Amati apa yang terjadi pada tinggi dan lebar kurva jika habitat laut rusak.
            3. **Karakteristik Spesies:** Geser *slider* **Laju Pertumbuhan (r)** untuk membandingkan ikan umur panjang (r kecil) vs pelagis kecil (r besar). Mana yang lebih rentan terhadap overfishing?
            4. **Biological Overfishing:** Perhatikan area di sebelah kanan garis merah (MSY). Mengapa menambah jaring (effort) di area ini justru menurunkan hasil tangkapan?
            """)
            
        # Plot Grafik Tab 1
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(E, Yield, label="Sustainable Yield (h)", color="green", linewidth=2)
        ax1.axvline(x=E_MSY, color="red", linestyle="--", label=f"MSY (E={E_MSY:.1f})")
        
        ax1.set_xlabel("Upaya Penangkapan / Effort (E)")
        ax1.set_ylabel("Hasil Tangkapan / Catch (h)")
        ax1.set_title("Hubungan Upaya Penangkapan dan Kelestarian")
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig1)
        
        st.info("Di sini terlihat bahwa tangkapan maksimal (MSY) dicapai pada titik tertentu. Menambah *effort* melampaui garis merah justru akan menurunkan hasil tangkapan karena populasi ikan gagal bereproduksi dengan cukup.")
# --- TAMBAHAN KATA KUNCI TAB 1 ---
        with st.expander("📌 Kata Kunci & Bahan Kajian Kelompok (Ekologi)"):
            st.markdown("""
            **Diskusikan konsep berikut berdasarkan pergerakan kurva:**
            *   **Carrying Capacity ($K$):** Apa dampaknya pada kurva jika habitat laut rusak sehingga nilai $K$ anjlok?
            *   **Biological Overfishing:** Di rentang *effort* mana populasi ikan mulai kehilangan kemampuan pemulihan alaminya?
            *   **Laju Pertumbuhan ($r$):** Bandingkan ikan berumur panjang (pertumbuhan lambat) vs ikan pelagis kecil. Mana yang lebih rentan terhadap intensitas penangkapan?
            *   **Titik Kritis MSY:** Mengapa mengejar hasil tangkapan fisik maksimal secara terus-menerus sering kali dianggap berisiko tinggi?
            """)
            
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        # ... [kode plot fig1 dan ax1 dilanjutkan di bawah sini] ...
    
    with tab2:
        st.subheader("Kurva Total Revenue (TR) dan Total Cost (TC)")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(E, TR, label="Total Revenue (TR)", color="blue", linewidth=2)
        ax2.plot(E, TC, label="Total Cost (TC)", color="orange", linewidth=2)
        
        # Plot Titik Kritis
        ax2.axvline(x=E_MEY, color="green", linestyle=":", label=f"MEY (E={E_MEY:.1f})")
        ax2.axvline(x=E_MSY, color="red", linestyle=":", label=f"MSY (E={E_MSY:.1f})")
        ax2.axvline(x=E_OAE, color="black", linestyle=":", label=f"OAE (E={E_OAE:.1f})")
        
        ax2.set_xlabel("Upaya Penangkapan / Effort (E)")
        ax2.set_ylabel("Nilai Moneter")
        ax2.set_title("Analisis Kebijakan Ekonomi Perikanan")
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig2)
        
        # Tabel Ringkasan
        st.markdown("### Ringkasan Titik Keseimbangan")
        st.write(f"- **MEY (Maximum Economic Yield):** Dicapai pada effort **{E_MEY:.2f}**. Jarak TR dan TC paling lebar (keuntungan maksimal). Ideal untuk kemitraan dengan alam.")
        st.write(f"- **MSY (Maximum Sustainable Yield):** Dicapai pada effort **{E_MSY:.2f}**. Pendapatan kotor tertinggi, tapi keuntungan bersih sudah menurun.")
        st.write(f"- **OAE (Open Access Equilibrium):** Dicapai pada effort **{E_OAE:.2f}**. TR = TC, keuntungan bersih habis (Tragedy of the Commons).")

# --- TAMBAHAN KATA KUNCI TAB 2 ---
        with st.expander("📌 Kata Kunci & Bahan Kajian Kelompok (Ekonomi & Kebijakan)"):
            st.markdown("""
            **Gunakan parameter di sebelah kiri untuk menjawab isu kebijakan berikut:**
            *   **Tragedy of the Commons:** Mengapa kondisi akses terbuka (OAE) membuat keuntungan ekonomi nelayan habis sama sekali ($TR = TC$)?
            *   **Efisiensi MEY vs MSY:** Secara matematis dan grafis, mengapa titik keuntungan ekonomi maksimal (MEY) **selalu** berada pada tingkat *effort* yang lebih rendah dibanding MSY?
            *   **Rente Ekonomi (Resource Rent):** Pada titik MEY, terdapat surplus (selisih besar antara TR dan TC). Menurut kelompok Anda, siapa yang berhak menikmati surplus ini?
            *   **Dampak Subsidi:** Geser *slider* Biaya (c) ke kiri (simulasi subsidi BBM). Apa dampaknya terhadap pergeseran titik OAE dan kelestarian stok ikan?
            """)
            
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        # ... [kode plot fig2 dan ax2 dilanjutkan di bawah sini] ...
# --- FOOTER / KREDIT ---
st.sidebar.markdown("---") 

# 1. Menampilkan Logo Unisba (dibuat ukurannya pas, tidak terlalu lebar)
try:
    st.sidebar.image("logounisba.png", width=90) 
except:
    pass

# 2. Membagi ruang menjadi dua kolom (rasio 1 untuk foto, 2.5 untuk teks)
col_foto, col_teks = st.sidebar.columns([1, 2.5])

with col_foto:
    try:
        # Pastikan nama filenya sesuai dengan yang di-upload di GitHub ya Kang 
        st.image("yuka.png", use_container_width=True)
    except:
        pass

with col_teks:
    # Menggunakan line-height agar jarak antar baris lebih rapat dan rapi
    st.markdown(
        """
        <div style="font-size: 11px; color: #666; line-height: 1.4; margin-top: 2px;">
            Dikembangkan oleh:<br>
            <b>Yuhka Sundaya</b><br>
            Ekonomi Pembangunan<br>
            Unisba, 2026
        </div>
        """, 
        unsafe_allow_html=True
    )
