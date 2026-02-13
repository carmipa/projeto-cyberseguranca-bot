"""
Admin cog - Administrative commands (/forcecheck).
"""
import discord
from discord.ext import commands
from discord import app_commands
import logging

log = logging.getLogger("CyberIntel")


class AdminCog(commands.Cog):
    """Cog com comandos administrativos."""
    
    def __init__(self, bot, run_scan_once_func):
        self.bot = bot
        self.run_scan_once = run_scan_once_func
    
    @app_commands.command(name="forcecheck", description="Força varredura imediata de feeds.")
    @app_commands.checks.has_permissions(administrator=True)
    async def forcecheck(self, interaction: discord.Interaction):
        """Força uma varredura imediata sem abrir o dashboard."""
        try:
            await interaction.response.defer(ephemeral=True)
            
            if not self.run_scan_once:
                await interaction.followup.send("❌ Função de scan não disponível.", ephemeral=True)
                return
            
            await self.run_scan_once(trigger="forcecheck")
            await interaction.followup.send("✅ Varredura forçada concluída!", ephemeral=True)
        except Exception as e:
            log.exception(f"❌ Erro crítico em /forcecheck: {e}")
            try:
                if interaction.response.is_done():
                    await interaction.followup.send("❌ Falha ao executar varredura.", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Falha ao executar varredura.", ephemeral=True)
            except:
                pass
    
    @app_commands.command(name="post_latest", description="Força a postagem da notícia mais recente (ignora cache)")
    @app_commands.checks.has_permissions(administrator=True)
    async def post_latest(self, interaction: discord.Interaction):
        """Força a postagem de 1 notícia ignorando se ela já foi postada."""
        try:
            await interaction.response.defer(ephemeral=True)
            
            if not self.run_scan_once:
                await interaction.followup.send("❌ Função de scan não disponível.", ephemeral=True)
                return
            
            await interaction.followup.send("🚀 Buscando notícia mais recente (Bypass Mode)...", ephemeral=True)
            await self.run_scan_once(trigger="post_latest", bypass_cache=True)
            await interaction.followup.send("✅ Operação finalizada. Verifique o canal SOC.", ephemeral=True)
        except Exception as e:
            log.exception(f"❌ Erro em /post_latest: {e}")
            try:
                await interaction.followup.send(f"❌ Falha: {str(e)[:200]}", ephemeral=True)
            except:
                pass

    
    # Error handlers para slash commands devem ser registrados no tree
    # Por enquanto, tratamento de erro está dentro do próprio comando


async def setup(bot):
    """Setup function para carregar o cog."""
    # O bound_scan foi injetado no bot no main.py
    run_scan = getattr(bot, "run_scan_once", None)
    await bot.add_cog(AdminCog(bot, run_scan))
