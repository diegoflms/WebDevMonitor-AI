from openai import OpenAI
import streamlit as st
from sheets import add_rows_to_sheet, init_google_sheets
from texts import ONBOARDING_TEXT, SYSTEM_PROMPT
from datetime import datetime, timedelta # Para timestamp das mensagens
import uuid # Para gerar IDs únicos

st.title("DevMonitor AI")

# Função para construir a lista de dados a serem salvos no Google Sheets
def build_list_to_sheet(message_id, role, content, feedback, token_usage, cached_tokens=0):
    timestamp = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    fb_text = str(feedback) # Garante que o feedback seja string para o Sheets não bugar
    return [timestamp, st.session_state['uuid'], message_id, role, content, fb_text, token_usage, cached_tokens]

# Função para salvar feedback no estado da sessão
def save_feedback(index):
    st.session_state.messages[index]["feedback"] = st.session_state[f"feedback_{index}"]
    feedback_list = build_list_to_sheet(
        st.session_state.messages[index]["message_id"],
        "feedback",
        "feedback",
        st.session_state[f"feedback_{index}"],
        0, # Token usage não é atualizado aqui
    )
    add_rows_to_sheet(tab, [feedback_list])

# Inicializa variáveis de sessão
if 'uuid' not in st.session_state:
    st.session_state['uuid'] = str(uuid.uuid4())
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = st.secrets["OPENAI_MODEL"]
if "messages" not in st.session_state:
    st.session_state.messages = []

tab = init_google_sheets() # Inicializa a aba do Google Sheets para salvar os logs
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) # Inicializa o cliente OpenAI

# Mensagem de inicial
if len(st.session_state.messages) == 0:
    mensagem_inicial = "Olá! Sou seu assistente de web dev. Pergunte-me qualquer coisa relacionada a programação e farei o meu melhor para ajudar! Para mais informações, consulte a barra lateral."
    st.session_state.messages.append({"role": "assistant", "content": mensagem_inicial, "message_id": str(uuid.uuid4())})

# Mensagem de onboarding na sidebar
with st.sidebar:
  st.title("DevMonitor AI")
  st.markdown(ONBOARDING_TEXT)

# Exibição do histórico
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i > 0: # Não exibir o componente de feedback para a mensagem inicial
            feedback = message.get("feedback", None)
            st.session_state[f"feedback_{i}"] = feedback
            st.feedback(
                "thumbs",
                key=f"feedback_{i}",
                disabled=feedback is not None,
                on_change=save_feedback,
                args=[i],
            ) # Componente de feedback

# Input do usuário
if prompt := st.chat_input("Dúvidas de código?"):
    msg_id = str(uuid.uuid4()) # Gera um ID único para a interação

    st.session_state.messages.append({"role": "user", "content": prompt, "message_id": msg_id}) # Salva a mensagem do usuário no estado
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do assistente
    with st.chat_message("assistant"):
        # Construção da lista de mensagens com o System Prompt, criando uma lista nova que começa com o System Prompt e concatena o histórico
        messages_api = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ]

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages_api,
            stream=True,
            stream_options={"include_usage": True},
        ) # Solicita resposta em streaming
        
        # Intercepta o stream para capturar tokens usados
        usage_data = {"prompt": 0, "completion": 0, "cached": 0}
        def interceptador(stream_original):
            for chunk in stream_original:
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content: yield content
                if hasattr(chunk, 'usage') and chunk.usage is not None:
                    usage_data["prompt"] = chunk.usage.prompt_tokens
                    usage_data["completion"] = chunk.usage.completion_tokens
                    if hasattr(chunk.usage, 'prompt_tokens_details') and chunk.usage.prompt_tokens_details:
                         usage_data["cached"] = chunk.usage.prompt_tokens_details.cached_tokens

        response = st.write_stream(interceptador(stream)) # Mostra a resposta em streaming
        
        st.feedback(
            "thumbs",
            key=f"feedback_{len(st.session_state.messages)}",
            on_change=save_feedback,
            args=[len(st.session_state.messages)],
        ) # Componente de feedback para a resposta

        # Salva no Sheets (Pergunta e Resposta iniciais)
        user_list = build_list_to_sheet(msg_id, "user", prompt, "n/a", usage_data["prompt"], usage_data["cached"])
        assistant_list = build_list_to_sheet(msg_id, "assistant", response, "a ser enviado", usage_data["completion"], 0)
        add_rows_to_sheet(tab, [user_list, assistant_list])

    st.session_state.messages.append({"role": "assistant", "content": response, "message_id": msg_id}) # Salva resposta no estado