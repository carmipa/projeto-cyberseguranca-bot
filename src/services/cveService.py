
import aiohttp
import logging

log = logging.getLogger("CyberIntel")

async def get_cve_details(cve_id):
    """
    Consulta detalhes de uma CVE específica via API CIRCL.lu
    Retorna um dicionário com os dados ou None se não encontrar/erro.
    """
    url = f"https://cve.circl.lu/api/cve/{cve_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    # A API do CIRCL retorna null ou objeto vazio as vezes se não achar
                    if data:
                        return {
                            "id": data.get("id", cve_id),
                            "cvss": data.get("cvss", "N/A"),
                            "summary": data.get("summary", "Sem descrição disponível."),
                            "published": data.get("Published", "Data não informada"),
                            "references": data.get("references", [])[:3], # Pega as 3 primeiras refs
                            "vulnerable_product": data.get("vulnerable_product", [])[:3] # Listar alguns produtos afetados
                        }
    except Exception as e:
        log.error(f"Erro ao consultar CVE {cve_id}: {e}")
    
    return None
