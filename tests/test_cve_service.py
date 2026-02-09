
import sys
import os
import asyncio

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.cveService import get_cve_details

async def test_cve_service():
    cve_id = "CVE-2021-44228" # Log4Shell
    print(f"Testando consulta para {cve_id}...")
    
    details = await get_cve_details(cve_id)
    
    if not details:
        print("❌ Falha ao buscar detalhes da CVE.")
        return

    print("✅ Detalhes recebidos:")
    print(f"ID: {details['id']}")
    print(f"CVSS: {details['cvss']}")
    print(f"Resumo: {details['summary'][:100]}...")
    print(f"Referências: {len(details['references'])}")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_cve_service())
