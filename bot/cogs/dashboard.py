import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import logging

log = logging.getLogger("CyberIntel")

class Dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dashboard_url = "http://localhost:1880/ui"
        self.nodered_internal_url = "http://nodered:1880" 

    async def check_nodered_health(self):
        """Verifica se o container do Node-RED está respondendo"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.nodered_internal_url, timeout=2) as resp:
                    return resp.status == 200
        except Exception as e:
            log.warning(f"Node-RED Health Check falhou: {e}")
            return False

    @app_commands.command(name="dashboard", description="Acessa o SOC Dashboard em tempo real")
    async def dashboard(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        is_online = await self.check_nodered_health()
        
        embed = discord.Embed(
            title="🛡️ CyberIntel SOC Dashboard",
            color=0x00ffcc if is_online else 0xff0000
        )
        
        view = None
        if is_online:
            embed.description = "Painel de monitoramento operacional. Clique no botão abaixo para abrir no seu monitor secundário."
            embed.add_field(name="Status do Serviço", value="🟢 ONLINE", inline=True)
            embed.add_field(name="Visualização", value="Real-Time Web", inline=True)
            embed.add_field(name="🔒 Acesso Seguro", value="Requer Túnel SSH (Porta 1880)", inline=False)
            
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Abrir Dashboard", url=self.dashboard_url, style=discord.ButtonStyle.link))
        else:
            embed.description = "⚠️ O serviço de Dashboard (Node-RED) parece estar offline."
            embed.add_field(name="Status", value="🔴 OFFLINE", inline=True)
            embed.add_field(name="Ação Requerida", value="Verifique o container no Docker Desktop.", inline=False)

        embed.set_footer(text=f"Requisitado por: {interaction.user.name} | Setup: Desktop-Ultrawide")
        
        await interaction.followup.send(embed=embed, view=view)

async def setup(bot, run_scan_once=None):
    # run_scan_once is accepted for compatibility with main.py but not used herein
    await bot.add_cog(Dashboard(bot))
