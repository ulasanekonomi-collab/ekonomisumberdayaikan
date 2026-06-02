import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# Konfigurasi Halaman
st.set_page_config(page_title="Simulasi Ekonomi Perikanan", layout="wide")
st.title("Simulasi Ekonomi Sumber Daya Ikan (Bioeconomics)")
st.write("Dibangun berdasarkan Model Gordon-Schaefer")

# Fungsi Pembantu untuk Mengubah Grafik Menjadi Base64 (Agar bisa dimasukkan ke file unduhan)
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# --- PANEL INPUT DI SIDEBAR ---
st.sidebar.header("Parameter Biologi")
r = st.sidebar.slider("Laju Pertumbuhan Intrinsik (r)", 0.1, 1.0, 0.5, step=0.05)
K = st.sidebar.slider("Daya Dukung Lingkungan (K)", 1000, 10000, 5000, step=500)
q = st.sidebar.slider("Koefisien Tangkap (q)", 0.001, 0.05, 0.01, step=0.001)

st.sidebar.header("Parameter Ekonomi")
p = st.sidebar.slider("Harga Jual Ikan (p)", 10, 200, 100, step=10)
c = st.sidebar.slider("Biaya per Unit Effort (c)", 100, 2000, 500, step=100)

# --- PERHITUNGAN MATEMATIS ---
if c >= p * q * K:
    st.error("Biaya operasional terlalu tinggi dibandingkan potensi pendapatan (c >= pqK). Perikanan tidak layak secara ekonomi.")
else:
    # Titik Kritis Effort (E)
    E_MSY = r / (2 * q)
    E_OAE = (r / q) * (1 - (c / (p * q * K)))
    E_MEY = E_OAE / 2

    # Membuat rentang Effort (E) untuk sumbu X grafik
    E_max = E_OAE * 1.2 if E_OAE > 0 else E_MSY * 2
    E = np.linspace(0, E_max, 200)

    # Persamaan Kurva
    Yield = q * E * K * (1 - (q * E) / r)
    TR = p * Yield
    TC = c * E

    # Nilai Hasil Tangkapan pada Titik Kritis
    Y_MSY = q * E_MSY * K * (1 - (q * E_MSY) / r)
    Y_MEY = q * E_MEY * K * (1 - (q * E_MEY) / r)

    # --- MEMBUAT TAB UNTUK SKENARIO ---
    tab1, tab2 = st.tabs(["1. Simulasi Gordon-Schaefer (Biologi)", "2. Simulasi Bioeconomics (Ekonomi)"])

    # ==========================================
    # TAB 1: GORDON-SCHAEFER (BIOLOGI)
    # ==========================================
    with tab1:
        st.subheader("Kurva Sustainable Yield")
        
        with st.expander("📖 Petunjuk Pembelajaran & Eksperimen (Klik untuk membuka)", expanded=False):
            st.markdown("""
            **Tujuan:** Menganalisis interaksi antara tingkat eksploitasi dan daya dukung lingkungan, serta memahami konsep batas kelestarian alam.
            
            **Langkah Eksperimen:**
            1. **Baseline:** Biarkan *slider* pada nilai awal. Puncak parabola adalah **MSY** (batas maksimal alam menyediakan sumber daya secara lestari).
            2. **Simulasi Kerusakan Lingkungan:** Geser *slider* **Daya Dukung Lingkungan (K)** ke kiri (turun). Amati apa yang terjadi pada tinggi dan lebar kurva jika habitat laut rusak.
            3. **Karakteristik Spesies:** Geser *slider* **Laju Pertumbuhan (r)** untuk membandingkan ikan umur panjang (r kecil) vs pelagis kecil (r besar). Mana yang lebih rentan terhadap overfishing?
            4. **Biological Overfishing:** Perhatikan area di sebelah kanan garis merah (MSY). Mengapa menambah jaring (effort) di area ini justru menurunkan hasil tangkapan?
            """)
            
        fig1, ax1 = plt.subplots(figsize=(10, 4.5))
        ax1.plot(E, Yield, label="Sustainable Yield (h)", color="green", linewidth=2)
        ax1.axvline(x=E_MSY, color="red", linestyle="--", label=f"MSY (E={E_MSY:.1f})")
        ax1.set_xlabel("Upaya Penangkapan / Effort (E)")
        ax1.set_ylabel("Hasil Tangkapan / Catch (h)")
        ax1.set_title("Hubungan Upaya Penangkapan dan Kelestarian")
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig1)

        # Tombol Unduh Laporan Tab 1
        img_b64_1 = fig_to_base64(fig1)
        html_report_1 = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 30px; color: #333; line-height: 1.6; }}
                .header {{ text-align: center; border-bottom: 2px solid #2e7d32; padding-bottom: 10px; margin-bottom: 20px; }}
                .title {{ font-size: 22px; font-weight: bold; color: #2e7d32; }}
                .subtitle {{ font-size: 13px; color: #666; }}
                .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .meta-table th, .meta-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 13px; }}
                .meta-table th {{ background-color: #f2f2f2; }}
                .chart-box {{ text-align: center; margin: 20px 0; }}
                .analysis {{ background-color: #f9f9f9; padding: 15px; border-left: 5px solid #2e7d32; border-radius: 4px; }}
                .footer {{ text-align: center; font-size: 11px; color: #888; margin-top: 40px; border-top: 1px solid #ddd; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">LAPORAN SIMULASI MODEL GORDON-SCHAEFER (BIOLOGI)</div>
                <div class="subtitle">Laboratorium Analisis Kebijakan Ekonomi Pembangunan UNISBA (2026)</div>
            </div>
            
            <h3>1. Parameter Eksperimen</h3>
            <table class="meta-table">
                <tr><th>Parameter</th><th>Nilai</th><th>Keterangan</th></tr>
                <tr><td>Laju Growth Intrinsik (r)</td><td>{r}</td><td>Kecepatan reproduksi alami stok ikan</td></tr>
                <tr><td>Carrying Capacity (K)</td><td>{K}</td><td>Batas daya dukung maksimum lingkungan habitat</td></tr>
                <tr><td>Catchability Coefficient (q)</td><td>{q}</td><td>Efisiensi alat tangkap per unit effort</td></tr>
            </table>

            <h3>2. Grafik Sustainable Yield Curve</h3>
            <div class="chart-box">
                <img src="data:image/png;base64,{img_b64_1}" style="max-width:100%; height:auto;">
            </div>

            <h3>3. Analisis Hasil Simulasi</h3>
            <div class="analysis">
                <ul>
                    <li><b>Maximum Sustainable Yield (MSY):</b> Titik tangkapan fisik maksimal tercapai pada tingkat <i>effort</i> sebesar <b>{E_MSY:.2f}</b> unit penangkapan, dengan volume tangkapan lestari maksimal sebesar <b>{Y_MSY:.2f}</b> unit biomassa.</li>
                    <li><b>Biological Overfishing Zone:</b> Jika mahasiswa atau pengambil kebijakan mendorong tingkat eksploitasi/<i>effort</i> melebihi <b>{E_MSY:.2f}</b>, maka hasil tangkapan jangka panjang dipastikan akan <b>menurun</b> akibat menipisnya stok induk ikan di alam.</li>
                </ul>
            </div>
            
            <div class="footer">
                Dikembangkan oleh Yuhka Sundaya, Ekonomi Pembangunan Unisba, 2026.<br>
                <i>Gunakan menu cetak browser (Ctrl+P / Cmd+P) untuk menyimpan dokumen ini sebagai file PDF resmi.</i>
            </div>
        </body>
        </html>
        """
        st.download_button(
            label="📥 Unduh Grafik & Analisis Biologi (HTML/PDF)",
            data=html_report_1,
            file_name="Laporan_Simulasi_Biologi_Ikan.html",
            mime="text/html"
        )

    # ==========================================
    # TAB 2: BIOECONOMICS (EKONOMI)
    # ==========================================
    with tab2:
        st.subheader("Kurva Total Revenue (TR) dan Total Cost (TC)")
        
        with st.expander("📖 Petunjuk Pembelajaran & Eksperimen (Klik untuk membuka)", expanded=False):
            st.markdown("""
            **Tujuan:** Mengintegrasikan variabel pasar (harga dan biaya) dengan kondisi ekologis untuk merumuskan kebijakan yang rasional.
            
            **Langkah Eksperimen:**
            1. **Identifikasi Rezim:** Temukan 3 titik kritis: **MEY** (Keuntungan Maksimal), **MSY** (Tangkapan Maksimal), dan **OAE** (Akses Terbuka/Keuntungan Nol).
            2. **Tragedy of the Commons:** Perhatikan titik hitam **OAE**. Jika tanpa aturan, mengapa nelayan terus menambah kapal hingga mencapai titik ini meski laut sudah rusak dan keuntungan habis (TR = TC)?
            3. **Simulasi Subsidi BBM:** Geser *slider* **Biaya (c)** ke kiri (lebih murah). Ke arah mana titik OAE bergeser? Apakah subsidi mempercepat overfishing?
            4. **Kemitraan dengan Alam:** Titik hijau (MEY) selalu di sebelah kiri MSY. Mengapa mengejar nilai ekonomi (MEY) terbukti lebih "ramah lingkungan" daripada mengejar volume fisik (MSY)? Instrumen kebijakan apa yang bisa menahan nelayan di titik MEY?
            """)
            
        fig2, ax2 = plt.subplots(figsize=(10, 4.5))
        ax2.plot(E, TR, label="Total Revenue (TR)", color="blue", linewidth=2)
        ax2.plot(E, TC, label="Total Cost (TC)", color="orange", linewidth=2)
        
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
        st.write(f"- **MEY (Maximum Economic Yield):** Effort **{E_MEY:.2f}**. Jarak TR dan TC paling lebar (keuntungan maksimal). Ideal untuk kelestarian.")
        st.write(f"- **MSY (Maximum Sustainable Yield):** Effort **{E_MSY:.2f}**. Pendapatan kotor tertinggi, tapi stok ikan mulai tertekan.")
        st.write(f"- **OAE (Open Access Equilibrium):** Effort **{E_OAE:.2f}**. TR = TC, keuntungan bersih habis (Tragedy of the Commons).")

        # Tombol Unduh Laporan Tab 2
        img_b64_2 = fig_to_base64(fig2)
        html_report_2 = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 30px; color: #333; line-height: 1.6; }}
                .header {{ text-align: center; border-bottom: 2px solid #1a5f7a; padding-bottom: 10px; margin-bottom: 20px; }}
                .title {{ font-size: 22px; font-weight: bold; color: #1a5f7a; }}
                .subtitle {{ font-size: 13px; color: #666; }}
                .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .meta-table th, .meta-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 13px; }}
                .meta-table th {{ background-color: #f2f2f2; }}
                .chart-box {{ text-align: center; margin: 20px 0; }}
                .analysis {{ background-color: #f4f9f4; padding: 15px; border-left: 5px solid #1a5f7a; border-radius: 4px; }}
                .footer {{ text-align: center; font-size: 11px; color: #888; margin-top: 40px; border-top: 1px solid #ddd; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">LAPORAN ANALISIS BIOEKONOMI PERIKANAN</div>
                <div class="subtitle">Laboratorium Analisis Kebijakan Ekonomi Pembangunan UNISBA (2026)</div>
            </div>
            
            <h3>1. Parameter Eksperimen Kebijakan</h3>
            <table class="meta-table">
                <tr><th>Parameter</th><th>Nilai</th><th>Keterangan</th></tr>
                <tr><td>Harga Jual Ikan (p)</td><td>Rp {p}</td><td>Harga pasar per satuan berat biomassa ikan</td></tr>
                <tr><td>Biaya per Unit Effort (c)</td><td>Rp {c}</td><td>Biaya operasional melaut per unit kapal/jaring</td></tr>
                <tr><td>Kombinasi Ekologi (r, K, q)</td><td>{r}, {K}, {q}</td><td>Kondisi biologis bawaan perairan</td></tr>
            </table>

            <h3>2. Grafik Analisis TR dan TC</h3>
            <div class="chart-box">
                <img src="data:image/png;base64,{img_b64_2}" style="max-width:100%; height:auto;">
            </div>

            <h3>3. Komparasi Rezim Pengelolaan</h3>
            <div class="analysis">
                <ul>
                    <li><b>Maximum Economic Yield (MEY):</b> Tercapai pada effort <b>{E_MEY:.2f}</b>. Titik ini memberikan keuntungan bersih (rente ekonomi) tertinggi bagi industri perikanan sekaligus menjaga stok ekologi karena posisinya paling konservatif (paling kiri).</li>
                    <li><b>Maximum Sustainable Yield (MSY):</b> Tercapai pada effort <b>{E_MSY:.2f}</b>. Memaksimalkan tangkapan fisik, namun keuntungan ekonomi sudah mulai tergerus akibat inefisiensi penambahan armada.</li>
                    <li><b>Open Access Equilibrium (OAE):</b> Keseimbangan pasar bebas tercapai pada effort ekstrem <b>{E_OAE:.2f}</b>. Di titik ini, rente ekonomi habis total (TR = TC). Perikanan mengalami kejenuhan ekonomi dan kerusakan parah secara biologis (<i>Tragedy of the Commons</i>).</li>
                </ul>
            </div>
            
            <div class="footer">
                Dikembangkan oleh Yuhka Sundaya, Ekonomi Pembangunan Unisba, 2026.<br>
                <i>Gunakan menu cetak browser (Ctrl+P / Cmd+P) untuk menyimpan dokumen ini sebagai file PDF resmi.</i>
            </div>
        </body>
        </html>
        """
        st.download_button(
            label="📥 Unduh Grafik & Analisis Ekonomi (HTML/PDF)",
            data=html_report_2,
            file_name="Laporan_Analisis_Bioekonomi.html",
            mime="text/html"
        )

# --- FOOTER / KREDIT ---
st.sidebar.markdown("---") 

try:
    st.sidebar.image("logounisba.png", width=90) 
except:
    pass

col_foto, col_teks = st.sidebar.columns([1, 2.5])

with col_foto:
    try:
        st.image("yuka.png", use_container_width=True)
    except:
        pass

with col_teks:
    st.sidebar.markdown(
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
