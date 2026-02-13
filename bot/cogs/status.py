"""
Status cog - /status command to show bot statistics.
"""
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import logging

from core.stats import stats
from settings import LOOP_MINUTES

log = logging.getLogger("CyberIntel")



class ScanButton(discord.ui.View):
    def __init__(self, run_scan_func):
        super().__init__(timeout=None)
        self.run_scan = run_scan_func

    @discord.ui.button(label="Verificar Agora", style=discord.ButtonStyle.primary, emoji="🔄", custom_id="status_scan_now")
    async def scan_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        try:
            # Feedback imediato
            await interaction.followup.send("🔎 Iniciando verificação manual...", ephemeral=True)
            
            # Executa o scan
            await self.run_scan(trigger="manual_button")
            
            # Confirmação
            await interaction.followup.send("✅ Verificação concluída! Se houver notícias novas, elas foram enviadas para o canal.", ephemeral=True)
        except Exception as e:
            log.exception(f"❌ Erro no botão scan_now: {e}")
            try:
                await interaction.followup.send(f"❌ Erro ao verificar: {str(e)[:200]}", ephemeral=True)
            except Exception as send_error:
                log.error(f"❌ Falha ao enviar mensagem de erro no scan_now: {send_error}")


class StatusCog(commands.Cog):
    """Cog com comando de status do bot."""
    
    def __init__(self, bot, run_scan_once_func):
        self.bot = bot
        self.run_scan_once = run_scan_once_func
    
    @app_commands.command(name="status", description="Mostra estatísticas do bot CyberIntel.")
    async def status(self, interaction: discord.Interaction):
        """Exibe estatísticas e status atual do bot."""
        try:
            await interaction.response.defer(ephemeral=True) # Fix timeout
            
            # Calcula próxima varredura
            next_scan = datetime.now() + timedelta(minutes=LOOP_MINUTES)
            next_scan_ts = int(next_scan.timestamp())
            
            embed = discord.Embed(
                title="🔐 Status do CyberIntel Bot",
                color=discord.Color.from_rgb(0, 255, 64),
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="⏰ Uptime",
                value=stats.format_uptime(),
                inline=True
            )
            
            embed.add_field(
                name="📡 Varreduras",
                value=f"{stats.scans_completed}",
                inline=True
            )
            
            embed.add_field(
                name="📰 Notícias Enviadas",
                value=f"{stats.news_posted}",
                inline=True
            )
            
            embed.add_field(
                name="📦 Cache Hits Total",
                value=f"{stats.cache_hits_total}",
                inline=True
            )
            
            if stats.last_scan_time:
                last_scan_str = f"<t:{int(stats.last_scan_time.timestamp())}:R>"
            else:
                last_scan_str = "Nenhuma ainda"
            
            embed.add_field(
                name="🕐 Última Varredura",
                value=last_scan_str,
                inline=True
            )
            
            embed.add_field(
                name="⏳ Próxima Varredura",
                value=f"<t:{next_scan_ts}:R>",
                inline=True
            )
            
            embed.set_footer(text=f"NetRunner v1.0 | Intervalo: {LOOP_MINUTES} min")
            
            # Adiciona o botão de scan
            view = ScanButton(self.run_scan_once)
            
            # EPHEMERAL: Apenas o usuário que digitou vê a mensagem.
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            log.exception(f"❌ Erro no comando /status: {e}")
            try:
                await interaction.followup.send("❌ Erro ao exibir status.", ephemeral=True)
            except Exception as send_error:
                log.error(f"❌ Falha ao enviar mensagem de erro no /status: {send_error}")

    @app_commands.command(name="now", description="Força uma verificação imediata de notícias.")
    @app_commands.checks.has_permissions(administrator=True)
    async def now(self, interaction: discord.Interaction):
        """Verifica notícias imediatamente."""
        try:
            await interaction.response.defer(ephemeral=True)
            
            if not self.run_scan_once:
                await interaction.followup.send("❌ Função de scan não disponível.", ephemeral=True)
                return
            
            await interaction.followup.send("🚀 Iniciando varredura manual (comando /now)...", ephemeral=True)
            await self.run_scan_once(trigger="command_now")
            await interaction.followup.send("✅ Scan finalizado.", ephemeral=True)
        except Exception as e:
            log.exception(f"❌ Erro no comando /now: {e}")
            try:
                await interaction.followup.send(f"❌ Erro: {str(e)[:200]}", ephemeral=True)
            except Exception as send_error:
                log.error(f"❌ Falha ao enviar mensagem de erro no /now: {send_error}")


async def setup(bot):
    """Setup function para carregar o cog."""
    # O bound_scan foi injetado no bot no main.py
    run_scan = getattr(bot, "run_scan_once", None)
    await bot.add_cog(StatusCog(bot, run_scan))
