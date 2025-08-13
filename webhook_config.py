#!/usr/bin/env python3
"""
Script para configurar webhooks do sistema de monitoramento.
Este script permite configurar Discord para receber alertas.
"""

import json
import os
import sys

def configure_discord():
    """Configura webhook do Discord."""
    print("\n=== Configuração do Discord ===")
    webhook_url = "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print(f"🔗 Usando URL: {webhook_url}")
    
    return {
        "type": "discord",
        "url": webhook_url,
    }

def update_monitor_script(config):
    """Atualiza o script de monitoramento com a nova configuração."""
    script_path = "/home/ubuntu/monitor_site.py"
    
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        
        start_marker = 'WEBHOOK_CONFIG = {'
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print("❌ Não foi possível encontrar a configuração no script!")
            return False
        
        # Substituição direta
        new_config = f"""WEBHOOK_CONFIG = {{
    "type": "{config['type']}",
    "url": "{config['url']}",
}}"""
        
        end_idx = content.find("}", start_idx) + 1
        new_content = content[:start_idx] + new_config + content[end_idx:]
        
        with open(script_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Configuração atualizada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar o script: {e}")
        return False

def test_webhook(config):
    """Testa o webhook configurado."""
    print("\n🧪 Testando webhook...")
    
    sys.path.insert(0, '/home/ubuntu')
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("monitor_site", "/home/ubuntu/monitor_site.py")
        monitor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(monitor_module)
        
        test_message = "🧪 **Teste de Configuração**\n\nEste é um teste do sistema de monitoramento."
        
        if monitor_module.send_alert(test_message):
            print("✅ Teste realizado com sucesso! Verifique se recebeu a mensagem.")
        else:
            print("❌ Falha no teste. Verifique a configuração.")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

def main():
    """Função principal."""
    print("🔧 Configurador de Webhooks - Sistema de Monitoramento")
    print("=" * 60)
    
    print("\nEscolha o serviço para receber para receber alertas:")
    print("1. Discord")
    print("2. Sair")
    
    choice = input("\nDigite sua escolha (1-2): ").strip()
    
    config = None
    
    if choice == "1":
        config = configure_discord()
    elif choice == "2":
        print("👋 Saindo...")
        return
    else:
        print("❌ Opção inválida!")
        return
    
    if config is None:
        print("❌ Configuração cancelada.")
        return
    
    if update_monitor_script(config):
        test = input("\n🧪 Deseja testar a configuração? (s/n): ").strip().lower()
        if test in ['s', 'sim', 'y', 'yes']:
            test_webhook(config)
        
        print("\n✅ Configuração concluída!")
    else:
        print("❌ Falha na configuração.")

if __name__ == "__main__":
    main()
