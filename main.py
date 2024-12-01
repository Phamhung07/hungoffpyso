from flask import Flask, render_template, request
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7313078697:AAEWdQ3HAIyYDYXAZ3PbvaLW3S7tfl_YyWg'  # Thay bằng token của bạn
TELEGRAM_CHAT_ID = '6074433365'  # Thay bằng chat ID Telegram của bạn

@app.route('/')
def home():
    # Lấy ngày tháng theo giờ Việt Nam
    now = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    date_time = now.strftime("%H:%M:%S %d-%m-%Y")
    return render_template('index.html', date_time=date_time)

@app.route('/send_info', methods=['POST'])
def send_info():
    user_response = request.form.get('response')
    if user_response == 'agree':
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        message = f"📱 **Thông tin truy cập**:\n- IP: {ip_address}\n- Thiết bị: {user_agent}"
        send_to_telegram(message)

        return "Cảm ơn bạn đã gửi thông tin! Tôi đã nhận được thông tin của bạn."
    else:
        return "Bạn đã từ chối gửi thông tin."

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)