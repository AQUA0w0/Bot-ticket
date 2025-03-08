import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
SUPPORT_ROLE_ID = int(os.getenv("SUPPORT_ROLE_ID"))

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        channel_id INTEGER,
        status TEXT
    )
""")
conn.commit()

# Configuração do bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online!")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# Comando para abrir um ticket
@bot.tree.command(name="ticket", description="Abre um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    user = interaction.user
    guild = interaction.guild

    # Verifica se o usuário já tem um ticket aberto
    cursor.execute("SELECT channel_id FROM tickets WHERE user_id = ? AND status = ?", (user.id, "aberto"))
    existing_ticket = cursor.fetchone()

    if existing_ticket:
        await interaction.response.send_message(f"Você já tem um ticket aberto! <#{existing_ticket[0]}>", ephemeral=True)
        return

    # Criar canal de ticket
    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
        category = await guild.create_category("Tickets")

    ticket_channel = await category.create_text_channel(f"ticket-{user.name}")
    await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
    
    support_role = guild.get_role(SUPPORT_ROLE_ID)
    if support_role:
        await ticket_channel.set_permissions(support_role, read_messages=True, send_messages=True)

    # Salvar ticket no banco de dados
    cursor.execute("INSERT INTO tickets (user_id, channel_id, status) VALUES (?, ?, ?)", (user.id, ticket_channel.id, "aberto"))
    conn.commit()

    await ticket_channel.send(f"Ticket aberto por {user.mention}. Aguarde a equipe de suporte.")

    await interaction.response.send_message(f"Seu ticket foi criado: {ticket_channel.mention}", ephemeral=True)

# Comando para fechar um ticket
@bot.tree.command(name="fechar", description="Fecha o ticket atual")
async def fechar(interaction: discord.Interaction):
    channel = interaction.channel

    # Verifica se o canal está registrado como um ticket
    cursor.execute("SELECT * FROM tickets WHERE channel_id = ? AND status = ?", (channel.id, "aberto"))
    ticket = cursor.fetchone()

    if not ticket:
        await interaction.response.send_message("Este canal não é um ticket aberto.", ephemeral=True)
        return

    # Atualizar status no banco de dados
    cursor.execute("UPDATE tickets SET status = ? WHERE channel_id = ?", ("fechado", channel.id))
    conn.commit()

    await interaction.response.send_message("O ticket será fechado em 5 segundos.", ephemeral=True)
    
    await channel.send("Este ticket foi fechado. O canal será excluído em breve.")
    await discord.utils.sleep_until(discord.utils.utcnow().replace(second=channel.created_at.second + 5))
    await channel.delete()

# Rodar o bot
bot.run(TOKEN)