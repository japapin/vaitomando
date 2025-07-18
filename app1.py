import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador Descarga e Paletização", layout="centered")

# Estilo dark personalizado
st.markdown("""
    <style>
        body, .main {
            background-color: #121212;
            color: #f0f0f0;
        }
        .stApp {
            background-color: #121212;
        }
        h1, h2, h3, h4 {
            color: #FFFFFF;
        }
        .stRadio > div {
            background-color: #1e1e1e;
            padding: 10px;
            border-radius: 8px;
        }
        .stSelectbox > div, .stMultiselect > div {
            background-color: #1e1e1e !important;
        }
        .stNumberInput > div {
            background-color: #1e1e1e !important;
        }
        .stTextInput > div {
            background-color: #1e1e1e !important;
        }
        .stMarkdown {
            color: #CCCCCC;
        }
        .total-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            color: #00ff88;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-top: 30px;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📦 Simulador Descarga/Paletização")
st.markdown("**Vigência: 01/01/2025 a 30/11/2025**")
st.markdown("---")

# Situação
situacao = st.radio("🧾 Selecione a situação do serviço:", ["Normal", "Reagendado", "Exceção"], horizontal=True)

# Tipo de carga
tipo_carga = st.selectbox("📄 Tipo de Carga:", ["Granel", "Paletizada"])

# Nova opção: exceção obrigatória
excecao_obrigatoria = st.checkbox("🔺 Simular como exceção obrigatória (cobra o veículo em qualquer tipo de carga)")

# Tipo de Veículo (sem devolução de paletes)
tipo_veiculo = st.selectbox("🚚 Tipo de Veículo:", [
    "CARRETA", "CARRETA (linha branca)",
    "TRUCK", "TRUCK (linha branca)",
    "TOCO", "TOCO (linha branca)"
])

# Quantidade de pallets
qtd_pallets = st.number_input("📦 Quantidade de Pallets:", min_value=0, step=1)

# Serviços adicionais
st.subheader("➕ Serviços Adicionais (opcional)")
servicos_adicionais = st.multiselect("Selecione adicionais:", [
    "PALETIZAÇÃO NO RECEBIMENTO",
    "Serviço de inutilização do palete (stretch)",
    "Descarga de Palete sobre Palete"
])

# Tabela de valores atualizada
valores = {
    "Normal": {
        "CARRETA": 831.13, "CARRETA (linha branca)": 1943.85,
        "TRUCK": 881.13, "TRUCK (linha branca)": 1981.21,
        "TOCO": 721.25, "TOCO (linha branca)": 664.50,
        "DESCARGA PALETIZADA": 24.44,
        "PALETIZAÇÃO NO RECEBIMENTO": 46.56,
        "VEÍCULOS UTILITÁRIO E FURGÕES (EXPRESS)": 199.29,
        "Serviço de inutilização do palete (stretch)": 2.97,
        "Descarga de Palete sobre Palete": 35.42
    },
    "Reagendado": {
        "CARRETA": 1761.96, "CARRETA (linha branca)": 4120.97,
        "TRUCK": 1867.20, "TRUCK (linha branca)": 4208.64,
        "TOCO": 1528.01, "TOCO (linha branca)": 1408.74,
        "DESCARGA PALETIZADA": 51.85,
        "PALETIZAÇÃO NO RECEBIMENTO": 98.70,
        "VEÍCULOS UTILITÁRIO E FURGÕES (EXPRESS)": 422.48,
        "Serviço de inutilização do palete (stretch)": 6.30,
        "Descarga de Palete sobre Palete": 75.07
    },
    "Exceção": {
        "CARRETA": 2466.72, "CARRETA (linha branca)": 5769.36,
        "TRUCK": 2614.79, "TRUCK (linha branca)": 5851.92,
        "TOCO": 2140.28, "TOCO (linha branca)": 1792.22,
        "DESCARGA PALETIZADA": 72.57,
        "PALETIZAÇÃO NO RECEBIMENTO": 138.18,
        "VEÍCULOS UTILITÁRIO E FURGÕES (EXPRESS)": 591.47,
        "Serviço de inutilização do palete (stretch)": 8.82,
        "Descarga de Palete sobre Palete": 105.11
    }
}

# Cálculo do valor total
total = 0.0

# Regra para exceção obrigatória
if excecao_obrigatoria:
    total += valores[situacao][tipo_veiculo]
    if tipo_carga == "Granel":
        total += qtd_pallets * valores[situacao]["PALETIZAÇÃO NO RECEBIMENTO"]
    elif tipo_carga == "Paletizada":
        total += qtd_pallets * valores[situacao]["DESCARGA PALETIZADA"]
else:
    if tipo_carga == "Granel":
        total += valores[situacao][tipo_veiculo]
        total += qtd_pallets * valores[situacao]["PALETIZAÇÃO NO RECEBIMENTO"]
    elif tipo_carga == "Paletizada":
        total += qtd_pallets * valores[situacao]["DESCARGA PALETIZADA"]

# Adicionais
for adicional in servicos_adicionais:
    total += valores[situacao][adicional]

# Resultado
st.markdown("---")
st.markdown(f"<div class='total-box'>💰 Valor total simulado: R$ {total:,.2f}</div>", unsafe_allow_html=True)
