import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()  # Extrai o texto de cada página
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",     # Quebra de linha em pedaços de texto a partir de um separador
        chunk_size=1000,    # Tamanho do pedaço de texto
        chunk_overlap=100,  # Tamanho do pedaço de texto de sobreposição
        length_function=len # Função que retorna o número de caracteres de cada pedaço de texto
    )
    chunks = text_splitter.split_text(text)  # Divide o texto em pedaços
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()  # Cria um gerador de vetores de embedding OpenAI
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)  # Cria um vetor de armazenamento
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
        temperature=0.2,             # Configura a temperatura
        model_name="gpt-3.5-turbo",  # Configura o modelo de LLM
        max_tokens=500               # Configura o número maximo de tokens por resposta
    )
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)  # Memória para manter o histórico de conversa
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),  # Cria a cadeia de conversação
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is not None:  # Verifica se a cadeia de conversação foi inicializada
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)  # Mensagem do usuário
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)  # Mensagem do bot

def main():
    load_dotenv()  # Carrega as variáveis de ambiente
    st.set_page_config(page_title="Converse com múltiplos PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    st.header("Converse com múltiplos PDFs :books:")
    user_question = st.text_input("Faça uma pergunta sobre seus documentos:")
    if user_question and 'conversation' in st.session_state:  # Verifica se 'conversation' está no estado da sessão
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Seus documentos")
        pdf_docs = st.file_uploader("Carregue seus PDFs aqui e clique em 'Processar'", accept_multiple_files=True)
        if st.button("Processar"):
            if pdf_docs:
                with st.spinner("Processando"):
                    # Obtém o texto do PDF
                    raw_text = get_pdf_text(pdf_docs)

                    # Obtém os pedaços de texto
                    text_chunks = get_text_chunks(raw_text)

                    # Cria o armazenamento de vetores
                    vectorstore = get_vectorstore(text_chunks)

                    # Cria a cadeia de conversação
                    st.session_state.conversation = get_conversation_chain(vectorstore)
            else:
                st.error("Por favor, carregue pelo menos um PDF para prosseguir.")

if __name__ == '__main__':
    main()
