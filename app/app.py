from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import warnings

# ปิดการแจ้งเตือน
warnings.filterwarnings('ignore')

app = Flask(__name__)

# --- 1. ฐานข้อมูลอะไหล่ (อัปเดตข้อมูลจากที่คุณให้มา + เพิ่มฟิลด์คัดกรอง) ---

# --- ส่วนฐานข้อมูลใหม่ (วางใน app.py) ---

cpus = [
    {"name": "Intel Core i3-12100F", "cpu_brand": "Intel", "price": 3000, "socket": "LGA1700", "ram_support": "DDR4"},
    {"name": "Intel Core i5-12400F", "cpu_brand": "Intel", "price": 4800, "socket": "LGA1700", "ram_support": "DDR4"},
    {"name": "Intel Core i5-13400F", "cpu_brand": "Intel", "price": 7500, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "Intel Core i5-13500", "cpu_brand": "Intel", "price": 8900, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "Intel Core i7-13700K", "cpu_brand": "Intel", "price": 14500, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "Intel Core i9-13900K", "cpu_brand": "Intel", "price": 20000, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "Intel Core i5-14600K", "cpu_brand": "Intel", "price": 11500, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "Intel Core i7-14700K", "cpu_brand": "Intel", "price": 15500, "socket": "LGA1700", "ram_support": "DDR5"},
    {"name": "AMD Ryzen 3 3200G", "cpu_brand": "AMD", "price": 2500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 5 4500", "cpu_brand": "AMD", "price": 2900, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 5 5500", "cpu_brand": "AMD", "price": 3500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 5 5600", "cpu_brand": "AMD", "price": 4500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 5 5600X", "cpu_brand": "AMD", "price": 5500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 7 5700X", "cpu_brand": "AMD", "price": 6500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 7 5800X3D", "cpu_brand": "AMD", "price": 10500, "socket": "AM4", "ram_support": "DDR4"},
    {"name": "AMD Ryzen 5 7600", "cpu_brand": "AMD", "price": 7000, "socket": "AM5", "ram_support": "DDR5"},
    {"name": "AMD Ryzen 5 7600X", "cpu_brand": "AMD", "price": 8000, "socket": "AM5", "ram_support": "DDR5"},
    {"name": "AMD Ryzen 7 7700X", "cpu_brand": "AMD", "price": 11000, "socket": "AM5", "ram_support": "DDR5"},
    {"name": "AMD Ryzen 7 7800X3D", "cpu_brand": "AMD", "price": 14000, "socket": "AM5", "ram_support": "DDR5"},
    {"name": "AMD Ryzen 9 7900X", "cpu_brand": "AMD", "price": 15000, "socket": "AM5", "ram_support": "DDR5"}
]

mbs = [
    {"name": "ASUS H610M-K (LGA1700/DDR4)", "price": 2200, "socket": "LGA1700", "ram_type": "DDR4"},
    {"name": "MSI PRO B660M-A (LGA1700/DDR4)", "price": 3500, "socket": "LGA1700", "ram_type": "DDR4"},
    {"name": "GIGABYTE B760M DS3H (LGA1700/DDR4)", "price": 4000, "socket": "LGA1700", "ram_type": "DDR4"},
    {"name": "ASUS PRIME Z690-P (LGA1700/DDR4)", "price": 6500, "socket": "LGA1700", "ram_type": "DDR4"},
    {"name": "ASUS PRIME B760M-A (LGA1700/DDR5)", "price": 4800, "socket": "LGA1700", "ram_type": "DDR5"},
    {"name": "MSI MAG B760 TOMAHAWK (LGA1700/DDR5)", "price": 6900, "socket": "LGA1700", "ram_type": "DDR5"},
    {"name": "ASUS PRIME Z790-P (LGA1700/DDR5)", "price": 8500, "socket": "LGA1700", "ram_type": "DDR5"},
    {"name": "GIGABYTE Z790 AORUS ELITE (LGA1700/DDR5)", "price": 9900, "socket": "LGA1700", "ram_type": "DDR5"},
    {"name": "ASUS PRIME A320M-K (AM4/DDR4)", "price": 1500, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "MSI B450M-A PRO MAX (AM4/DDR4)", "price": 2000, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "ASUS PRIME A520M-A (AM4/DDR4)", "price": 2200, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "GIGABYTE B550M DS3H (AM4/DDR4)", "price": 3200, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "MSI MAG B550 TOMAHAWK (AM4/DDR4)", "price": 5500, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "ASUS PRIME X570-P (AM4/DDR4)", "price": 6000, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "GIGABYTE X570S AORUS (AM4/DDR4)", "price": 8000, "socket": "AM4", "ram_type": "DDR4"},
    {"name": "ASRock A620M-HDV/M.2 (AM5/DDR5)", "price": 3000, "socket": "AM5", "ram_type": "DDR5"},
    {"name": "GIGABYTE B650M DS3H (AM5/DDR5)", "price": 4900, "socket": "AM5", "ram_type": "DDR5"},
    {"name": "MSI MAG B650 TOMAHAWK WIFI (AM5/DDR5)", "price": 7500, "socket": "AM5", "ram_type": "DDR5"},
    {"name": "ASUS PRIME X670-P (AM5/DDR5)", "price": 9500, "socket": "AM5", "ram_type": "DDR5"},
    {"name": "ASUS ROG CROSSHAIR X670E HERO (AM5/DDR5)", "price": 22000, "socket": "AM5", "ram_type": "DDR5"}
]

gpus = [
    {"name": "NVIDIA GT 1030 2GB", "price": 2800, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 6500 XT 4GB", "price": 4500, "gpu_brand": "AMD"},
    {"name": "NVIDIA GTX 1650 4GB", "price": 4800, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA GTX 1660 SUPER 6GB", "price": 6500, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA RTX 3050 6GB", "price": 7000, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 6600 8GB", "price": 7500, "gpu_brand": "AMD"},
    {"name": "AMD Radeon RX 7600 8GB", "price": 9900, "gpu_brand": "AMD"},
    {"name": "NVIDIA RTX 3060 12GB", "price": 10500, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA RTX 4060 8GB", "price": 11500, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA RTX 3060 Ti 8GB", "price": 12500, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 6700 XT 12GB", "price": 13000, "gpu_brand": "AMD"},
    {"name": "NVIDIA RTX 4060 Ti 8GB", "price": 14500, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA RTX 4070 12GB", "price": 21000, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 7800 XT 16GB", "price": 20000, "gpu_brand": "AMD"},
    {"name": "NVIDIA RTX 4070 SUPER 12GB", "price": 24000, "gpu_brand": "NVIDIA"},
    {"name": "NVIDIA RTX 4070 Ti SUPER 16GB", "price": 31000, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 7900 XT 20GB", "price": 32000, "gpu_brand": "AMD"},
    {"name": "NVIDIA RTX 4080 SUPER 16GB", "price": 40000, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 7900 XTX 24GB", "price": 38000, "gpu_brand": "AMD"},
    {"name": "NVIDIA RTX 4090 24GB", "price": 75000, "gpu_brand": "NVIDIA"}
]

rams = [
    # --- RAM ---
    {"name": "4GB DDR3 1600MHz", "price": 250, "ram_type": "DDR3", "ram_size": 4},
    {"name": "4GB DDR4 2400MHz", "price": 400, "ram_type": "DDR4", "ram_size": 4},
    {"name": "4GB DDR4 3200MHz", "price": 450, "ram_type": "DDR4", "ram_size": 4},
    {"name": "8GB DDR4 2666MHz", "price": 600, "ram_type": "DDR4", "ram_size": 8},
    {"name": "8GB DDR4 3200MHz", "price": 700, "ram_type": "DDR4", "ram_size": 8},
    {"name": "16GB (1x16GB) DDR4 3200MHz", "price": 1200, "ram_type": "DDR4", "ram_size": 16},
    {"name": "16GB (8GBx2) DDR4 3200MHz", "price": 1400, "ram_type": "DDR4", "ram_size": 16},
    {"name": "16GB (8GBx2) DDR4 3600MHz", "price": 1600, "ram_type": "DDR4", "ram_size": 16},
    {"name": "32GB (16GBx2) DDR4 3200MHz", "price": 2500, "ram_type": "DDR4", "ram_size": 32},
    {"name": "16GB (1x16GB) DDR5 4800MHz", "price": 1600, "ram_type": "DDR5", "ram_size": 16},
    {"name": "16GB (8GBx2) DDR5 5200MHz", "price": 2000, "ram_type": "DDR5", "ram_size": 16},
    {"name": "32GB (16GBx2) DDR5 6000MHz", "price": 4200, "ram_type": "DDR5", "ram_size": 32},
    {"name": "64GB (32GBx2) DDR5 6000MHz", "price": 7500, "ram_type": "DDR5", "ram_size": 64}
]

ssds = [

    {"name": "500GB M.2 NVMe", "price": 1500, "ssd_size": 500},
    {"name": "1TB M.2 NVMe", "price": 2800, "ssd_size": 1000},
    {"name": "2TB M.2 NVMe", "price": 5200, "ssd_size": 2000}

]

# --- ส่วน Loop สร้าง valid_builds ที่แก้ให้ตรงกับ Key ด้านบน ---
valid_builds = []
for cpu in cpus:
    for mb in mbs:
        if cpu['socket'] == mb['socket'] and cpu['ram_support'] == mb['ram_type']:
            for ram in rams:
                if ram['ram_type'] == mb['ram_type']:
                    for gpu in gpus:
                        for ssd in ssds:
                            valid_builds.append({
                                "cpu": cpu['name'],
                                "cpu_brand": cpu['cpu_brand'],
                                "mb": mb['name'],
                                "ram": ram['name'],
                                "ram_size": ram['ram_size'],
                                "gpu": gpu['name'],
                                "gpu_brand": gpu['gpu_brand'],
                                "ssd": ssd['name'],
                                "ssd_size": ssd['ssd_size'],
                                "price": cpu['price'] + mb['price'] + ram['price'] + gpu['price'] + ssd['price']
                            })

import pandas as pd
df = pd.DataFrame(valid_builds)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/build', methods=['POST'])
def build_pc():
    data = request.json
    budget = float(data.get('budget'))
    cpu_brand = data.get('cpu_brand')
    gpu_brand = data.get('gpu_brand')
    ram_size = data.get('ram_size')
    ssd_size = data.get('ssd_size')

    # 1. เริ่มต้นด้วยการ Copy DataFrame ทั้งหมด
    filtered_df = df.copy()

    # 2. กรองตามเงื่อนไข (ถ้าไม่ใช่ "Any" หรือ "อะไรก็ได้" ให้ทำการกรอง)
    if cpu_brand != 'Any':
        filtered_df = filtered_df[filtered_df['cpu_brand'] == cpu_brand]
    
    if gpu_brand != 'Any':
        filtered_df = filtered_df[filtered_df['gpu_brand'] == gpu_brand]

    if ram_size != 'Any':
        filtered_df = filtered_df[filtered_df['ram_size'] == int(ram_size)]

    if ssd_size != 'Any':
        filtered_df = filtered_df[filtered_df['ssd_size'] == int(ssd_size)]

    # 3. กรองงบประมาณ (เฉพาะกรณีที่จำกัดงบ)
    if data.get('is_limited'):
        filtered_df = filtered_df[filtered_df['price'] <= budget]

    # 4. ตรวจสอบว่าหลังจากกรองแล้วเหลือข้อมูลไหม
    if filtered_df.empty:
        return jsonify({
            'status': 'error',
            'message': '❌ ไม่พบสเปคที่ตรงกับเงื่อนไขของคุณในงบที่กำหนด กรุณาเพิ่มงบหรือปรับตัวเลือกอุปกรณ์'
        })

    # 5. ใช้ KNN หรือเลือกตัวที่แรงที่สุด/ใกล้เคียงที่สุด
    # (ตัวอย่าง: เลือกตัวที่ราคาสูงที่สุดภายใต้งบเพื่อให้ได้ของแรงสุด)
    best_match = filtered_df.loc[filtered_df['price'].idxmax()]

    return jsonify({
        'status': 'success',
        'cpu': best_match['cpu'],
        'mb': best_match['mb'],
        'ram': best_match['ram'],
        'gpu': best_match['gpu'],
        'ssd': best_match['ssd'],
        'total_price': int(best_match['price']),
        'change': int(budget - best_match['price'])
    })

if __name__ == '__main__':
    app.run(debug=True)