#!/bin/bash
# Script tự động deploy Telegram Bot lên Ubuntu Server

set -e

echo "=================================="
echo "TELEGRAM BOT DEPLOYMENT SCRIPT"
echo "=================================="
echo ""

# Màu sắc cho output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kiểm tra quyền root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Không nên chạy script này với quyền root${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Bước 1: Cập nhật hệ thống...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${YELLOW}📦 Bước 2: Cài đặt Python và dependencies...${NC}"
sudo apt install python3 python3-pip python3-venv -y

echo -e "${YELLOW}📁 Bước 3: Tạo virtual environment...${NC}"
python3 -m venv venv

echo -e "${YELLOW}📥 Bước 4: Cài đặt requirements...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}🔍 Bước 5: Kiểm tra file session...${NC}"
if [ ! -f "rio_session.session" ]; then
    echo -e "${RED}❌ Không tìm thấy file rio_session.session!${NC}"
    echo -e "${YELLOW}Vui lòng upload file session từ máy local lên server${NC}"
    exit 1
fi

echo -e "${GREEN}✅ File session đã có sẵn${NC}"

echo -e "${YELLOW}⚙️  Bước 6: Cấu hình systemd service...${NC}"
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

# Tạo file service
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null <<EOF
[Unit]
Description=Telegram Tracking Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$CURRENT_DIR/venv/bin"
ExecStart=$CURRENT_DIR/venv/bin/python3 $CURRENT_DIR/telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${YELLOW}🔄 Bước 7: Reload systemd và enable service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot

echo -e "${YELLOW}🚀 Bước 8: Khởi động bot...${NC}"
sudo systemctl start telegram-bot

sleep 2

echo -e "${YELLOW}📊 Bước 9: Kiểm tra trạng thái...${NC}"
sudo systemctl status telegram-bot --no-pager

echo ""
echo -e "${GREEN}=================================="
echo -e "✅ DEPLOYMENT HOÀN TẤT!"
echo -e "==================================${NC}"
echo ""
echo -e "${YELLOW}Các lệnh hữu ích:${NC}"
echo "  • Xem logs: sudo journalctl -u telegram-bot -f"
echo "  • Dừng bot: sudo systemctl stop telegram-bot"
echo "  • Khởi động: sudo systemctl start telegram-bot"
echo "  • Restart: sudo systemctl restart telegram-bot"
echo "  • Trạng thái: sudo systemctl status telegram-bot"
echo ""

