#!/bin/bash

# Script de Backup - Projeto Linux
# Cria backup completo de todos os arquivos e configurações do projeto

# Configurações
BACKUP_BASE_DIR="/backup"
PROJECT_NAME="projeto-linux"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE_DIR/${PROJECT_NAME}_$TIMESTAMP"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar se é executado como root para alguns arquivos
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        warning "Script não está sendo executado como root."
        warning "Alguns arquivos podem não ser copiados devido a permissões."
        warning "Execute com sudo para backup completo."
        echo
    fi
}

# Criar diretório de backup
create_backup_dir() {
    log "Criando diretório de backup: $BACKUP_DIR"
    
    if ! mkdir -p "$BACKUP_DIR"; then
        error "Falha ao criar diretório de backup"
        exit 1
    fi
    
    success "Diretório de backup criado"
}

# Backup de arquivos de configuração do Nginx
backup_nginx_config() {
    log "Fazendo backup das configurações do Nginx..."
    
    local nginx_backup_dir="$BACKUP_DIR/nginx"
    mkdir -p "$nginx_backup_dir"
    
    # Configuração do site
    if [[ -f "/etc/nginx/sites-available/projeto-linux" ]]; then
        cp "/etc/nginx/sites-available/projeto-linux" "$nginx_backup_dir/"
        success "Configuração do site copiada"
    else
        warning "Arquivo de configuração do site não encontrado"
    fi
    
    # Configuração principal do Nginx (para referência)
    if [[ -f "/etc/nginx/nginx.conf" ]]; then
        cp "/etc/nginx/nginx.conf" "$nginx_backup_dir/"
        success "Configuração principal do Nginx copiada"
    fi
}

# Backup dos arquivos web
backup_web_files() {
    log "Fazendo backup dos arquivos web..."
    
    local web_backup_dir="$BACKUP_DIR/web"
    mkdir -p "$web_backup_dir"
    
    if [[ -d "/var/www/html/projeto-linux" ]]; then
        cp -r "/var/www/html/projeto-linux" "$web_backup_dir/"
        success "Arquivos web copiados"
    else
        warning "Diretório web não encontrado"
    fi
}

# Backup dos scripts de monitoramento
backup_monitoring_scripts() {
    log "Fazendo backup dos scripts de monitoramento..."
    
    local scripts_backup_dir="$BACKUP_DIR/scripts"
    mkdir -p "$scripts_backup_dir"
    
    # Scripts Python
    for script in "monitor_site.py" "webhook_config.py" "log_analyzer.py"; do
        if [[ -f "/home/ubuntu/$script" ]]; then
            cp "/home/ubuntu/$script" "$scripts_backup_dir/"
            success "Script $script copiado"
        else
            warning "Script $script não encontrado"
        fi
    done
    
    # Este script de backup
    if [[ -f "/home/ubuntu/scripts_backup.sh" ]]; then
        cp "/home/ubuntu/scripts_backup.sh" "$scripts_backup_dir/"
        success "Script de backup copiado"
    fi
}

# Backup das configurações do systemd
backup_systemd_config() {
    log "Fazendo backup das configurações do systemd..."
    
    local systemd_backup_dir="$BACKUP_DIR/systemd"
    mkdir -p "$systemd_backup_dir"
    
    # Arquivos do serviço de monitoramento
    for file in "monitor-site.service" "monitor-site.timer"; do
        if [[ -f "/etc/systemd/system/$file" ]]; then
            cp "/etc/systemd/system/$file" "$systemd_backup_dir/"
            success "Arquivo $file copiado"
        else
            warning "Arquivo $file não encontrado"
        fi
    done
}

# Backup das configurações de logrotate
backup_logrotate_config() {
    log "Fazendo backup das configurações de logrotate..."
    
    local logrotate_backup_dir="$BACKUP_DIR/logrotate"
    mkdir -p "$logrotate_backup_dir"
    
    if [[ -f "/etc/logrotate.d/projeto-linux" ]]; then
        cp "/etc/logrotate.d/projeto-linux" "$logrotate_backup_dir/"
        success "Configuração de logrotate copiada"
    else
        warning "Configuração de logrotate não encontrada"
    fi
}

# Backup dos logs
backup_logs() {
    log "Fazendo backup dos logs..."
    
    local logs_backup_dir="$BACKUP_DIR/logs"
    mkdir -p "$logs_backup_dir"
    
    # Logs do monitoramento
    if [[ -f "/var/log/monitoramento.log" ]]; then
        cp "/var/log/monitoramento.log" "$logs_backup_dir/"
        success "Log de monitoramento copiado"
    fi
    
    # Logs do Nginx
    for log_file in "/var/log/nginx/projeto-linux.access.log" "/var/log/nginx/projeto-linux.error.log"; do
        if [[ -f "$log_file" ]]; then
            cp "$log_file" "$logs_backup_dir/"
            success "Log $(basename $log_file) copiado"
        fi
    done
    
    # Relatórios de análise de logs
    for report in /home/ubuntu/relatorio_logs_*.json; do
        if [[ -f "$report" ]]; then
            cp "$report" "$logs_backup_dir/"
            success "Relatório $(basename $report) copiado"
        fi
    done
}

# Backup da documentação
backup_documentation() {
    log "Fazendo backup da documentação..."
    
    local docs_backup_dir="$BACKUP_DIR/documentation"
    mkdir -p "$docs_backup_dir"
    
    # Arquivos de documentação
    for doc in "README.md" "INSTALL.md" "todo.md"; do
        if [[ -f "/home/ubuntu/$doc" ]]; then
            cp "/home/ubuntu/$doc" "$docs_backup_dir/"
            success "Documentação $doc copiada"
        fi
    done
}

# Criar arquivo de informações do backup
create_backup_info() {
    log "Criando arquivo de informações do backup..."
    
    local info_file="$BACKUP_DIR/backup_info.txt"
    
    cat > "$info_file" << EOF
INFORMAÇÕES DO BACKUP - PROJETO LINUX
=====================================

Data/Hora do Backup: $(date)
Hostname: $(hostname)
Usuário: $(whoami)
Sistema Operacional: $(lsb_release -d | cut -f2)
Kernel: $(uname -r)

VERSÕES DOS COMPONENTES:
- Nginx: $(nginx -v 2>&1 | cut -d' ' -f3)
- Python: $(python3 --version)
- Systemd: $(systemctl --version | head -1)

STATUS DOS SERVIÇOS NO MOMENTO DO BACKUP:
- Nginx: $(systemctl is-active nginx)
- Monitor Timer: $(systemctl is-active monitor-site.timer)

ESTRUTURA DO BACKUP:
- nginx/: Configurações do Nginx
- web/: Arquivos da aplicação web
- scripts/: Scripts de monitoramento e utilitários
- systemd/: Configurações de serviços systemd
- logrotate/: Configurações de rotação de logs
- logs/: Logs atuais do sistema
- documentation/: Documentação do projeto

INSTRUÇÕES DE RESTAURAÇÃO:
1. Copie os arquivos para suas localizações originais
2. Ajuste permissões conforme necessário
3. Recarregue configurações: sudo systemctl daemon-reload
4. Reinicie serviços: sudo systemctl restart nginx monitor-site.timer
5. Teste funcionamento: curl -I http://localhost

COMANDOS ÚTEIS PARA RESTAURAÇÃO:
sudo cp nginx/projeto-linux /etc/nginx/sites-available/
sudo cp -r web/projeto-linux /var/www/html/
cp scripts/* /home/ubuntu/
sudo cp systemd/* /etc/systemd/system/
sudo cp logrotate/projeto-linux /etc/logrotate.d/

EOF

    success "Arquivo de informações criado"
}

# Compactar backup (opcional)
compress_backup() {
    log "Compactando backup..."
    
    local archive_name="${PROJECT_NAME}_${TIMESTAMP}.tar.gz"
    local archive_path="$BACKUP_BASE_DIR/$archive_name"
    
    if tar -czf "$archive_path" -C "$BACKUP_BASE_DIR" "$(basename $BACKUP_DIR)"; then
        success "Backup compactado: $archive_path"
        
        # Remover diretório não compactado
        rm -rf "$BACKUP_DIR"
        success "Diretório temporário removido"
        
        # Mostrar tamanho do arquivo
        local size=$(du -h "$archive_path" | cut -f1)
        log "Tamanho do backup: $size"
    else
        error "Falha ao compactar backup"
    fi
}

# Limpeza de backups antigos (manter apenas os 10 mais recentes)
cleanup_old_backups() {
    log "Limpando backups antigos..."
    
    local backup_count=$(ls -1 "$BACKUP_BASE_DIR"/${PROJECT_NAME}_*.tar.gz 2>/dev/null | wc -l)
    
    if [[ $backup_count -gt 10 ]]; then
        local to_remove=$((backup_count - 10))
        ls -1t "$BACKUP_BASE_DIR"/${PROJECT_NAME}_*.tar.gz | tail -n $to_remove | xargs rm -f
        success "Removidos $to_remove backups antigos"
    else
        log "Nenhum backup antigo para remover (total: $backup_count)"
    fi
}

# Função principal
main() {
    echo
    log "=== INICIANDO BACKUP DO PROJETO LINUX ==="
    echo
    
    check_permissions
    create_backup_dir
    
    backup_nginx_config
    backup_web_files
    backup_monitoring_scripts
    backup_systemd_config
    backup_logrotate_config
    backup_logs
    backup_documentation
    create_backup_info
    
    # Perguntar se quer compactar
    echo
    read -p "Deseja compactar o backup? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        compress_backup
        cleanup_old_backups
    fi
    
    echo
    success "=== BACKUP CONCLUÍDO COM SUCESSO ==="
    log "Localização: $BACKUP_DIR"
    echo
}

# Verificar se o diretório base de backup existe
if [[ ! -d "$BACKUP_BASE_DIR" ]]; then
    log "Criando diretório base de backup: $BACKUP_BASE_DIR"
    sudo mkdir -p "$BACKUP_BASE_DIR"
    sudo chown ubuntu:ubuntu "$BACKUP_BASE_DIR"
fi

# Executar função principal
main

