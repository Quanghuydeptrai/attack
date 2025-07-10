import requests, os
from datetime import datetime

# Hiển thị banner bản quyền
print("""
╔═══════════════════════════════════════════════════════════════╗
║            DVNTEAM - TOOL GET HTTP PROXY                     ║
║  © Bản quyền: Quốc Dũng | DVNTEAM | Zalo: 0328073436         ║
╚═══════════════════════════════════════════════════════════════╝
""")

print("DVNTEAM ĐANG LẤY PROXY CHO BẠN...\n")

# Danh sách nguồn proxy HTTP
proxy_sources = [
	"https://raw.githubusercontent.com/TuanMinPay/live-proxy/873c59a93551725a21d83fe422ee9855c55904a6/http.txt",
	"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all",
"https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=3000&country=all&ssl=all&anonymity=all",
"https://proxylist.geonode.com/api/proxy-list?limit=50000&page=1&sort_by=lastChecked&sort_type=desc",
"https://openproxy.space/list/http",
"https://openproxy.space/list/https",
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",
"https://www.proxy-list.download/api/v1/get?type=https",
"https://www.proxy-list.download/api/v1/get?type=http"
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
"https://raw.githubusercontent.com/sunny9577/proxy-list/master/proxies.txt",
"https://raw.githubusercontent.com/Muhammetsezer/Proxy-List/master/http.txt",
"https://raw.githubusercontent.com/proxybot/proxies/main/http.txt",
"https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/Anonym0usWork1221/free-proxies/main/http.txt",
"https://raw.githubusercontent.com/ErcanUygu/Free-Proxy-List/main/http.txt",
"https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
"https://raw.githubusercontent.com/RXNET-ORG/proxylist/master/http.txt",
"https://raw.githubusercontent.com/caliph71/proxylist/master/http.txt",
"https://raw.githubusercontent.com/rosemaryr/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
"https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
"https://raw.githubusercontent.com/mertguven/proxy-list/main/proxy-list/data.txt",
"https://raw.githubusercontent.com/parserpp/proxy-list/main/proxies.txt",
"https://raw.githubusercontent.com/officialputuid/KangProxy/main/http/http.txt",
"https://raw.githubusercontent.com/yemix/proxy-list/main/proxy-list/data.txt",
"https://raw.githubusercontent.com/mmok/proxy-list/master/http.txt",
"https://raw.githubusercontent.com/Uptobox-Proxy/Proxy-List/master/proxy-list/data.txt",
"https://raw.githubusercontent.com/webshare-io/proxy-list/main/proxies-http.txt",
"https://raw.githubusercontent.com/opsxcq/proxy-list/master/proxy.txt",
"https://raw.githubusercontent.com/hookzof/socks5_list/master/http.txt",
"https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
"https://raw.githubusercontent.com/KingToom/proxy-list/master/http.txt",
"https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
"https://raw.githubusercontent.com/Hyperclaw7/Proxy-List/main/http.txt",
"https://raw.githubusercontent.com/yusufonur/proxy-list/main/proxy.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
"https://raw.githubusercontent.com/rxnets/proxylist/master/http.txt",
"https://raw.githubusercontent.com/Volkovoy1/Proxy-list/main/http.txt",
"https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
"https://raw.githubusercontent.com/Mr-Zal/Proxy-List/main/http.txt",
"https://raw.githubusercontent.com/KorexT/Proxy-List/main/http.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000",
    "https://www.free-proxy-list.net/download?type=http",
    "https://vakhov.github.io/fresh-proxy-list/http.txt",
    "https://proxifly.dev/free-proxy-list.txt",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&sort_by=lastChecked&format=textplain",
    "http://alexa.lr2b.com/proxylist.txt",
    "http://worm.rip/http.txt",
    "http://rootjazz.com/proxies/proxies.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_HTTP.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/constverum/ProxyBroker/master/docs/examples/proxy_list.txt",
    "https://raw.githubusercontent.com/free-proxy-list/proxy-daily-http/main/proxy-list.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/im-razvan/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/proxy.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy-list-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
    "https://www.proxy-list.download/api/v1/get?type=http"
]

# Tập hợp proxy không trùng lặp
http_proxies = set()

# Bắt đầu quét từng nguồn
for i, url in enumerate(proxy_sources, 1):
    try:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"🔄 Đang lấy proxy từ nguồn thứ {i}... [{now}]")
        r = requests.get(url, timeout=10)
        if r.ok:
            if "<html" in r.text.lower() or "<!doctype" in r.text.lower():
                continue  # Bỏ qua nếu là HTML
            for line in r.text.splitlines():
                line = line.strip()
                if (
                    ":" in line
                    and not line.startswith("#")
                    and not line.lower().startswith("proxy-list")
                    and not line.lower().startswith("moved to")
                    and not line.lower().startswith("http://")
                    and not line.lower().startswith("https://")
                    and line.count(":") == 1
                ):
                    http_proxies.add(line)
    except:
        pass  # Ẩn lỗi không in ra

# Ghi file
os.makedirs("output", exist_ok=True)
with open("proxy.txt", "w") as f:
    for proxy in sorted(http_proxies):
        f.write(proxy + "\n")

print("\n✅ DVNTEAM ĐÃ LẤY PROXY CHO BẠN THÀNH CÔNG!")
print(f"✅ Đã lưu {len(http_proxies)} proxy HTTP vào: output/http_proxies.txt")
print("© Quốc Dũng | DVNTEAM | Zalo: 0328073436")
