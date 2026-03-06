import streamlit as st
import pandas as pd
import warnings

# ปิดการแจ้งเตือน
warnings.filterwarnings('ignore')

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="AI PC Builder", page_icon="🖥️")
st.title("🖥️ ระบบจัดสเปคคอมพิวเตอร์อัจฉริยะ")
st.markdown("ระบุงบประมาณและความต้องการของคุณ เพื่อให้ AI ช่วยจัดสเปคที่ดีที่สุด")

# --- 1. ฐานข้อมูลอะไหล่ ---
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
    {"name": "NVIDIA RTX 4090 24GB", "price": 75000, "gpu_brand": "NVIDIA"},
    {"name": "AMD Radeon RX 550 4GB", "price": 1500, "gpu_brand": "AMD"},
    {"name": "AMD Radeon RX 560 4GB", "price": 1800, "gpu_brand": "AMD"},
    {"name": "AMD Radeon RX 570 4GB", "price": 2200, "gpu_brand": "AMD"},
    {"name": "AMD Radeon RX 580 8GB", "price": 2800, "gpu_brand": "AMD"},
    {"name": "AMD Radeon RX 590 8GB", "price": 3500, "gpu_brand": "AMD"}
]

rams = [
    {"name": "4GB DDR4 3200MHz", "price": 450, "ram_type": "DDR4", "ram_size": 4},
    {"name": "8GB DDR4 3200MHz", "price": 700, "ram_type": "DDR4", "ram_size": 8},
    {"name": "16GB (8GBx2) DDR4 3200MHz", "price": 1400, "ram_type": "DDR4", "ram_size": 16},
    {"name": "16GB (8GBx2) DDR5 5200MHz", "price": 2000, "ram_type": "DDR5", "ram_size": 16},
    {"name": "32GB (16GBx2) DDR5 6000MHz", "price": 4200, "ram_type": "DDR5", "ram_size": 32}
]

ssds = [
    {"name": "250GB M.2 NVMe", "price": 500, "ssd_size": 250},
    {"name": "500GB M.2 NVMe", "price": 1500, "ssd_size": 500},
    {"name": "1TB M.2 NVMe", "price": 2800, "ssd_size": 1000},
    {"name": "2TB M.2 NVMe", "price": 5200, "ssd_size": 2000}
]

# --- 2. สร้าง Database ชั่วคราว (Cache ไว้เพื่อความเร็ว) ---
@st.cache_data
def get_all_builds():
    valid_builds = []
    for cpu in cpus:
        for mb in mbs:
            if cpu['socket'] == mb['socket'] and cpu['ram_support'] == mb['ram_type']:
                for ram in rams:
                    if ram['ram_type'] == mb['ram_type']:
                        for gpu in gpus:
                            for ssd in ssds:
                                valid_builds.append({
                                    "cpu": cpu['name'], "cpu_brand": cpu['cpu_brand'],
                                    "mb": mb['name'], "ram": ram['name'], "ram_size": ram['ram_size'],
                                    "gpu": gpu['name'], "gpu_brand": gpu['gpu_brand'],
                                    "ssd": ssd['name'], "ssd_size": ssd['ssd_size'],
                                    "price": cpu['price'] + mb['price'] + ram['price'] + gpu['price'] + ssd['price']
                                })
    return pd.DataFrame(valid_builds)

df = get_all_builds()

# --- 3. ส่วน UI สำหรับรับค่า (Sidebar) ---
st.sidebar.header("⚙️ ตั้งค่าความต้องการ")
budget = st.sidebar.number_input("งบประมาณ (บาท)", min_value=5000, value=25000, step=500)
cpu_choice = st.sidebar.selectbox("ค่าย CPU", ["Any", "Intel", "AMD"])
gpu_choice = st.sidebar.selectbox("ค่าย GPU", ["Any", "NVIDIA", "AMD"])
ram_choice = st.sidebar.selectbox("ขนาด RAM (GB)", ["Any", 8, 16, 32])
ssd_choice = st.sidebar.selectbox("ขนาด SSD (GB)", ["Any", 250, 500, 1000, 2000])

# --- 4. ตรรกะการประมวลผล ---
if st.button("🚀 จัดสเปคเดี๋ยวนี้!"):
    filtered_df = df.copy()

    if cpu_choice != "Any":
        filtered_df = filtered_df[filtered_df['cpu_brand'] == cpu_choice]
    if gpu_choice != "Any":
        filtered_df = filtered_df[filtered_df['gpu_brand'] == gpu_choice]
    if ram_choice != "Any":
        filtered_df = filtered_df[filtered_df['ram_size'] == int(ram_choice)]
    if ssd_choice != "Any":
        filtered_df = filtered_df[filtered_df['ssd_size'] == int(ssd_choice)]
    
    # กรองตามงบประมาณ
    filtered_df = filtered_df[filtered_df['price'] <= budget]

    if not filtered_df.empty:
        # เลือกตัวที่ราคาสูงที่สุดในงบ (เพื่อความแรงสูงสุด)
        best_match = filtered_df.loc[filtered_df['price'].idxmax()]
        
        # แสดงผลลัพธ์
        st.success(f"✅ จัดสเปคสำเร็จ! อยู่ในงบ {budget:,.0f} บาท")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**CPU:** {best_match['cpu']}")
            st.info(f"**Mainboard:** {best_match['mb']}")
            st.info(f"**RAM:** {best_match['ram']}")
        with col2:
            st.info(f"**GPU:** {best_match['gpu']}")
            st.info(f"**SSD:** {best_match['ssd']}")
            st.warning(f"**ราคารวมทั้งสิ้น:** {best_match['price']:,.0f} บาท")
        
        st.write(f"💰 เงินเหลือ: {budget - best_match['price']:,.0f} บาท")
    else:
        st.error("❌ ไม่พบสเปคที่ตรงกับเงื่อนไขในงบนี้ ลองเพิ่มงบหรือปรับตัวเลือกดูครับ")
