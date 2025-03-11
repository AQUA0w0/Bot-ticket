import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Carregar variáveis do .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
SUPPORT_ROLE_ID = int(os.getenv("SUPPORT_ROLE_ID"))
VIP_ROLE_ID = int(os.getenv("VIP_ROLE_ID", 0))  # Cargo VIP para prioridade
FEEDBACK_CHANNEL_ID = int(os.getenv("FEEDBACK_CHANNEL_ID", 0))  # Canal para feedbacks

# Configuração do bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} está online!")
    await bot.tree.sync()

# Criar ticket com botões de seleção
class TicketCategorySelect(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Suporte", style=discord.ButtonStyle.primary, custom_id="suporte")
    async def suporte_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "suporte")

    @discord.ui.button(label="Dúvida", style=discord.ButtonStyle.secondary, custom_id="duvida")
    async def duvida_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "dúvida")

    @discord.ui.button(label="Outro", style=discord.ButtonStyle.success, custom_id="outro")
    async def outro_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "outro")

    async def create_ticket(self, interaction, category):
        user = interaction.user
        guild = interaction.guild

        # Criar a categoria de tickets se não existir
        category_obj = discord.utils.get(guild.categories, name="Tickets")
        if not category_obj:
            category_obj = await guild.create_category("Tickets")

        is_vip = VIP_ROLE_ID and discord.utils.get(user.roles, id=VIP_ROLE_ID)
        ticket_name = f"vip-ticket-{user.name}" if is_vip else f"{category}-ticket-{user.name}"
        ticket_channel = await category_obj.create_text_channel(ticket_name, topic=f"Ticket de {user.id}")

        # Definir permissões para suporte e usuário
        await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
        support_role = guild.get_role(SUPPORT_ROLE_ID)
        if support_role:
            await ticket_channel.set_permissions(support_role, read_messages=True, send_messages=True)

        # Botão de fechar ticket
        view = CloseTicketView(user)
        await ticket_channel.send(f"✅ Ticket aberto por {user.mention} na categoria **{category.capitalize()}**.", view=view)
        await interaction.response.send_message(f"Seu ticket foi criado: {ticket_channel.mention}", ephemeral=True)

# **🔴 Botão para fechar ticket e avaliar suporte**
class CloseTicketView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel

        if not channel.topic or "Ticket de" not in channel.topic:
            await interaction.response.send_message("❌ Este canal não é um ticket válido.", ephemeral=True)
            return

        # Captura de quem prestou suporte (usuários com cargo de suporte que interagiram)
        messages = [message async for message in channel.history(limit=100)]
        support_role = interaction.guild.get_role(SUPPORT_ROLE_ID)
        support_members = {msg.author for msg in messages if msg.author != self.user and not msg.author.bot and support_role in msg.author.roles}

        support_list = "\n".join([f"- {member.mention}" for member in support_members]) if support_members else "Nenhum suporte interagiu."

        await interaction.response.send_message("🔴 Por favor, avalie o atendimento antes de fechar o ticket.", ephemeral=True)
        await channel.send(
            f"📝 **Avalie o atendimento antes de fecharmos o ticket!**\n"
            f"👤 **Usuário:** {self.user.mention}\n"
            f"👨‍💼 **Atendimento prestado por:**\n{support_list}",
            view=FeedbackView(self.user, support_members, channel)
        )

# **⭐ Botão para avaliação do suporte**
class FeedbackView(discord.ui.View):
    def __init__(self, user, support_members, ticket_channel):
        super().__init__()
        self.user = user
        self.support_members = support_members
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="⭐ 1", style=discord.ButtonStyle.secondary, custom_id="1")
    async def feedback_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_feedback(interaction, 1)

    @discord.ui.button(label="⭐ 2", style=discord.ButtonStyle.secondary, custom_id="2")
    async def feedback_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_feedback(interaction, 2)

    @discord.ui.button(label="⭐ 3", style=discord.ButtonStyle.secondary, custom_id="3")
    async def feedback_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_feedback(interaction, 3)

    @discord.ui.button(label="⭐ 4", style=discord.ButtonStyle.primary, custom_id="4")
    async def feedback_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_feedback(interaction, 4)

    @discord.ui.button(label="⭐ 5", style=discord.ButtonStyle.success, custom_id="5")
    async def feedback_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_feedback(interaction, 5)

    async def send_feedback(self, interaction: discord.Interaction, rating: int):
        feedback_channel = interaction.guild.get_channel(FEEDBACK_CHANNEL_ID)
        
        # Emojis para estrelas
        star_rating = "⭐" * rating
        
        support_mentions = " ".join([member.mention for member in self.support_members]) if self.support_members else "Nenhum suporte registrado"
        
        if feedback_channel:
            await feedback_channel.send(
                f"📊 **Feedback de Atendimento**\n"
                f"👤 **Usuário:** {self.user.mention}\n"
                f"👨‍💼 **Atendido por:** {support_mentions}\n"
                f"🌟 **Avaliação:** {star_rating} ({rating}/5)"
            )

        await interaction.response.send_message("✅ Obrigado pela sua avaliação! O ticket será fechado em 5 segundos.", ephemeral=True)
        await self.ticket_channel.send("✅ Avaliação registrada. O canal será excluído agora.")
        await asyncio.sleep(5)
        await self.ticket_channel.delete()

# Comando para iniciar a escolha da categoria do ticket
@bot.tree.command(name="ticket", description="Abre um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message("Selecione a categoria do seu ticket:", view=TicketCategorySelect(), ephemeral=True)

# Iniciar o bot
bot.run(TOKEN)
