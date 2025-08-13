# Projeto Linux - Infraestrutura Web com Monitoramento Automatizado

## Visão Geral

Este projeto implementa uma infraestrutura web completa em ambiente Linux com sistema de monitoramento automatizado.
### Objetivos do Projeto

- **Configurar um servidor web Nginx** funcional e seguro
- **Implementar monitoramento automatizado** com verificações a cada minuto
- **Configurar sistema de alertas** via Discord
- **Estabelecer logging abrangente** para auditoria e troubleshooting
- **Documentar todo o processo** para replicabilidade e manutenção

### Arquitetura da Solução

A infraestrutura implementada consiste nos seguintes componentes principais:

1. **Servidor Web Nginx**: Hospeda uma página HTML responsiva com informações do projeto
2. **Sistema de Monitoramento**: Script Python que verifica a disponibilidade do site
3. **Sistema de Alertas**: Integração com webhooks para notificações automáticas
4. **Sistema de Logs**: Registro detalhado de eventos e métricas de performance
5. **Automação**: Serviços systemd para execução automática e confiável

## Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|---------|
| Ubuntu Linux | 22.04 LTS | Sistema operacional base |
| Nginx | 1.18.0 | Servidor web HTTP |
| Python | 3.11 | Linguagem para scripts de monitoramento |
| Systemd | 249 | Gerenciamento de serviços e timers |
| HTML5/CSS3 | - | Interface web responsiva |
| Logrotate | - | Rotação automática de logs |

## Pré-requisitos

Antes de iniciar a implementação, certifique-se de que o ambiente atende aos seguintes requisitos:

### Requisitos de Sistema

- **Sistema Operacional**: Ubuntu 22.04 LTS ou superior
- **Privilégios**: Acesso sudo para instalação de pacotes e configuração de serviços
- **Conectividade**: Acesso à internet para download de pacotes e webhooks
- **Recursos**: Mínimo de 1GB RAM e 10GB de espaço em disco

### Dependências de Software

As seguintes dependências serão instaladas durante o processo:

- **nginx**: Servidor web HTTP de alta performance
- **python3**: Interpretador Python para scripts de monitoramento
- **python3-requests**: Biblioteca para requisições HTTP
- **curl**: Ferramenta para testes de conectividade
- **systemd**: Sistema de init para gerenciamento de serviços (já incluído no Ubuntu)

## Instalação e Configuração

### Etapa 1: Preparação do Ambiente

Primeiro, atualize o sistema e instale as dependências necessárias:

```bash
# Atualizar lista de pacotes
sudo apt update

# Instalar Nginx e ferramentas essenciais
sudo apt install -y nginx curl python3 python3-pip

# Instalar biblioteca Python para requisições HTTP
pip3 install requests
```

### Etapa 2: Configuração do Servidor Web

#### 2.1 Criação da Estrutura de Diretórios

```bash
# Criar diretório para o projeto
sudo mkdir -p /var/www/html/projeto-linux

# Definir permissões adequadas
sudo chown -R www-data:www-data /var/www/html/projeto-linux
sudo chmod -R 755 /var/www/html/projeto-linux
```

#### 2.2 Criação da Página HTML

A página HTML foi desenvolvida com design responsivo e moderno, incluindo:

- **Interface visual atrativa** com gradientes e efeitos de transparência
- **Informações em tempo real** sobre o status do sistema
- **Design responsivo** compatível com dispositivos móveis
- **Atualização automática** do timestamp via JavaScript

O arquivo `index.html` deve ser colocado em `/var/www/html/projeto-linux/` e contém uma estrutura completa com CSS incorporado e funcionalidades JavaScript para uma experiência de usuário otimizada.

#### 2.3 Configuração do Nginx

Crie um arquivo de configuração específico para o projeto:

```bash
sudo nano /etc/nginx/sites-available/projeto-linux
```

A configuração inclui:

- **Virtual host** dedicado para o projeto
- **Logs específicos** para facilitar o monitoramento
- **Headers de segurança** para proteção básica
- **Cache otimizado** para arquivos estáticos
- **Configurações de performance** adequadas

#### 2.4 Ativação do Site

```bash
# Criar link simbólico para ativar o site
sudo ln -s /etc/nginx/sites-available/projeto-linux /etc/nginx/sites-enabled/

# Remover configuração padrão
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Recarregar configuração
sudo systemctl reload nginx
```

#### 2.5 Configuração do Serviço Systemd

O Nginx já vem configurado como serviço systemd, mas é importante verificar:

```bash
# Verificar se está habilitado para iniciar automaticamente
sudo systemctl is-enabled nginx

# Habilitar se necessário
sudo systemctl enable nginx

# Verificar status
sudo systemctl status nginx
```


### Etapa 3: Sistema de Monitoramento

#### 3.1 Desenvolvimento do Script de Monitoramento

O sistema de monitoramento foi implementado em Python com as seguintes características:

**Funcionalidades Principais:**

- **Verificação de disponibilidade**: Testa conectividade HTTP a cada execução
- **Detecção de mudanças de estado**: Identifica quando o site sai do ar ou volta a funcionar
- **Sistema de alertas inteligente**: Envia notificações apenas quando há mudança de status
- **Logging detalhado**: Registra todas as verificações com timestamps e métricas
- **Canais de notificação**: Suporte para Discord
- **Tratamento de erros robusto**: Captura e registra diferentes tipos de falhas

**Arquitetura do Script:**

O script `monitor_site.py` utiliza uma arquitetura modular com as seguintes funções principais:

1. **`check_site_status()`**: Realiza a verificação HTTP e coleta métricas
2. **`load_previous_status()`** e **`save_current_status()`**: Gerenciam o estado persistente
3. **`send_discord_alert()`**: Implementam os canais de notificação
4. **`format_alert_message()`**: Formata mensagens de alerta de forma consistente

**Configuração de Webhooks:**

O sistema o webhooks do discord:

- **Discord**: Utiliza webhooks nativos do Discord para envio de mensagens

#### 3.2 Configuração do Script

```bash
# Criar o script de monitoramento
nano /home/ubuntu/monitor_site.py

# Tornar executável
chmod +x /home/ubuntu/monitor_site.py

# Criar diretório de logs se não existir
sudo mkdir -p /var/log

# Criar arquivo de log com permissões adequadas
sudo touch /var/log/monitoramento.log
sudo chown ubuntu:ubuntu /var/log/monitoramento.log
```

#### 3.3 Configuração de Webhooks

Para configurar os webhooks, utilize o script auxiliar fornecido:

```bash
# Executar configurador de webhooks
python3 /home/ubuntu/webhook_config.py
```

**No Discord:**
1. Acesse as configurações do seu servidor Discord
2. Vá em Integrações > Webhooks
3. Crie um novo webhook e copie a URL
4. Cole a URL no configurador

#### 3.4 Automação com Systemd

O sistema utiliza systemd timers para execução automática e confiável:

**Arquivo de Serviço** (`/etc/systemd/system/monitor-site.service`):
```ini
[Unit]
Description=Monitor do Site - Verificação de Disponibilidade
After=network.target nginx.service

[Service]
Type=oneshot
User=ubuntu
Group=ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/monitor_site.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Arquivo de Timer** (`/etc/systemd/system/monitor-site.timer`):
```ini
[Unit]
Description=Timer para Monitor do Site
Requires=monitor-site.service

[Timer]
OnCalendar=*:*:00
Persistent=true

[Install]
WantedBy=timers.target
```

**Ativação do Timer:**
```bash
# Recarregar configurações do systemd
sudo systemctl daemon-reload

# Habilitar e iniciar o timer
sudo systemctl enable monitor-site.timer
sudo systemctl start monitor-site.timer

# Verificar status
sudo systemctl status monitor-site.timer
```


### Etapa 4: Sistema de Logs e Análise

#### 4.1 Configuração de Logs

O projeto implementa um sistema abrangente de logging com múltiplas camadas:

**Logs do Nginx:**
- **Access Log**: `/var/log/nginx/projeto-linux.access.log` - Registra todas as requisições HTTP
- **Error Log**: `/var/log/nginx/projeto-linux.error.log` - Registra erros do servidor web

**Logs do Monitoramento:**
- **Monitor Log**: `/var/log/monitoramento.log` - Registra todas as verificações e alertas

#### 4.2 Rotação de Logs

Para evitar que os logs consumam muito espaço em disco, foi configurada a rotação automática:

```bash
# Configuração em /etc/logrotate.d/projeto-linux
/var/log/nginx/projeto-linux.*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data adm
    sharedscripts
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1
    endscript
}

/var/log/monitoramento.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    copytruncate
}
```

#### 4.3 Análise de Logs

Foi desenvolvido um script de análise de logs (`log_analyzer.py`) que fornece:

**Métricas do Servidor Web:**
- Total de requisições e visitantes únicos
- Distribuição de códigos de status HTTP
- Páginas mais acessadas
- Análise temporal (por hora e por dia)
- Detecção de erros e tentativas de acesso malicioso

**Métricas do Monitoramento:**
- Uptime percentual do serviço
- Tempo médio de resposta
- Número de verificações realizadas
- Eventos de indisponibilidade
- Alertas enviados

**Uso do Analisador:**
```bash
# Executar análise completa
python3 /home/ubuntu/log_analyzer.py

# O script gera um relatório em tela e salva um arquivo JSON detalhado
```

#### 4.4 Monitoramento em Tempo Real

Para monitoramento em tempo real, utilize os seguintes comandos:

```bash
# Acompanhar logs do Nginx em tempo real
sudo tail -f /var/log/nginx/projeto-linux.access.log

# Acompanhar logs do monitoramento
tail -f /var/log/monitoramento.log

# Verificar status dos serviços
sudo systemctl status nginx
sudo systemctl status monitor-site.timer

# Listar próximas execuções do timer
sudo systemctl list-timers monitor-site.timer
```

## Testes e Validação

### Teste 1: Verificação da Página Web

1. **Acesso Local:**
   ```bash
   curl -I http://localhost
   ```
   Deve retornar status HTTP 200 OK.

2. **Acesso via Navegador:**
   Abra um navegador e acesse `http://localhost` ou o IP do servidor.
   A página deve carregar com o design responsivo e informações atualizadas.

### Teste 2: Validação do Sistema de Monitoramento

1. **Teste de Funcionamento Normal:**
   ```bash
   python3 /home/ubuntu/monitor_site.py
   ```
   Deve registrar "Site OK" no log.

2. **Teste de Detecção de Falha:**
   ```bash
   # Parar o Nginx
   sudo systemctl stop nginx
   
   # Executar monitoramento
   python3 /home/ubuntu/monitor_site.py
   
   # Verificar logs
   tail -5 /var/log/monitoramento.log
   ```

3. **Teste de Restauração:**
   ```bash
   # Reiniciar o Nginx
   sudo systemctl start nginx
   
   # Executar monitoramento novamente
   python3 /home/ubuntu/monitor_site.py
   ```

### Teste 3: Verificação de Alertas

Se os webhooks estiverem configurados:

1. Pare o serviço Nginx
2. Execute o script de monitoramento
3. Verifique se recebeu o alerta no canal configurado
4. Reinicie o Nginx
5. Execute novamente e verifique o alerta de restauração

### Teste 4: Validação da Automação

```bash
# Verificar se o timer está ativo
sudo systemctl is-active monitor-site.timer

# Verificar próximas execuções
sudo systemctl list-timers monitor-site.timer

# Aguardar alguns minutos e verificar logs
tail -10 /var/log/monitoramento.log
```


## Troubleshooting

### Problemas Comuns e Soluções

#### Nginx não inicia

**Sintomas:** Erro ao executar `sudo systemctl start nginx`

**Possíveis Causas e Soluções:**

1. **Conflito de porta:**
   ```bash
   # Verificar se a porta 80 está em uso
   sudo netstat -tlnp | grep :80
   
   # Se houver conflito, parar o serviço conflitante ou alterar a porta do Nginx
   ```

2. **Erro de configuração:**
   ```bash
   # Testar configuração
   sudo nginx -t
   
   # Verificar logs de erro
   sudo journalctl -u nginx.service
   ```

3. **Permissões incorretas:**
   ```bash
   # Verificar permissões dos arquivos de configuração
   sudo ls -la /etc/nginx/sites-available/projeto-linux
   
   # Corrigir se necessário
   sudo chmod 644 /etc/nginx/sites-available/projeto-linux
   ```

#### Script de monitoramento não funciona

**Sintomas:** Logs não são gerados ou alertas não são enviados

**Soluções:**

1. **Verificar dependências Python:**
   ```bash
   python3 -c "import requests; print('OK')"
   
   # Se der erro, instalar:
   pip3 install requests
   ```

2. **Verificar permissões do arquivo de log:**
   ```bash
   ls -la /var/log/monitoramento.log
   
   # Corrigir permissões se necessário
   sudo chown ubuntu:ubuntu /var/log/monitoramento.log
   ```

3. **Testar conectividade:**
   ```bash
   curl -I http://localhost
   ```

#### Timer systemd não executa

**Sintomas:** Script não executa automaticamente

**Soluções:**

1. **Verificar status do timer:**
   ```bash
   sudo systemctl status monitor-site.timer
   sudo systemctl list-timers monitor-site.timer
   ```

2. **Verificar logs do systemd:**
   ```bash
   sudo journalctl -u monitor-site.service
   sudo journalctl -u monitor-site.timer
   ```

3. **Recarregar configurações:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart monitor-site.timer
   ```

#### Webhooks não funcionam

**Sintomas:** Alertas não chegam aos canais configurados

**Soluções:**

1. **Verificar configuração:**
   ```bash
   grep -A 10 "WEBHOOK_CONFIG" /home/ubuntu/monitor_site.py
   ```

2. **Testar conectividade:**
   ```bash
   # Para Discord
   curl -X POST [URL_DO_WEBHOOK] -H "Content-Type: application/json" -d '{"content":"teste"}'
   ```

3. **Reconfigurar webhooks:**
   ```bash
   python3 /home/ubuntu/webhook_config.py
   ```

## Manutenção

### Tarefas de Manutenção Regulares

#### Diária
- Verificar logs de erro: `sudo tail /var/log/nginx/projeto-linux.error.log`
- Monitorar espaço em disco: `df -h`
- Verificar status dos serviços: `sudo systemctl status nginx monitor-site.timer`

#### Semanal
- Analisar relatórios de logs: `python3 /home/ubuntu/log_analyzer.py`
- Verificar atualizações de segurança: `sudo apt list --upgradable`
- Testar sistema de backup (se implementado)

#### Mensal
- Revisar configurações de rotação de logs
- Analisar métricas de performance
- Atualizar documentação se necessário

### Atualizações de Sistema

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes (cuidado com atualizações do Nginx)
sudo apt upgrade

# Reiniciar serviços se necessário
sudo systemctl restart nginx
```

### Backup e Recuperação

**Arquivos importantes para backup:**
- `/etc/nginx/sites-available/projeto-linux`
- `/var/www/html/projeto-linux/`
- `/home/ubuntu/monitor_site.py`
- `/home/ubuntu/webhook_config.py`
- `/home/ubuntu/log_analyzer.py`
- `/etc/systemd/system/monitor-site.*`
- `/etc/logrotate.d/projeto-linux`

**Script de backup sugerido:**
```bash
#!/bin/bash
BACKUP_DIR="/backup/projeto-linux-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup de configurações
cp -r /etc/nginx/sites-available/projeto-linux $BACKUP_DIR/
cp -r /var/www/html/projeto-linux/ $BACKUP_DIR/
cp /home/ubuntu/*.py $BACKUP_DIR/
cp /etc/systemd/system/monitor-site.* $BACKUP_DIR/
cp /etc/logrotate.d/projeto-linux $BACKUP_DIR/

# Backup de logs recentes
cp /var/log/monitoramento.log $BACKUP_DIR/
cp /var/log/nginx/projeto-linux.*.log $BACKUP_DIR/

echo "Backup criado em $BACKUP_DIR"
```
