import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.services.newsService import get_latest_security_news

log = logging.getLogger("CyberIntel")

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Busca as últimas notícias de Cyber Segurança (The Hacker News, BleepingComputer)")
    async def news(self, interaction: discord.Interaction):
        # Audit Log
        user = interaction.user
        log.info(f"AUDIT: Comando /news solicitado por {user} (ID: {user.id}) em {interaction.guild} (ID: {interaction.guild_id if interaction.guild else 'DM'})")

        await interaction.response.defer()

        try:
            news_items = get_latest_security_news()
            
            if not news_items:
                await interaction.followup.send("❌ Não foi possível obter notícias no momento.")
                return

            embed = discord.Embed(
                title="🛡️ CyberIntel Feed - Últimas Notícias",
                description="Monitoramento de Threat Intelligence em tempo real.",
                color=0x00ffcc # Cyber Green
            )
            
            for item in news_items:
                embed.add_field(
                    name=item['title'],
                    value=f"{item['summary']}\n[Ler mais]({item['link']})",
                    inline=False
                )

            embed.set_footer(text="Fontes: The Hacker News, BleepingComputer | CyberIntel System")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            log.error(f"Erro ao executar comando /news: {e}")
            await interaction.followup.send("❌ Ocorreu um erro ao buscar as notícias.")

async def setup(bot):
    await bot.add_cog(News(bot))
