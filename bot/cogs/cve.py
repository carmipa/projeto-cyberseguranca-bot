import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.services.cveService import get_cve_details

log = logging.getLogger("CyberIntel")

class CVE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cve", description="Busca detalhes de uma vulnerabilidade específica (Ex: CVE-2021-44228)")
    @app_commands.describe(cve_id="O ID da CVE (ex: CVE-2021-44228)")
    async def cve(self, interaction: discord.Interaction, cve_id: str):
        # Audit Log
        user = interaction.user
        log.info(f"AUDIT: Comando /cve {cve_id} solicitado por {user}")

        await interaction.response.defer()
        
        # Formata para garantir uppercase
        cve_id = cve_id.strip().upper()
        
        # Validação básica de formato
        if not cve_id.startswith("CVE-"):
            await interaction.followup.send("❌ Formato inválido. Use: `CVE-ANO-NUMERO` (Ex: CVE-2023-1234)")
            return

        details = await get_cve_details(cve_id)
        
        if details:
            # Define cor baseada na criticidade (CVSS)
            try:
                cvss_score = float(details['cvss'])
                if cvss_score >= 9.0:
                    color = 0x000000 # Critical - Black/Dark
                elif cvss_score >= 7.0:
                    color = 0xff0000 # High - Red
                elif cvss_score >= 4.0:
                    color = 0xffff00 # Medium - Yellow
                else:
                    color = 0x00ff00 # Low - Green
            except:
                color = 0x808080 # Unknown - Grey
            
            embed = discord.Embed(
                title=f"🛡️ Vulnerabilidade: {details['id']}",
                description=details['summary'],
                color=color
            )
            
            embed.add_field(name="⚖️ Score CVSS", value=f"**{details['cvss']}**", inline=True)
            embed.add_field(name="📅 Publicado em", value=details['published'], inline=True)
            
            if details.get('vulnerable_product'):
                prods = "\n".join([f"`{p}`" for p in details['vulnerable_product']])
                embed.add_field(name="⚠️ Produtos Afetados (Amostra)", value=prods, inline=False)
            
            if details['references']:
                refs = "\n".join([f"• {r}" for r in details['references']])
                embed.add_field(name="🔗 Referências", value=refs[:1024], inline=False) # Limite do Discord
                
            embed.set_footer(text="Fonte: CIRCL.lu CVE Search | CyberIntel System")
            
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ Não encontrei detalhes para a CVE `{cve_id}`. Verifique se o código está correto.")

async def setup(bot):
    await bot.add_cog(CVE(bot))
