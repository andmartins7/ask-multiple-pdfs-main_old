# MultiPDF Chat App


## Introdução
------------
O MultiPDF Chat App é uma aplicação Python que permite conversar com vários documentos PDF. Você pode fazer perguntas sobre os PDFs usando linguagem natural, e a aplicação fornecerá respostas relevantes baseadas no conteúdo dos documentos. Este aplicativo utiliza um modelo de linguagem para gerar respostas precisas para suas consultas. Observe que o aplicativo responderá apenas a perguntas relacionadas aos PDFs carregados.

## Funcionamento
------------


A aplicação segue estes passos para fornecer respostas às suas perguntas:

1. Carregamento de PDF: O aplicativo lê vários documentos PDF e extrai o conteúdo textual deles.

2. Fragmentação de Texto: O texto extraído é dividido em pedaços menores que podem ser processados eficazmente.

3. Modelo de Linguagem: A aplicação utiliza um modelo de linguagem para gerar representações vetoriais (embeddings) dos fragmentos de texto.

4. Correspondência de Semelhança: Quando você faz uma pergunta, o aplicativo a compara com os fragmentos de texto e identifica os mais semanticamente semelhantes.

5. Geração de Resposta: Os fragmentos selecionados são passados para o modelo de linguagem, que gera uma resposta baseada no conteúdo relevante dos PDFs.

## Dependências e Instalação
----------------------------
Para instalar o MultiPDF Chat App, siga estes passos:

1. Copie o código para sua máquina local.

2. Instale as dependências necessárias executando o seguinte comando:
   ```
   pip install -r requirements.txt
   ```

3. Instale o **pytest** para executar os testes da aplicação. Recomenda-se utilizar um ambiente virtual:
   ```
   pip install pytest
   ```
4. Obtenha uma chave de API da OpenAI e adicione-a ao arquivo `.env` no diretório do projeto.
```commandline
OPENAI_API_KEY=your_secrit_api_key
```

## Uso
-----
Para usar o MultiPDF Chat App, siga estes passos:

1. Certifique-se de ter instalado as dependências necessárias e adicionado a chave da API da OpenAI ao arquivo `.env`.

2. Execute o arquivo `app.py` usando a CLI do Streamlit. Execute o seguinte comando:
   ```
   streamlit run app.py
   ```

3. A aplicação será lançada em seu navegador web padrão, exibindo a interface do usuário.

4. Carregue vários documentos PDF no aplicativo, seguindo as instruções fornecidas.

5. Faça perguntas em linguagem natural sobre os PDFs carregados usando a interface de chat.