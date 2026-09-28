import streamlit as st
import requests

# 1. Configurações da página no navegador
st.set_page_config(page_title="Chat com Agente PDF", page_icon="🤖", layout="centered")
st.title("🤖 Assistente de Documentos PDF")
st.caption("Faça perguntas sobre os documentos carregados no Agente.")

# 2. URL da sua API FastAPI (onde o ex1deploy.py está rodando)
API_URL = "https://primeiro-deploy-agente-pdf.onrender.com/chat"

# 3. Inicializa o histórico de mensagens na memória da sessão do navegador
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Exibe todas as mensagens anteriores que estão no histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Campo de entrada para o usuário digitar a pergunta
if prompt := st.chat_input("Digite sua dúvida sobre o PDF..."):
    # Mostra a mensagem do usuário na tela e salva no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Envia a requisição para a API FastAPI e exibe a resposta
    with st.chat_message("assistant"):
        with st.spinner("O agente está consultando o PDF..."):
            try:
                # Monta o payload no formato que o ex1deploy.py espera (ChatRequest)
                payload = {
                    "message": prompt,
                    "user_id": "usuario_web"
                }

                response = requests.post(API_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    resposta_texto = response.json().get("response", "Sem resposta.")
                    st.markdown(resposta_texto)
                    # Guarda a resposta do agente no histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                else:
                    st.error(f"Erro na API ({response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar ao backend. Verifique se o `ex1deploy.py` está rodando na porta 8000!")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")