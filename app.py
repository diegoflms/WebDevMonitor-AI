import streamlit as st
import uuid
from texts import *
from utils import *
from interface import *
from sheets import *
from styles import *

# --- CONFIGURAÇÃO INICIAL ---
init_session_state() # Garante que as variáveis de estado existam antes de qualquer coisa
st.markdown(get_main_styles(), unsafe_allow_html=True) # Aplica os estilos principais
st.set_page_config(page_title="WebDevMonitor AI", page_icon="🚀", layout="wide") # Configuração da visual página

if not st.session_state["authenticated"]: # Lógica de autenticação
    login_screen(st.secrets["PASSWORD"])
    st.stop()

st.title("WebDevMonitor AI") # Título da aplicação
client, tab = load_connections() # Inicializa conexões com OpenAI e Google Sheets

if st.session_state["authenticated"]: # Renderiza a sidebar
    render_sidebar(INTRO_TEXT, ONBOARDING_TEXT, click_question)

# --- EXIBIÇÃO DO CHAT ---
if len(st.session_state.messages) == 0: # Mensagem inicial
    first_message = FIRST_MSG
    st.session_state.messages.append({"role": "assistant", "content": first_message, "message_id": str(uuid.uuid4())})

render_chat_history(st.session_state.messages, save_feedback, tab) # Renderiza o histórico de mensagens

# --- LÓGICA DE INPUT ---
prompt = None
text_input = st.chat_input("Dúvida de código?")

# 1. Definição do Prompt (Sidebar ou Input)
if st.session_state.clicked_question:
    prompt = st.session_state.clicked_question
    st.session_state.clicked_question = None
elif text_input:
    prompt = text_input

if prompt:
    msg_id = str(uuid.uuid4())
    st.session_state.messages.append({"role": "user", "content": prompt, "message_id": msg_id})
    
    with st.chat_message("user", avatar='user'):
        st.markdown(prompt)

    # 2. Resposta do Assistente
    with st.chat_message("assistant", avatar='assistant'):
        with st.spinner("Analisando sua mensagem..."):
            # Prepara o histórico limitado
            CONTEXT_WINDOW = 10
            recent_history = st.session_state.messages[-CONTEXT_WINDOW:]
            messages_api = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in recent_history
            ]

            try:
                usage_data = {"prompt": 0, "completion": 0, "cached": 0} # Dicionário para capturar os tokens vindos do utils
                
                response = st.write_stream(get_ai_response(client, st.session_state["openai_model"], messages_api, usage_data)) # O st.write_stream consome o gerador que criamos no utils
                
                # 3. Finalização (Feedback e Logs)
                st.feedback(
                    "thumbs",
                    key=f"feedback_{len(st.session_state.messages)}",
                    on_change=save_feedback,
                    args=[len(st.session_state.messages), tab],
                )

                user_list = build_list_to_sheet(msg_id, "user", prompt, "n/a", usage_data["prompt"], usage_data["cached"])
                assistant_list = build_list_to_sheet(msg_id, "assistant", response, "a ser enviado", usage_data["completion"], 0)
                add_rows_to_sheet(tab, [user_list, assistant_list])

                st.session_state.messages.append({"role": "assistant", "content": response, "message_id": msg_id})

            except Exception as e:
                st.error("⚠️ Ops! Tivemos um problema técnico ao falar com a IA.")
                st.info("Tente novamente em instantes.")
                print(f"Erro OpenAI: {e}")