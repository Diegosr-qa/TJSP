# Missão Aprovação — Render + Neon PostgreSQL

Esta versão mantém a página e o JavaScript de `estudo_tjsp.py`, mas troca o arquivo local `progresso_tjsp.json` por uma linha JSONB no PostgreSQL. A autenticação HTTP Basic protege o site e os dados: só quem souber o usuário e a senha configurados pode abrir e alterar o progresso.

## Arquivos

- `estudo_tjsp.py`: conteúdo original da aplicação (interface, plano e funções).
- `app.py`: servidor Flask, API `/api/state`, persistência PostgreSQL e proteção por senha.
- `requirements.txt`: dependências.
- `render.yaml`: configuração do serviço no Render.
- `importar_progresso.py`: importador opcional de um `progresso_tjsp.json` que você já tenha no computador.

## URL do Neon: não coloque no código

A aplicação lê a variável de ambiente `DATABASE_URL` (`os.environ`). Não edite `app.py` para colar a URL. No Render, cadastre a URL em **Environment → DATABASE_URL**. Para desenvolvimento local, copie `.env.example` para `.env` e use um carregador de ambiente se necessário; o app não carrega `.env` automaticamente. Nunca envie `.env` ao GitHub.

O comando `npm run build` deste projeto é apenas uma verificação de sintaxe dos arquivos Python, porque a aplicação original é Python/Flask e não um app Node.js.

## Neon CLI (opcional para provisionamento)

No seu computador, na raiz do projeto, execute os comandos da documentação/solicitação do Neon. Se houver solicitação de autenticação no navegador, conclua o login. Se a instalação ou o login expirar, execute `neon login` e tente novamente. Depois de `neon deploy`, confira `.env.local`/`.env` e copie a variável `DATABASE_URL` para as variáveis de ambiente do Render; o Render não importa automaticamente arquivos `.env.local` do seu computador.

A aplicação usa PostgreSQL. O código atual **não usa object storage**: os backups são baixados pelo navegador como já acontecia na versão original. Para ativar armazenamento de objetos seria necessário conhecer e configurar as variáveis/endpoints exatos provisionados para esse serviço e alterar o recurso de backup; não vou inventar nomes de variáveis nem afirmar que esse serviço está conectado.

## Publicação gratuita

### 1. Criar o banco no Neon

1. Crie uma conta em https://neon.tech/ e crie um projeto PostgreSQL.
2. No painel do projeto, use **Connect** e copie a connection string PostgreSQL. Trate essa URL como senha: não a publique no GitHub nem a envie a ninguém.
3. Guarde a URL para a etapa de variáveis de ambiente. A aplicação cria a tabela `app_state` automaticamente na primeira utilização.

### 2. Enviar os arquivos ao GitHub

1. Crie um repositório novo no GitHub, por exemplo `missao-aprovacao-tjsp`.
2. Envie todos os arquivos desta pasta. Não envie senhas, URLs de banco ou seu arquivo pessoal `progresso_tjsp.json`.
3. Deixe o repositório privado se preferir; o Render precisa ser autorizado a acessá-lo.

### 3. Criar o Web Service no Render

1. Entre em https://render.com/ e conecte sua conta do GitHub.
2. Escolha **New + → Blueprint** e selecione o repositório com `render.yaml`. Se não aparecer Blueprint, crie um **Web Service** apontando para o repositório e configure:
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: **Free**
3. Nas variáveis de ambiente, crie:
   - `DATABASE_URL` = connection string do Neon.
   - `APP_USER` = `estudos` (ou outro usuário que você prefira).
   - `APP_PASSWORD` = uma senha longa, única e difícil de adivinhar.
4. Inicie o deploy e aguarde o estado **Live**. Abra a URL `https://...onrender.com` mostrada pelo Render.
5. O navegador pedirá usuário e senha. Use os valores de `APP_USER` e `APP_PASSWORD`.

### 4. Testar antes de usar

1. Abra o site e confirme que o plano aparece.
2. Marque um tema como concluído e registre uma sessão de questões.
3. Espere alguns segundos para o salvamento automático.
4. Recarregue a página. O progresso deve continuar lá.
5. Abra o mesmo link em outro computador e entre com a mesma senha. O progresso deve ser o mesmo.
6. Use **Baixar backup** periodicamente e guarde o arquivo em local seguro.

## Importar progresso antigo (opcional)

Se você já tem `progresso_tjsp.json` ao lado do script antigo, pode importá-lo para o banco antes de usar a versão hospedada. Faça uma cópia de segurança primeiro. No seu computador, instale as dependências com `pip install -r requirements.txt`, defina `DATABASE_URL` para a URL do Neon e execute:

- Windows PowerShell:
  `$env:DATABASE_URL="COLE_A_URL_DO_NEON_AQUI"`
  `python importar_progresso.py "C:\caminho\para\progresso_tjsp.json"`
- macOS/Linux:
  `export DATABASE_URL='COLE_A_URL_DO_NEON_AQUI'`
  `python importar_progresso.py /caminho/para/progresso_tjsp.json`

A importação substitui o estado existente no banco. Faça isso antes de começar a registrar novos dados no site.

## Limitações e segurança

- O Render gratuito pode colocar o serviço para dormir após inatividade; a primeira abertura depois disso pode demorar cerca de um minuto.
- O banco Neon é externo ao Render, então reinícios e novos deploys do serviço não apagam o progresso. Plano gratuito e limites dos provedores podem mudar; confira os painéis oficiais.
- O site tem um único estado de progresso compartilhado entre quem usa o mesmo login. Não compartilhe usuário e senha. A autenticação protege o acesso, mas não substitui backups.
- O código original salva automaticamente após pequenas alterações; espere alguns segundos antes de fechar a página. Use **Baixar backup** como cópia adicional.
- Não coloque `DATABASE_URL` ou `APP_PASSWORD` no código nem no repositório.
