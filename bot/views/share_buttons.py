import discord
import urllib.parse

class ShareButtons(discord.ui.View):
    def __init__(self, news_title: str, news_url: str):
        super().__init__()
        
        # Garante que o texto esteja seguro para URL
        safe_title = urllib.parse.quote(news_title)
        safe_url = urllib.parse.quote(news_url)
        safe_text = f"🚨 *Alerta CyberIntel*\n\n{safe_title}\n🔗 {safe_url}"
        safe_text_encoded = urllib.parse.quote(safe_text)
        
        # WhatsApp Button
        self.add_item(discord.ui.Button(
            label="Encaminhar (WhatsApp)", 
            emoji="📱",
            url=f"https://api.whatsapp.com/send?text={safe_text_encoded}",
            style=discord.ButtonStyle.link
        ))
        
        # Email Button (Outlook/System Default)
        # mailto:?subject=...&body=...
        mail_subject = urllib.parse.quote(f"⚠️ CyberIntel Alert: {news_title}")
        mail_body = urllib.parse.quote(f"Prezados,\n\nIdentificamos um alerta de segurança relevante:\n\n{news_title}\n\nLink Original: {news_url}\n\n--\nCyberIntel SOC Bot")
        
        self.add_item(discord.ui.Button(
            label="Reportar por Email", 
            emoji="📧",
            url=f"mailto:?subject={mail_subject}&body={mail_body}",
            style=discord.ButtonStyle.link
        ))
