<!-- PROJECT LOGO -->
<br>
<div align="center">
  <a href="">
    <img src="assets\login_img.png" alt="Logo" width="150" height="150">
  </a>

  <h1 align="center">WebDevMonitor AI</h1>

  <p align="center">
    O seu tutor pessoal de desenvolvimento web e mobile!
    <br>
    <a href="https://github.com/diegoflms/WebDevMonitor-AI">Explore o Projeto</a>
    &middot;
    <a href="https://webdevmonitor-ai.onrender.com/">Acesse o Sistema</a>
    &middot;
    <a href="https://github.com/diegoflms/WebDevMonitor-AI/issues/new?labels=bug&template=bug-report---.md">Reportar Bug</a>
    &middot;
    <a href="https://github.com/diegoflms/WebDevMonitor-AI/issues/new?labels=enhancement&template=feature-request---.md">Sugerir Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<div align="center">
  <h3 align="center">Conteúdos</h3>

  <p align="center">
    <a href="#sobre-o-projeto">Sobre o Projeto</a>
    &middot;
    <a href="#tecnologias">Tecnologias</a>
    &middot;
    <a href="#primeiros-passos">Primeiros Passos</a>
    &middot;
    <a href="#pré-requisitos">Pré-requisitos</a>
    &middot;
    <a href="#instalação">Instalação</a>
    &middot;
    <a href="#uso">Uso</a>
    &middot;
    <a href="#contribuição">Contribuição</a>
    &middot;
    <a href="#licença">Licença</a>
    &middot;
    <a href="#contato">Contato</a>
    &middot;
    <a href="#agradecimentos">Agradecimentos</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## Sobre o Projeto
![tela inicial do projeto](assets\screenshot.png)

O WebDevMonitor AI é um assistente pedagógico inteligente desenvolvido para apoiar o ensino e aprendizado de tecnologias de desenvolvimento web e mobile, tanto front-end quanto back-end. Este projeto surge no contexto da minha graduação e está vinculado a um trabalho de Iniciação Científica, servindo como peça central para o meu Trabalho de Conclusão de Curso (TCC).

A ferramenta foi concebida para atender às demandas da disciplina Desenvolvimento Web e Mobile, funcionando como um tutor em tempo real que guia os alunos na resolução de problemas de código sem entregar a resposta pronta. Utilizando modelos de linguagem de grande escala (LLMs), o sistema prioriza uma abordagem didática, enquanto registra e estrutura logs de interação para permitir a análise posterior da evolução pedagógica dos estudantes.

### Tecnologias

A arquitetura do WebDevMonitor AI foi planejada para unir simplicidade de interface com robustez no processamento de dados. A aplicação utiliza o framework Streamlit para fornecer uma experiência de usuário fluida e responsiva, enquanto o backend é impulsionado por modelos de linguagem de última geração via API da Groq e OpenAI. Para a persistência de dados e monitoramento em tempo real das interações, o sistema integra-se diretamente à Google Sheets API, permitindo que os logs pedagógicos sejam estruturados e analisados sem a necessidade de um banco de dados relacional complexo.

* Linguagem: Python
* Interface Web: Streamlit
* Modelos de IA: Groq (Llama 3.3) e OpenAI
* Persistência de Dados: Google Sheets API
* Infraestrutura e Deploy: Render
* Gerenciamento de Ambiente: Python-dotenv e Streamlit Secrets
* Auditoria de Respostas: Framework ELMES (Ambiente de Desenvolvimento)

<!-- GETTING STARTED -->
## Primeiros Passos

Siga as instruções abaixo para configurar uma cópia local do projeto e executá-la em seu ambiente de desenvolvimento.

### Pré-requisitos

Antes de começar, você precisa ter o Python 3.9+ instalado em sua máquina, assim como o Pip (gerenciador de pacotes do Python).
```sh
python -m pip install --upgrade pip
```

### Instalação

O projeto foi estruturado para facilitar a configuração, utilizando variáveis de ambiente para gerenciar as chaves de API com segurança.

1. Clone o repositório
    ```sh
    git clone https://github.com/diegoflms/WebDevMonitorAI.git
    ```
3. Crie e ative um ambiente virtual
    ```sh
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Instale as dependências
    ```sh
    pip install -r requirements.txt
    ```
    * Observe que as dependências para executar os testes do ELMES estão comentadas. Se desejar executar testes, instale aquelas dependências.  
    Também é necessário configurar o arquivo de testes, inserindo alguns dados, segue exemplo:
        ```sh
        api_key: "SUA_CHAVE_AQUI"
        api_base: https://api.groq.com/openai/v1
        model: llama-3.3-70b-versatile
        ```
5. Configure suas variáveis de ambiente
    Crie um arquivo secrets.toml em .streamlit/ e adicione suas chaves:
    ```toml
    GROQ_API_KEY= "sua_chave_openai_aqui"
    GROQ_MODEL = "seu_modelo_aqui"
    PASSWORD = "sua_senha_acesso"
    TITLE = "titulo_arquivo_google_sheets"
    FOLDER_ID = "id_pasta_google"
    [gcp_service_account]
    "seu_json_do_google_aqui" (em chaves)
    ```
6. Execute a aplicação:
    ```sh
    streamlit run app.py
    ```

<!-- USAGE EXAMPLES -->
## Uso

O WebDevMonitor AI foi projetado para ser intuitivo e totalmente focado no fluxo de aprendizagem do aluno de programação web e mobile. Ao acessar a URL da aplicação, o usuário é inicialmente recebido por uma tela de autenticação, onde deve inserir a senha de acesso configurada para garantir a segurança do ambiente de tutoria. Uma vez autenticado, a interface principal apresenta um chat limpo e uma barra lateral que contém instruções de onboarding e botões de atalho para dúvidas recorrentes, facilitando o início imediato da interação.

A interação ocorre de forma natural: o estudante envia seu fragmento de código ou descreve uma dificuldade, e o tutor responde não com a solução pronta, mas com pistas, provocações técnicas e explicações conceituais que guiam o aluno na construção do próprio conhecimento. Durante a conversa, o usuário pode utilizar o sistema de feedback integrado (ícones de polegar) para avaliar a utilidade de cada resposta. Todas essas interações, incluindo o consumo de tokens e as notas de feedback, são registradas automaticamente em uma planilha de monitoramento, fornecendo a base de dados necessária para a análise pedagógica da pesquisa.

<!-- CONTRIBUTING -->
## Contribuição

Contribuições são o motor que faz a comunidade acadêmica e de código aberto um lugar incrível para aprender, inspirar e criar. Como o WebDevMonitor AI é um projeto em constante evolução dentro de um Trabalho de Conclusão de Curso (TCC) e Iniciação Científica, toda ajuda para torná-lo uma ferramenta pedagógica melhor é muito apreciada.

Se você tiver uma sugestão que possa melhorar a didática do tutor ou a eficiência do monitoramento, por favor, faça um fork do repositório e crie um pull request. Você também pode abrir uma issue com a tag "melhoria".
Não se esqueça de dar uma estrela no projeto! Agradeço imensamente o apoio.

1. Faça o Fork do projeto
2. Crie sua Feature Branch (git checkout -b feature/NovaFuncionalidade)
3. Faça o Commit de suas alterações (git commit -m 'Adicionando uma funcionalidade incrível')
4. Faça o Push para a Branch (git push origin feature/NovaFuncionalidade)
5. Abra um Pull Request

<!-- LICENSE -->
## Licença

Este projeto está sob a licença MIT.

Copyright 2026 Diego Lemos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<!-- CONTACT -->
## Contato

Diego Lemos - [LinkedIn](https://www.linkedin.com/in/diego-lemos-b08ab4270/)

Link do Projeto: [WebDevMonitor AI](https://github.com/diegoflms/WebDevMonitorAI)


<!-- ACKNOWLEDGMENTS -->
## Agradecimentos

Este projeto é fruto de um esforço coletivo entre pesquisa acadêmica e desenvolvimento técnico. Gostaria de agradecer aos recursos e instituições que tornaram este trabalho possível:

* [LabES (Laboratório de Engenharia de Software)](http://www.labes.icmc.usp.br/)
* [Profa. Dra. Lina Garcés](https://scholar.google.com.br/citations?hl=pt-BR&user=d-eBm1oAAAAJ&view_op=list_works)
* [Framework ELMES](https://arxiv.org/abs/2507.22947)