import streamlit as st
import requests
import random

from deep_translator import GoogleTranslator

idioma = st.sidebar.selectbox("Idioma", ["Português", "Inglês"])
codigo_idioma = "pt" if idioma == "Português" else "en"

cores = ["#FFFFFF", "#F5F5F5", "#E0F7FA", "#E6FFFA", "#F3E5F5", "#FFE0B2", "#FFEBEE", "#FFF9C4", "#E3F2FD", "#F1F8E9"]
fundo = random.choice(cores)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {fundo};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def traduzir(texto):
    if codigo_idioma == "pt":
        return texto
    try:
        return GoogleTranslator(source='auto', target=codigo_idioma).translate(texto)
    except:
        return texto

st.title(traduzir("Consulte o modelo de carro desejado"))

modelo = st.text_input(traduzir("Digite o modelo do carro desejado (ex: civic, corolla, cruze):")).strip().lower()

if modelo:
    url = f'https://api.api-ninjas.com/v1/cars?model={modelo}'
    headers = {'X-Api-Key': st.secrets['API_KEY']}

    try:
        resposta = requests.get(url, headers=headers, timeout=5)
        resposta.raise_for_status()
        carros = resposta.json()

        if carros:
            for carro in carros:
                st.write(f"#### **{traduzir('Carro encontrado no banco de dados')}** ")
                st.write(f"{traduzir('Marca')}: {carro['make']}")
                st.write(f"{traduzir('Modelo')}: {carro['model']}")
                st.write(f"{traduzir('Ano')}: {carro['year']}")
                st.write(f"{traduzir('Cilindros')}: {carro['cylinders']}")
                st.write(f"{traduzir('Combustível')}: {carro['fuel_type']}")
                transmissao = "Manual" if carro['transmission'] == 'm' else "Automática"
                st.write(f"{traduzir('Transmissão')}: {traduzir(transmissao)}")
                st.write(f"{traduzir('Tração')}: {carro['drive'].upper()}")
                st.write("-" * 30)
        else:
            st.warning(f"{traduzir('Nenhum resultado encontrado para')} '{modelo}'.")
    except Exception as e:
        st.error(f"{traduzir('Erro na requisição')}: {e}")
else:
    st.info(traduzir("Nenhum modelo foi digitado."))
