# HƯỚNG DẪN DEPLOY TELEGRAM BOT LÊN UBUNTU SERVER

## 📋 YÊU CẦU
- Server Ubuntu (18.04 trở lên)
- Python 3.8 trở lên
- Quyền sudo trên server

## 🚀 CÁC BƯỚC DEPLOY

### BƯỚC 1: Kết nối SSH vào server
```bash
ssh username@your-server-ip
```

### BƯỚC 2: Cập nhật hệ thống
```bash
sudo apt update && sudo apt upgrade -y
```

### BƯỚC 3: Cài đặt Python và các công cụ cần thiết
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

Kiểm tra phiên bản Python:
```bash
python3 --version
```

### BƯỚC 4: Tạo thư mục cho project
```bash
cd ~
mkdir telegram-bot
cd telegram-bot
```

### BƯỚC 5: Upload code lên server

**Cách 1: Dùng Git (Khuyên dùng)**
```bash
# Nếu bạn đã push code lên GitHub/GitLab
git clone https://github.com/your-username/your-repo.git .
```

**Cách 2: Dùng SCP từ máy local (Windows)**

Mở PowerShell trên máy Windows và chạy:
```powershell
# Di chuyển đến thư mục project
cd C:\projects\myproject\python-tracking-telegram

# Upload các file cần thiết
scp telegram_bot.py requirements.txt username@your-server-ip:~/telegram-bot/

# Upload session file (QUAN TRỌNG!)
scp rio_session.session username@your-server-ip:~/telegram-bot/
```

**Cách 3: Dùng SFTP hoặc FileZilla**
- Tải FileZilla Client
- Kết nối đến server
- Upload các file: `telegram_bot.py`, `requirements.txt`, `rio_session.session`

### BƯỚC 6: Tạo virtual environment
```bash
cd ~/telegram-bot
python3 -m venv venv
source venv/bin/activate
```

### BƯỚC 7: Cài đặt dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### BƯỚC 8: Test chạy bot
```bash
python3 telegram_bot.py
```

Nếu chạy thành công, bạn sẽ thấy:
```
==================================================
Starting Telegram Bot...
==================================================
[OK] Client started successfully!

[TRACKING CONFIGURATION]:
  -5030834670 -> [-5077669868]

Waiting for new messages...
```

Nhấn `Ctrl + C` để dừng test.

### BƯỚC 9: Tạo systemd service để bot chạy tự động

Tạo file service:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Dán nội dung sau vào (thay `your-username` bằng username của bạn):
```ini
[Unit]
Description=Telegram Tracking Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/telegram-bot
Environment="PATH=/home/your-username/telegram-bot/venv/bin"
ExecStart=/home/your-username/telegram-bot/venv/bin/python3 /home/your-username/telegram-bot/telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Lưu file:
- Nhấn `Ctrl + X`
- Nhấn `Y`
- Nhấn `Enter`

### BƯỚC 10: Kích hoạt và khởi động service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Bật service tự động chạy khi khởi động
sudo systemctl enable telegram-bot

# Khởi động service
sudo systemctl start telegram-bot

# Kiểm tra trạng thái
sudo systemctl status telegram-bot
```

Nếu thành công, bạn sẽ thấy `active (running)` màu xanh.

### BƯỚC 11: Các lệnh quản lý bot

**Xem logs (real-time):**
```bash
sudo journalctl -u telegram-bot -f
```

**Xem logs (100 dòng cuối):**
```bash
sudo journalctl -u telegram-bot -n 100
```

**Dừng bot:**
```bash
sudo systemctl stop telegram-bot
```

**Khởi động lại bot:**
```bash
sudo systemctl restart telegram-bot
```

**Tắt auto-start:**
```bash
sudo systemctl disable telegram-bot
```

**Kiểm tra trạng thái:**
```bash
sudo systemctl status telegram-bot
```

## 🔄 CẬP NHẬT CODE

Khi muốn cập nhật code:

```bash
cd ~/telegram-bot

# Nếu dùng git
git pull

# Hoặc upload file mới qua SCP/SFTP

# Khởi động lại service
sudo systemctl restart telegram-bot

# Kiểm tra logs
sudo journalctl -u telegram-bot -f
```

## 🔐 BẢO MẬT

### 1. Bảo vệ API credentials
Không nên hardcode api_id và api_hash trong code. Nên dùng file `.env`:

Cài đặt python-dotenv:
```bash
pip install python-dotenv
```

Tạo file `.env`:
```bash
nano .env
```

Nội dung:
```
API_ID=34825182
API_HASH=cca8421e42f03c10bccdffddf07be13b
```

Cập nhật `telegram_bot.py` để đọc từ file `.env`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
```

### 2. Bảo vệ file session
```bash
chmod 600 ~/telegram-bot/rio_session.session
```

### 3. Cấu hình Firewall (tùy chọn)
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw status
```

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "Permission denied"
```bash
chmod +x telegram_bot.py
```

### Lỗi: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Bot không chạy sau khi reboot
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Kiểm tra lỗi chi tiết
```bash
sudo journalctl -u telegram-bot -n 50 --no-pager
```

## 📊 GIÁM SÁT

### Kiểm tra bot có đang chạy không
```bash
ps aux | grep telegram_bot
```

### Kiểm tra tài nguyên sử dụng
```bash
top -p $(pgrep -f telegram_bot)
```

### Kiểm tra disk space
```bash
df -h
```

## 🎯 HOÀN TẤT!

Bot của bạn giờ đã chạy 24/7 trên server Ubuntu và sẽ tự động khởi động lại khi:
- Server reboot
- Bot bị crash
- Có lỗi xảy ra

Chúc bạn deploy thành công! 🎉

