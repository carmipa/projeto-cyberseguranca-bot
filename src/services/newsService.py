
import feedparser

def get_latest_security_news():
    # Feeds confiáveis
    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/"
    ]
    
    news_list = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: # Pega as 3 últimas de cada
                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": (entry.description[:200] + "...") if hasattr(entry, 'description') else "Sem resumo disponível."
                })
        except Exception as e:
            print(f"Erro ao ler feed {url}: {e}")
            
    return news_list
