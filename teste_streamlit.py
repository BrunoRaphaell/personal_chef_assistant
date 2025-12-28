import streamlit as st
import base64
from src.agent import build_chef_agent # Supondo que sua factory esteja aqui
from langchain_core.messages import HumanMessage

# Instancia o agente
chef_agent = build_chef_agent()
config = {"configurable": {"thread_id": "sessao_usuario_1"}}

st.title("👨‍🍳 Chef IA")

# 1. Upload do Arquivo
uploaded_file = st.file_uploader("Upload da foto da geladeira", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Mostra a imagem na tela
    st.image(uploaded_file, caption="Imagem carregada", use_column_width=True)

    if st.button("Analisar e Criar Receita"):
        
        # 2. Processamento: Converter o arquivo em memória para Base64
        # .getvalue() pega os bytes brutos do upload
        image_bytes = uploaded_file.getvalue()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Define o tipo MIME (opcional, mas bom ser preciso)
        mime_type = uploaded_file.type # ex: 'image/jpeg' ou 'image/png'

        # 3. Montar o Payload Multimodal
        # O modelo espera uma lista contendo partes de texto e partes de imagem
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

        # 4. Invocar o Agente
        st.write("🤖 Chef processando...")
        
        try:
            response = chef_agent.invoke(
                # Passamos ("user", conteudo_complexo)
                {"messages": [("user", message_content)]},
                config=config
            )
            
            # Recuperar a resposta (ajuste conforme seu output estruturado ou texto)
            # Se estiver usando response_format:
            if "structured_response" in response:
                receita = response["structured_response"]
                st.success(f"Receita: {receita.titulo}")
                st.write(receita.instrucoes)
            else:
                st.write(response["messages"][-1].content)
                
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

