import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.services.dbService import get_db_stats

log = logging.getLogger("CyberIntel")

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status_db", description="Exibe estatísticas do banco de dados de inteligência")
    async def status_db(self, interaction: discord.Interaction):
        try:
            # Audit Log
            user = interaction.user
            log.info(f"AUDIT: Comando /status_db solicitado por {user} (ID: {user.id})")
            
            total, last_update = get_db_stats()
            
            embed = discord.Embed(
                title="📊 Dashboard de Inteligência - CyberIntel",
                description="Métricas de persistência e monitoramento.",
                color=0x2f3136 # Dark Theme
            )
            
            embed.add_field(name="🗞️ Notícias Processadas", value=f"**{total}**", inline=True)
            embed.add_field(name="🕒 Última Atualização", value=f"`{last_update if last_update else 'N/A'}`", inline=True)
            
            # Status do Banco (técnico)
            embed.add_field(name="🗄️ Storage", value="JSON (File-based)", inline=False)
            
            embed.set_footer(text="CyberIntel System | Database Status")
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            log.exception(f"❌ Erro no comando /status_db: {e}")
            try:
                await interaction.response.send_message("❌ Erro ao exibir estatísticas do banco.", ephemeral=True)
            except Exception as send_error:
                log.error(f"❌ Falha ao enviar mensagem de erro no /status_db: {send_error}")

async def setup(bot):
    await bot.add_cog(Stats(bot))
