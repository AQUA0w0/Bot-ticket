import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# 🔹 Carregar variáveis do .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# 🔹 Criar bot temporário apenas para registrar comandos
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    try:
        print("🔄 Removendo comandos antigos...")
        bot.tree.clear_commands(guild=discord.Object(id=GUILD_ID))  # Limpa comandos antigos

        print("🔄 Criando comando `/ticket`...")
        async def ticket_callback(interaction: discord.Interaction):
            await interaction.response.send_message("🎫 Painel de tickets criado!", ephemeral=True)

        ticket_command = app_commands.Command(
            name="ticket",
            description="🎫 Criar painel para abrir tickets",
            callback=ticket_callback
        )
        
        bot.tree.add_command(ticket_command)

        print("🔄 Sincronizando comandos Slash...")
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Comandos Slash sincronizados: {len(synced)}")

    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos: {e}")

    await bot.close()

bot.run(TOKEN)