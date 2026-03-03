import streamlit as st
from datetime import datetime, timedelta
import gspread # Biblioteca para Google Sheets
from oauth2client.service_account import ServiceAccountCredentials # Autenticação

@st.cache_resource
def init_google_sheets():
  """Inicializa a conexão com o Google Sheets usando as credenciais do serviço e retorna a aba para manipulação."""
  creds_dict = st.secrets["gcp_service_account"]
  scope = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes=scope)
  client = gspread.authorize(creds)

  complete_sheet = client.open(title=st.secrets["TITLE"], folder_id=st.secrets["FOLDER_ID"])
  sheet = complete_sheet.get_worksheet(0)
  return sheet

def add_rows_to_sheet(tab, data_list):
    """Adiciona uma lista de dados como nova linha no Google Sheets, com tratamento de erros."""
    try:
        tab.append_rows(data_list)
    except Exception as e:
        print(f"⚠️ Erro crítico ao salvar no Google Sheets: {e}")

def build_list_to_sheet(message_id, role, content, feedback, token_usage, cached_tokens=0):
    """Constrói a lista de dados a serem salvos no Google Sheets, incluindo timestamp, UUID da sessão, ID da mensagem, papel (user/assistant), conteúdo, feedback e uso de tokens."""
    timestamp = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    fb_text = str(feedback) # Garante que o feedback seja string para o Sheets não bugar
    return [timestamp, st.session_state['uuid'], message_id, role, content, fb_text, token_usage, cached_tokens]