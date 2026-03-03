import streamlit as st
from src.constants.styles import get_login_styles

def login_screen(CORRECT_PASSWORD):
    """Renderiza a tela de login e gerencia a autenticação."""
    st.markdown(get_login_styles(), unsafe_allow_html=True) # Aplica o CSS específico de login

    col_pad1, col_form, col_gap, col_img, col_pad2 = st.columns([0.2, 1, 0.1, 1, 0.2]) # Colunas: [Respiro, Form, Gap, Imagem, Respiro]

    with col_form: # Renderiza a coluna do formulário
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">WebDevMonitor AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Seu tutor pessoal de desenvolvimento web</p>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            password = st.text_input("", type="password", placeholder="Insira o código de acesso...")
            submit = st.form_submit_button("Acessar Plataforma", use_container_width=True)
            
            if submit:
                if password == CORRECT_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")

    with col_img: # Renderiza a coluna da imagem
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("assets/login_img.png", use_container_width=True)
        
        st.markdown(
            f'<div style="text-align: center; margin-top: 0px; padding: 0px;">'
            f'<span style="color: white; font-size: 0.8rem;">Imagem por </span>'
            f'<a href="https://www.vecteezy.com/members/emojoez" style="color: #F9A940; text-decoration: none; font-weight: bold; font-size: 0.8rem;">Emojoez (Vecteezy)</a>'
            f'</div>', 
            unsafe_allow_html=True
        )

def render_sidebar(intro_text, onboarding_text, click_func):
    """Renderiza a barra lateral completa do sistema."""
    with st.sidebar:
        st.title("WebDevMonitor AI")
        st.markdown(intro_text)

        with st.expander("📌 Como funciona?", expanded=False): # Onboarding Fechável
            st.markdown(onboarding_text)
          
        st.divider()

        st.subheader("💡 Por onde começar?") # Seção "Não sabe por onde começar?"
        st.caption("Clique para enviar:")
          
        base_questions = [
            "Como centralizar uma div?",
            "Explique o Box Model do CSS",
            "Qual a diferença de var, let e const?",
            "Crie uma estrutura básica de HTML5",
            "O que é o DOM no JavaScript?"
        ]
          
        for p in base_questions:
            if st.button(p, key=p):
                click_func(p) # Chama a função utilitária passada por parâmetro

        st.divider()

        if st.button("🗑️ Limpar Conversa", use_container_width=True):
            st.session_state.messages = []
            st.session_state.clicked_question = None
            st.rerun()

def render_chat_history(messages, save_feedback_func, tab_connection):
    """Renderiza o histórico de mensagens do chat, incluindo os componentes de feedback para as mensagens do assistente."""
    for i, message in enumerate(messages):
        role = message["role"]
        with st.chat_message(role, avatar=role):
            st.markdown(message["content"])
            
            if role == "assistant" and i > 0: # Não exibir o componente de feedback para a mensagem inicial e para o usuário
                render_feedback_component(i, message, save_feedback_func, tab_connection)

def render_feedback_component(index, message, callback, tab):
    """Adiciona o componente de feedback (joinha) para as mensagens do assistente, garantindo que o estado do feedback seja mantido e salvo corretamente."""
    feedback_state = message.get("feedback", None)
    st.session_state[f"feedback_{index}"] = feedback_state
    
    st.feedback(
        "thumbs",
        key=f"feedback_{index}",
        disabled=feedback_state is not None,
        on_change=callback,
        args=[index, tab],
    )