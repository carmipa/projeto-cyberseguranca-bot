import discord
from discord import app_commands
from discord.ext import commands
import logging
from settings import OWNER_ID

logger = logging.getLogger("CyberIntel_Guard")

class ActiveDefense(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Lista negra de IDs de usuários (na VPS você pode persistir isso no JSON)
        self.blacklist = set()

    async def log_intruder(self, user: discord.User):
        """Registra a tentativa de intrusão com a frase personalizada"""
        logger.warning(f"🚨 TENTATIVA DE INTRUSÃO DETECTADA: {user.name} (ID: {user.id})")
        logger.warning("MENSAGEM: 'O malandro se acha malandro até achar um malandro melhor.'")

    @app_commands.command(name="admin_panel", description="[RESTRITO] Acesso ao painel de administração")
    async def admin_panel(self, interaction: discord.Interaction):
        """
        Comando Honeypot.
        Se não for o Dono, loga como intrusão e nega acesso.
        """
        # Verifica se o usuário é o dono configurado
        if interaction.user.id != OWNER_ID:
            self.blacklist.add(interaction.user.id)
            await self.log_intruder(interaction.user)
            
            # Resposta para o "malandro"
            embed = discord.Embed(
                title="❌ ACESSO NEGADO",
                description="**Sistema de Defesa Ativa acionado.**\n\n'O malandro se acha malandro até achar um malandro melhor.'",
                color=0xFF0000
            )
            # Imagem opcional (Gundam apontando arma ou similar, mas manter simples por enquanto)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("✅ **Bem-vindo, Comandante.** Sistemas operacionais.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ActiveDefense(bot))
