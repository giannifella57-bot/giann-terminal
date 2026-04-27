import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit.components.v1 as components



st.set_page_config(page_title="Giann Terminal", layout="wide")

# NOUVEAU BLOC DE FORCE
components.html("""
    <head>
        <meta name="google-adsense-account" content="ca-pub-1620667805227992">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1620667805227992" crossorigin="anonymous"></script>
    </head>
    <body style="background-color: transparent;">
    </body>
""", height=0)


# 1. CONFIGURATION
st.set_page_config(page_title="Giann Terminal - Finance Libre", layout="wide")

# CSS pour le look Terminal
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4251; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE (SIDEBAR)
with st.sidebar:
    st.title("🛡️ Giann Terminal")
    st.subheader("Configuration")
    nom = st.text_input("Investisseur", "Giann")
    risque_label = st.select_slider("Profil de risque", 
                                   options=["Prudent", "Équilibré", "Dynamique", "Agressif"], 
                                   value="Équilibré")
    risk_map = {"Prudent": 0.8, "Équilibré": 1.5, "Dynamique": 2.5, "Agressif": 4.0}
    seuil_max = risk_map[risque_label]
    
    st.divider()
    
# EMPLACEMENT RÉEL GOOGLE ADSENSE
    st.write("📢 **Sponsor**")
    components.html("""
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1620667805227992"
             crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-1620667805227992"
             data-ad-slot="XXXXXXXXXX"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    """, height=300)

# 3. NAVIGATION PAR ONGLETS (TOUT EST DÉBLOQUÉ)
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Analyse Marché", "⚖️ Comparateur", "🔮 Simulation", "📚 Éducation"])

# --- ONGLET 1 : ANALYSE ---
with tab1:
    ticker = st.text_input("Rechercher un actif", "NVDA").upper()
    
    if ticker:
        data = yf.Ticker(ticker)
        hist = data.history(period="1y", interval="1d")
        
        if not hist.empty:
            prix_actuel = hist['Close'].iloc[-1]
            volatilite = hist['Close'].pct_change().std() * 100
            sma50 = hist['Close'].rolling(window=50).mean()
            
            # Métriques
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Prix", f"{prix_actuel:.2f} $")
            m2.metric("Volatilité j.", f"{volatilite:.2f} %")
            m3.success("✅ ANALYSE ACTIVE")
            m4.info("🚀 SMA 50 INCLUSE")

            # Graphique
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.add_trace(go.Scatter(x=hist.index, y=sma50, name="Moyenne 50j", line=dict(color='orange')))
            fig.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig, use_container_width=True)
            
            # RSI automatique (Anciennement Premium)
            st.subheader("💡 Indicateurs Avancés")
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            perte = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain/perte))).iloc[-1]
            st.info(f"Force du Marché (RSI) : {rsi:.2f}")

# --- ONGLET 2 : COMPARATEUR ---
with tab2:
    st.subheader("⚖️ Comparaison")
    # ... (Code inchangé mais accès libre)
    t1 = st.text_input("Actif A", "SPY").upper()
    t2 = st.text_input("Actif B", "BTC-USD").upper()
    df = yf.download([t1, t2], period="1y")['Close']
    st.line_chart(df / df.iloc[0] * 100)

# --- ONGLET 3 : SIMULATION (DÉBLOQUÉ) ---
with tab3:
    st.subheader("🔮 Simulateur de Patrimoine")
    
    # EMPLACEMENT PUB 2 : Bannière horizontale avant simulation
    components.html("""
        <div style="background-color: #1e2130; color: white; padding: 10px; text-align: center; border-radius: 5px;">
            <p style="margin: 0; font-size: 10px; color: gray;">PUBLICITÉ</p>
            <p style="margin: 0;">Besoin d'un courtier ? Profitez de 0€ de commission ici.</p>
        </div>
    """, height=60)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        t_sim = st.text_input("Ticker Simulation", "SPY").upper()
        cap_init = st.number_input("Capital initial (€)", value=1000)
    with col_s2:
        versement = st.number_input("Épargne mensuelle (€)", value=100)
        duree = st.slider("Horizon (Années)", 1, 30, 10)
            
    if t_sim:
        h_sim = yf.Ticker(t_sim).history(period="10y")
        if not h_sim.empty:
            rendement_ann = ((h_sim['Close'].iloc[-1] / h_sim['Close'].iloc[0]) ** (1/10)) - 1
            cap = cap_init
            evolution = []
            for i in range(duree * 12):
                cap = (cap + versement) * (1 + (rendement_ann/12))
                evolution.append(cap)
            st.metric("Projection Finale", f"{cap:,.2f} €")
            st.line_chart(evolution)

# --- ONGLET 4 : ÉDUCATION ---
with tab4:
    st.subheader("🎓 Masterclass")
    st.write("Contenu éducatif gratuit financé par la publicité.")
