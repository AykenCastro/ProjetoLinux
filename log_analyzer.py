#!/usr/bin/env python3
"""
Analisador de Logs do Projeto Linux
Analisa logs do Nginx e do sistema de monitoramento para gerar relatórios.
"""

import re
import json
import datetime
from collections import defaultdict, Counter
from pathlib import Path

def analyze_nginx_access_log(log_path="/var/log/nginx/projeto-linux.access.log"):
    """
    Analisa o log de acesso do Nginx.
    
    Args:
        log_path: Caminho para o arquivo de log
        
    Returns:
        Dict com estatísticas do log
    """
    stats = {
        "total_requests": 0,
        "unique_ips": set(),
        "status_codes": Counter(),
        "user_agents": Counter(),
        "hourly_requests": defaultdict(int),
        "daily_requests": defaultdict(int),
        "top_pages": Counter(),
        "errors": []
    }
    
    # Padrão para log do Nginx (formato padrão)
    log_pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" '
        r'(?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                match = log_pattern.match(line.strip())
                if match:
                    data = match.groupdict()
                    
                    stats["total_requests"] += 1
                    stats["unique_ips"].add(data["ip"])
                    stats["status_codes"][data["status"]] += 1
                    stats["user_agents"][data["user_agent"]] += 1
                    stats["top_pages"][data["path"]] += 1
                    
                    # Parse datetime
                    try:
                        dt = datetime.datetime.strptime(data["datetime"], "%d/%b/%Y:%H:%M:%S %z")
                        hour_key = dt.strftime("%Y-%m-%d %H:00")
                        day_key = dt.strftime("%Y-%m-%d")
                        
                        stats["hourly_requests"][hour_key] += 1
                        stats["daily_requests"][day_key] += 1
                        
                        # Verifica se é erro
                        if int(data["status"]) >= 400:
                            stats["errors"].append({
                                "timestamp": dt.isoformat(),
                                "ip": data["ip"],
                                "status": data["status"],
                                "path": data["path"],
                                "user_agent": data["user_agent"]
                            })
                    except ValueError:
                        pass
                        
    except FileNotFoundError:
        print(f"Arquivo de log não encontrado: {log_path}")
    except Exception as e:
        print(f"Erro ao analisar log: {e}")
    
    # Converte set para lista para serialização JSON
    stats["unique_ips"] = list(stats["unique_ips"])
    
    return stats

def analyze_monitoring_log(log_path="/var/log/monitoramento.log"):
    """
    Analisa o log do sistema de monitoramento.
    
    Args:
        log_path: Caminho para o arquivo de log
        
    Returns:
        Dict com estatísticas do monitoramento
    """
    stats = {
        "total_checks": 0,
        "successful_checks": 0,
        "failed_checks": 0,
        "alerts_sent": 0,
        "average_response_time": 0,
        "response_times": [],
        "errors": [],
        "uptime_percentage": 0,
        "downtime_events": []
    }
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if "Site OK" in line:
                    stats["total_checks"] += 1
                    stats["successful_checks"] += 1
                    
                    # Extrai tempo de resposta
                    time_match = re.search(r'Tempo: ([\d.]+)s', line)
                    if time_match:
                        response_time = float(time_match.group(1))
                        stats["response_times"].append(response_time)
                
                elif "Site com problema" in line or "Erro ao acessar" in line:
                    stats["total_checks"] += 1
                    stats["failed_checks"] += 1
                    
                    # Extrai timestamp do erro
                    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if timestamp_match:
                        stats["downtime_events"].append({
                            "timestamp": timestamp_match.group(1),
                            "error": line.strip()
                        })
                
                elif "Alerta" in line and "enviado" in line:
                    stats["alerts_sent"] += 1
                    
    except FileNotFoundError:
        print(f"Arquivo de log não encontrado: {log_path}")
    except Exception as e:
        print(f"Erro ao analisar log de monitoramento: {e}")
    
    # Calcula estatísticas
    if stats["response_times"]:
        stats["average_response_time"] = sum(stats["response_times"]) / len(stats["response_times"])
    
    if stats["total_checks"] > 0:
        stats["uptime_percentage"] = (stats["successful_checks"] / stats["total_checks"]) * 100
    
    return stats

def generate_report():
    """
    Gera um relatório completo dos logs.
    
    Returns:
        Dict com o relatório completo
    """
    print("🔍 Analisando logs...")
    
    nginx_stats = analyze_nginx_access_log()
    monitoring_stats = analyze_monitoring_log()
    
    report = {
        "generated_at": datetime.datetime.now().isoformat(),
        "nginx": nginx_stats,
        "monitoring": monitoring_stats,
        "summary": {
            "total_web_requests": nginx_stats["total_requests"],
            "unique_visitors": len(nginx_stats["unique_ips"]),
            "monitoring_uptime": monitoring_stats["uptime_percentage"],
            "total_monitoring_checks": monitoring_stats["total_checks"],
            "alerts_sent": monitoring_stats["alerts_sent"]
        }
    }
    
    return report

def print_summary_report(report):
    """
    Imprime um resumo do relatório.
    
    Args:
        report: Relatório gerado pela função generate_report
    """
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE LOGS - PROJETO LINUX")
    print("="*60)
    
    print(f"\n🕒 Gerado em: {report['generated_at']}")
    
    print("\n🌐 ESTATÍSTICAS DO SERVIDOR WEB:")
    print(f"   • Total de requisições: {report['nginx']['total_requests']}")
    print(f"   • Visitantes únicos: {len(report['nginx']['unique_ips'])}")
    print(f"   • Códigos de status mais comuns:")
    for status, count in report['nginx']['status_codes'].most_common(5):
        print(f"     - {status}: {count} requisições")
    
    if report['nginx']['top_pages']:
        print(f"   • Páginas mais acessadas:")
        for page, count in report['nginx']['top_pages'].most_common(5):
            print(f"     - {page}: {count} acessos")
    
    print("\n📊 ESTATÍSTICAS DO MONITORAMENTO:")
    print(f"   • Total de verificações: {report['monitoring']['total_checks']}")
    print(f"   • Verificações bem-sucedidas: {report['monitoring']['successful_checks']}")
    print(f"   • Verificações com falha: {report['monitoring']['failed_checks']}")
    print(f"   • Uptime: {report['monitoring']['uptime_percentage']:.2f}%")
    print(f"   • Tempo médio de resposta: {report['monitoring']['average_response_time']:.3f}s")
    print(f"   • Alertas enviados: {report['monitoring']['alerts_sent']}")
    
    if report['monitoring']['downtime_events']:
        print(f"\n⚠️  EVENTOS DE INDISPONIBILIDADE:")
        for event in report['monitoring']['downtime_events'][-5:]:  # Últimos 5
            print(f"   • {event['timestamp']}: {event['error']}")
    
    if report['nginx']['errors']:
        print(f"\n❌ ERROS HTTP RECENTES:")
        for error in report['nginx']['errors'][-5:]:  # Últimos 5
            print(f"   • {error['timestamp']}: {error['status']} - {error['path']} ({error['ip']})")

def save_report_json(report, filename=None):
    """
    Salva o relatório em formato JSON.
    
    Args:
        report: Relatório a ser salvo
        filename: Nome do arquivo (opcional)
    """
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/home/ubuntu/relatorio_logs_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Relatório salvo em: {filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {e}")

def main():
    """Função principal."""
    print("📋 Analisador de Logs - Projeto Linux")
    
    # Gera o relatório
    report = generate_report()
    
    # Exibe o resumo
    print_summary_report(report)
    
    # Salva o relatório completo
    save_report_json(report)
    
    print("\n✅ Análise concluída!")

if __name__ == "__main__":
    main()

