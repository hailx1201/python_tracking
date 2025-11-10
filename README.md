# 🤖 Telegram Tracking Bot

Bot Telegram tự động theo dõi và chuyển tiếp tin nhắn giữa các nhóm/kênh.

## ✨ Tính năng

- ✅ Tự động tracking tin nhắn từ các nhóm được chỉ định
- ✅ Chuyển tiếp tin nhắn (text + media) đến các nhóm đích
- ✅ Hỗ trợ nhiều cặp group tracking
- ✅ Logs chi tiết mọi hoạt động
- ✅ Tự động khởi động lại khi gặp lỗi

## 📋 Yêu cầu

- Python 3.8+
- Telegram API credentials (api_id và api_hash)
- Session file đã được xác thực

## 🚀 Cài đặt Local (Windows/Mac/Linux)

1. Clone hoặc download project

2. Tạo virtual environment:
```bash
python -m venv venv
```

3. Kích hoạt virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

5. Chạy bot:
```bash
python telegram_bot.py
```

## 🔧 Cấu hình

### Thêm cặp tracking group mới

Chỉnh sửa `TRACKING_MAP` trong file `telegram_bot.py`:

```python
TRACKING_MAP = {
    -5030834670: [-5077669868],  # Group nguồn -> [Group đích]
    -1234567890: [-9876543210, -1111111111],  # Một nguồn -> nhiều đích
}
```

### Lấy ID của group/channel

1. Thêm bot [@userinfobot](https://t.me/userinfobot) vào group
2. Bot sẽ gửi ID của group
3. Hoặc forward 1 tin nhắn từ group đến bot

## 📦 Deploy lên Ubuntu Server

Xem hướng dẫn chi tiết trong file [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Quick Start

1. Upload code lên server:
```bash
scp -r . username@server-ip:~/telegram-bot/
```

2. SSH vào server:
```bash
ssh username@server-ip
```

3. Chạy script tự động deploy:
```bash
cd ~/telegram-bot
chmod +x deploy.sh
./deploy.sh
```

## 📊 Quản lý Bot (trên Server)

### Xem logs real-time
```bash
sudo journalctl -u telegram-bot -f
```

### Restart bot
```bash
sudo systemctl restart telegram-bot
```

### Stop bot
```bash
sudo systemctl stop telegram-bot
```

### Kiểm tra trạng thái
```bash
sudo systemctl status telegram-bot
```

## 🔐 Bảo mật

- ⚠️ **QUAN TRỌNG**: Không share file session với ai
- ⚠️ Không commit api_id, api_hash lên git public
- ✅ Nên dùng file `.env` để lưu credentials
- ✅ Set quyền cho file session: `chmod 600 *.session`

## 📝 Logs

Bot ghi logs chi tiết mọi hoạt động:
- `[NEW MESSAGE]`: Tin nhắn mới được phát hiện
- `[SUCCESS]`: Chuyển tiếp thành công
- `[FAILED]`: Lỗi khi chuyển tiếp
- `[SKIP]`: Tin nhắn trống bị bỏ qua

## 🐛 Xử lý lỗi

### Bot không nhận được tin nhắn
- Kiểm tra bot có trong group nguồn không
- Kiểm tra ID group có đúng không (bao gồm dấu `-`)

### Bot không gửi được tin nhắn
- Kiểm tra bot có trong group đích không
- Kiểm tra bot có quyền gửi tin nhắn không

### Session expired
- Chạy lại bot local để tạo session mới
- Upload session mới lên server

## 📞 Support

Nếu gặp vấn đề, hãy kiểm tra logs:
```bash
sudo journalctl -u telegram-bot -n 100
```

## 📜 License

MIT License - Free to use for personal and commercial projects.

