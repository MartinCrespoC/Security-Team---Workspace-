#!/bin/bash
# MCP Manager - Gestión del servidor CyberStrike MCP
# Uso: ./mcp-manager.sh [start|stop|restart|status|logs|web]

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SERVICE="cyberstrike-mcp.service"
PORT=4096

case "$1" in
    start)
        echo -e "${BLUE}[*] Iniciando CyberStrike MCP...${NC}"
        systemctl --user start $SERVICE
        sleep 2
        if systemctl --user is-active --quiet $SERVICE; then
            echo -e "${GREEN}[✓] Servidor activo en http://127.0.0.1:$PORT${NC}"
        else
            echo -e "${RED}[✗] Error al iniciar el servicio${NC}"
            exit 1
        fi
        ;;
    stop)
        echo -e "${YELLOW}[*] Deteniendo CyberStrike MCP...${NC}"
        systemctl --user stop $SERVICE
        echo -e "${GREEN}[✓] Servicio detenido${NC}"
        ;;
    restart)
        echo -e "${BLUE}[*] Reiniciando CyberStrike MCP...${NC}"
        systemctl --user restart $SERVICE
        sleep 2
        systemctl --user status $SERVICE --no-pager
        ;;
    status)
        echo -e "${BLUE}[*] Estado del servicio:${NC}"
        systemctl --user status $SERVICE --no-pager
        echo ""
        echo -e "${BLUE}[*] Verificando conectividad:${NC}"
        if curl -s http://127.0.0.1:$PORT/ > /dev/null 2>&1; then
            echo -e "${GREEN}[✓] Servidor respondiendo en puerto $PORT${NC}"
        else
            echo -e "${RED}[✗] Servidor no responde${NC}"
        fi
        ;;
    logs)
        echo -e "${BLUE}[*] Logs del servicio (últimas 50 líneas):${NC}"
        journalctl --user -u $SERVICE -n 50 --no-pager
        ;;
    web)
        echo -e "${BLUE}[*] Abriendo interfaz web de CyberStrike...${NC}"
        cyberstrike web &
        ;;
    attach)
        echo -e "${BLUE}[*] Conectando al servidor...${NC}"
        cyberstrike attach http://127.0.0.1:$PORT
        ;;
    *)
        echo "CyberStrike MCP Manager"
        echo ""
        echo "Uso: $0 {start|stop|restart|status|logs|web|attach}"
        echo ""
        echo "Comandos:"
        echo "  start   - Iniciar el servidor MCP"
        echo "  stop    - Detener el servidor MCP"
        echo "  restart - Reiniciar el servidor MCP"
        echo "  status  - Ver estado del servicio"
        echo "  logs    - Ver logs del servicio"
        echo "  web     - Abrir interfaz web"
        echo "  attach  - Conectar al servidor desde terminal"
        echo ""
        echo "Servidor: http://127.0.0.1:$PORT"
        echo "Password: RedTeam2026!"
        exit 1
        ;;
esac
