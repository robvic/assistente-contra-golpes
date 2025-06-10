# Assistente-Contra-Golpes
Assistente de IA para guias e dúvidas contra os golpes digitais mais comumente aplicados.

## Requisitos:
- Git instalado
- Python 3.*
- Instalar dependências (*pip install -r requirements.txt*)
- Instalar Google Cloud CLI:
https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
- Instalar WhatsApp Desktop:
https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi
- Login no GCP via CLI (*gcloud auth login*)
- Token do OpenAI nas variáveis de ambiente: (*setx GPT_KEY "token_gerado"*)
https://platform.openai.com/settings/organization/api-keys

## Instruções:
1) Faça o clone deste repositório na máquina local.
2) Disponibilize o caminho do link do WhatsApp Desktop (ex: *C:/Users/Desktop/Whatsapp.lnk*)
3) Substitua o caminho do link na constante **APP_LINK** em *src/interface.py*
4) Execute o código via ponto de entrada: *src/app.py*

## TO-DO:
- [x] Conexão do GPT com WhatsApp.
- [x] Ingest com sumarização de arquivos txt e pdf.
- [x] Implantação na máquina local.
- [x] Pipeline CI.
- [x] Workaround sobre janela de notificações.
- [x] Escrita da resposta com acentuação correta.
- [x] Externalização das instruções/prompts.
- [x] IaC.
- [ ] Estrtura de testes técnicos.
- [ ] Registro de logs.
- [ ] Estrutura de testes de funcionalidade e acurácia.