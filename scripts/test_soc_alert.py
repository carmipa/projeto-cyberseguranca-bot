import requests
from datetime import datetime
import sys

# Simulação de um alerta crítico de Log4Shell
fake_cve = {
    "title": "CRITICAL: Remote Code Execution found in Log4j (CVE-2021-44228)",
    "link": "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source": "NIST / Mitre",
    "cvss": "10.0"
}

# Envia para o Node-RED
try:
    print(f"Attempting to connect to Node-RED at http://localhost:1880/cyber-intel...")
    response = requests.post("http://localhost:1880/cyber-intel", json=fake_cve, timeout=5)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("🛡️ Alerta de teste enviado com sucesso ao SOC Dashboard!")
    else:
        print(f"⚠️ Recebido status code inesperado: {response.status_code}")
except Exception as e:
    print(f"❌ Falha ao enviar alerta: {e}")
    sys.exit(1)
