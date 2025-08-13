#!/usr/bin/env python3
"""
Script de Monitoramento de Site
Verifica a disponibilidade do site a cada execução e envia alertas se necessário.
"""

import requests
import datetime
import json
import os
import sys
import logging
from typing import Dict, Any

# Configurações
SITE_URL = "http://localhost"
LOG_FILE = "/var/log/monitoramento.log"
STATUS_FILE = "/tmp/site_status.json"
TIMEOUT = 10  # segundos

# Configuração de webhook (Discord)
# Para Discord: Use um webhook URL do Discord
WEBHOOK_CONFIG = {
    "type": "discord",  # "discord"
    "url": "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXX",  # Cole aqui o webhook URL do Discord
}

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_site_status() -> Dict[str, Any]:
    """
    Verifica o status do site e retorna informações sobre a verificação.
    
    Returns:
        Dict contendo status, código de resposta, tempo de resposta e timestamp
    """
    try:
        start_time = datetime.datetime.now()
        response = requests.get(SITE_URL, timeout=TIMEOUT)
        end_time = datetime.datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        status_info = {
            "timestamp": start_time.isoformat(),
            "url": SITE_URL,
            "status_code": response.status_code,
            "response_time": response_time,
            "is_up": response.status_code == 200,
            "error": None
        }
        
        if response.status_code == 200:
            logger.info(f"Site OK - Status: {response.status_code}, Tempo: {response_time:.2f}s")
        else:
            logger.warning(f"Site com problema - Status: {response.status_code}, Tempo: {response_time:.2f}s")
            
        return status_info
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        status_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "url": SITE_URL,
            "status_code": None,
            "response_time": None,
            "is_up": False,
            "error": error_msg
        }
        
        logger.error(f"Erro ao acessar o site: {error_msg}")
        return status_info

def load_previous_status() -> Dict[str, Any]:
    """
    Carrega o status anterior do arquivo de status.
    
    Returns:
        Dict com o status anterior ou None se não existir
    """
    try:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Erro ao carregar status anterior: {e}")
    
    return {"is_up": True}  # Assume que estava funcionando se não há histórico

def save_current_status(status_info: Dict[str, Any]) -> None:
    """
    Salva o status atual no arquivo de status.
    
    Args:
        status_info: Informações do status atual
    """
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(status_info, f, indent=2)
    except Exception as e:
        logger.error(f"Erro ao salvar status: {e}")

def send_discord_alert(message: str) -> bool:
    """
    Envia alerta via Discord webhook.
    
    Args:
        message: Mensagem a ser enviada
        
    Returns:
        True se enviado com sucesso, False caso contrário
    """
    if not WEBHOOK_CONFIG.get("url"):
        logger.warning("URL do webhook Discord não configurada")
        return False
        
    try:
        payload = {
            "content": message,
            "username": "Monitor do Site",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/2919/2919906.png"
        }
        
        response = requests.post(WEBHOOK_CONFIG["url"], json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info("Alerta enviado via Discord com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar alerta via Discord: {e}")
        return False

def send_alert(message: str) -> bool:
    """
    Envia alerta usando o método configurado.
    
    Args:
        message: Mensagem a ser enviada
        
    Returns:
        True se enviado com sucesso, False caso contrário
    """
    webhook_type = WEBHOOK_CONFIG.get("type", "").lower()
    
    if webhook_type == "discord":
        return send_discord_alert(message)
    else:
        logger.warning(f"Tipo de webhook não suportado: {webhook_type}")
        return False

def format_alert_message(status_info: Dict[str, Any], is_down_alert: bool) -> str:
    """
    Formata a mensagem de alerta.
    
    Args:
        status_info: Informações do status
        is_down_alert: True se é um alerta de site fora do ar
        
    Returns:
        Mensagem formatada
    """
    timestamp = datetime.datetime.fromisoformat(status_info["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
    
    if is_down_alert:
        if status_info["error"]:
            return f"""🚨 **ALERTA: Site Fora do Ar** 🚨

**URL:** {status_info['url']}
**Timestamp:** {timestamp}
**Erro:** {status_info['error']}

O site não está respondendo. Verifique o servidor imediatamente!"""
        else:
            return f"""🚨 **ALERTA: Site com Problema** 🚨

**URL:** {status_info['url']}
**Timestamp:** {timestamp}
**Status Code:** {status_info['status_code']}
**Tempo de Resposta:** {status_info['response_time']:.2f}s

O site retornou um código de erro. Verifique o servidor!"""
    else:
        return f"""✅ **Site Restaurado** ✅

**URL:** {status_info['url']}
**Timestamp:** {timestamp}
**Status Code:** {status_info['status_code']}
**Tempo de Resposta:** {status_info['response_time']:.2f}s

O site voltou a funcionar normalmente."""

def main():
    """
    Função principal do script de monitoramento.
    """
    logger.info("Iniciando verificação do site...")
    
    # Carrega status anterior
    previous_status = load_previous_status()
    
    # Verifica status atual
    current_status = check_site_status()
    
    # Salva status atual
    save_current_status(current_status)
    
    # Verifica se houve mudança de status
    was_up = previous_status.get("is_up", True)
    is_up = current_status["is_up"]
    
    # Envia alertas apenas quando há mudança de status
    if was_up and not is_up:
        # Site saiu do ar
        message = format_alert_message(current_status, True)
        if send_alert(message):
            logger.info("Alerta de site fora do ar enviado")
        else:
            logger.error("Falha ao enviar alerta de site fora do ar")
            
    elif not was_up and is_up:
        # Site voltou ao ar
        message = format_alert_message(current_status, False)
        if send_alert(message):
            logger.info("Alerta de site restaurado enviado")
        else:
            logger.error("Falha ao enviar alerta de site restaurado")
    
    logger.info("Verificação concluída")

if __name__ == "__main__":
    main()

