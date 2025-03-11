# 🎟️ Bot de Tickets para Discord  
**Desenvolvido por [aqua0w0](https://github.com/aqua0w0)**  

Um bot de tickets completo para Discord, permitindo que usuários **abram tickets rapidamente, avaliem o suporte** e que **administradores removam tickets bugados**.  

🚀 **Destaques**:  
✅ Tickets criados com um clique  
✅ Avaliação de suporte antes do fechamento  
✅ Correção automática de tickets bugados  
✅ Feedback detalhado no canal de feedbacks  

## 📌 **Funcionalidades**
- **Criação de tickets** via botões interativos.  
- **Fechamento de tickets** apenas pelo usuário que abriu.  
- **Avaliação de atendimento** antes do fechamento.  
- **Correção automática de tickets bugados**.  
- **Envio de feedbacks** detalhados com nota e atendentes.  

## 🛠️ **Instalação**
1️⃣ **Clone o repositório**:  
   ```bash
   git clone https://github.com/aqua0w0/bot-ticket.git
   cd bot-de-tickets

2️⃣ Instale as dependências:

pip install -r requirements.txt

3️⃣ Configure o .env com os IDs do seu servidor.

4️⃣ Inicie o bot:

python bot.py

⚙️ Configuração (.env)

Edite o arquivo .env com as configurações do seu servidor:

# Token do bot
DISCORD_TOKEN=SEU_TOKEN_AQUI

# ID do servidor
GUILD_ID=SEU_ID_DO_SERVIDOR

# ID do cargo de suporte
SUPPORT_ROLE_ID=SEU_ID_DO_CARGO_DE_SUPORTE

# ID do cargo VIP (opcional)
VIP_ROLE_ID=SEU_ID_DO_CARGO_VIP

# ID do canal de feedbacks (opcional)
FEEDBACK_CHANNEL_ID=SEU_ID_DO_CANAL_DE_FEEDBACKS

🎟️ Como Usar

1️⃣ Criar um Ticket

📌 Use o comando: /ticket
📌 Escolha a categoria (Suporte, Dúvida, Outro)
📌 O ticket será criado automaticamente em uma categoria privada.

2️⃣ Fechar um Ticket

📌 Clique no botão "Fechar Ticket" dentro do canal do ticket.
📌 O usuário deve avaliar o atendimento antes do ticket ser excluído.
📌 A avaliação será enviada ao canal de feedbacks.

3️⃣ Resolver Tickets Bugados

📌 Se um ticket não fechar corretamente, o bot oferece um botão para excluí-lo.
📌 Administradores podem usar /resetartickets para remover tickets travados.

📊 Sistema de Avaliação

Após o atendimento, o usuário recebe um botão para avaliar o suporte antes do ticket ser fechado.

📌 A avaliação inclui:

🌟 Nota de 1 a 5 estrelas

👤 Quem abriu o ticket

👨‍💼 Quem prestou suporte

📢 O feedback é enviado para um canal específico

💡 Segurança e Redundâncias

✔️ Verificação automática de tickets bugados
✔️ Somente o usuário pode fechar tickets
✔️ Feedback detalhado no canal configurado
✔️ Correção automática de canais travados

🏆 Créditos

Este bot foi desenvolvido por aqua0w0.
Se quiser sugerir melhorias ou relatar bugs, entre em contato no GitHub. 🚀
