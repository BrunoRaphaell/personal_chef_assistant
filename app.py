import streamlit as st
from src.agent import build_chef_agent
import base64

st.set_page_config(
    page_title="Personal Chef AI",
    page_icon="👨‍🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Remove o padding padrão exagerado do topo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Estiliza o título principal */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        color: #333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    /* Estiliza o botão de upload para ficar mais discreto */
    .stFileUploader {
        max-width: 500px;
        margin: 0 auto;
    }
    /* Card de receita (exemplo de formatação) */
    .recipe-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_chef_agent():
    return build_chef_agent()

chef_agent = get_chef_agent()
config = {"configurable": {"thread_id": "user_session_123"}}

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👨‍🍳 Personal Chef AI")
st.markdown('<p class="subtitle">O que tem na sua geladeira hoje? Tire uma foto e deixe-me criar a receita.</p>', unsafe_allow_html=True)

upload_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Arraste sua foto ou clique para buscar", 
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed" # Esconde o label para ficar mais limpo
    )

# --- Lógica Principal ---
if uploaded_file is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Sua despensa/geladeira", use_column_width=True)
        
    b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
    with b_col2:
        analyze_btn = st.button("🔍 Analisar e Cozinhar", type="primary", use_container_width=True)

    if analyze_btn:
        
        with st.spinner("O Chef está analisando seus ingredientes..."):
            image_bytes = uploaded_file.getvalue()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            mime_type = uploaded_file.type
            
            message_content = [
                {
                    "type": "text", 
                    "text": "Analise esta imagem, identifique os ingredientes e sugira uma receita baseada neles."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}
                }
            ]

            try:
                response = chef_agent.invoke(
                    {"messages": [("user", message_content)]},
                    config=config
                )
                
                ai_message = response['messages'][-1].content
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_message
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao processar {e}")

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte algo sobre a receita (ex: 'Posso trocar tomate por cebola?')"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando o Chef..."):
            try:
                response = chef_agent.invoke(
                    {"messages": [("user", prompt)]},
                    config=config
                )
                
                ai_content = response['messages'][-1].content
                
                st.markdown(ai_content)
                st.session_state.messages.append({"role": "assistant", "content": response['messages'][-1].content})
            except Exception as e:
                st.error(f"Erro de comunicação: {e}")
                