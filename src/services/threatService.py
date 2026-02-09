import aiohttp
import logging
from typing import Dict, Any, Optional
from settings import URLSCAN_API_KEY, OTX_API_KEY, VT_API_KEY

log = logging.getLogger("CyberIntel_ThreatService")

class ThreatService:
    """
    Serviço centralizado para consultas de Threat Intelligence
    (URLScan, AlienVault OTX, VirusTotal).
    """

    @staticmethod
    async def scan_url_urlscan(url_to_scan: str) -> Optional[Dict[str, Any]]:
        """
        Submete uma URL para análise no URLScan.io
        """
        if not URLSCAN_API_KEY:
            log.warning("URLScan API Key não configurada.")
            return None
        
        endpoint = "https://urlscan.io/api/v1/scan/"
        headers = {
            "API-Key": URLSCAN_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "url": url_to_scan,
            "visibility": "public"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(endpoint, headers=headers, json=data, timeout=30) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    elif resp.status == 429:
                        log.warning("URLScan Rate Limit atingido.")
                    else:
                        log.error(f"URLScan erro: {resp.status}")
        except Exception as e:
            log.error(f"Erro ao conectar URLScan: {e}")
        return None

    @staticmethod
    async def get_urlscan_result(uuid: str) -> Optional[Dict[str, Any]]:
        """Busca o resultado de um scan UUID."""
        if not uuid: return None
        endpoint = f"https://urlscan.io/api/v1/result/{uuid}/"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=30) as resp:
                     if resp.status == 200:
                         return await resp.json()
        except Exception as e:
            log.error(f"Erro ao buscar resultado URLScan: {e}")
        return None

    @staticmethod
    async def get_otx_pulses(limit: int = 5) -> list:
        """
        Busca pulses recentes do AlienVault OTX
        """
        if not OTX_API_KEY:
             return []
        
        endpoint = "https://otx.alienvault.com/api/v1/pulses/subscribed"
        headers = {"X-OTX-API-KEY": OTX_API_KEY}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers, params={"limit": limit}, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("results", [])
                    else:
                        log.warning(f"OTX retornou status {resp.status}")
        except Exception as e:
             log.error(f"Erro ao consultar OTX: {e}")
        return []

    @staticmethod
    async def check_vt_reputation(url: str) -> Dict[str, Any]:
        """
        Checa reputação no VirusTotal (Scan URL)
        """
        if not VT_API_KEY:
            return {}
            
        endpoint = "https://www.virustotal.com/api/v3/urls"
        headers = {"x-apikey": VT_API_KEY}
        data = {"url": url}

        try:
            async with aiohttp.ClientSession() as session:
                # 1. Submeter
                async with session.post(endpoint, headers=headers, data=data, timeout=30) as resp:
                    if resp.status != 200:
                        return {"error": f"VT submit error {resp.status}"}
                    submit_data = await resp.json()
                
                # O resultado do POST é um ID de análise, não o report direto.
                # Para reputação imediata de algo já scanneado, o endpoint é GET /urls/{id_base64}
                # Mas aqui estamos forçando um novo scan.
                # Para simplificar, retornamos o ID para consulta posterior ou implementamos a espera.
                return submit_data
                
        except Exception as e:
             log.error(f"Erro ao consultar VT: {e}")
             return {"error": str(e)}
