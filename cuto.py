import streamlit as st
import os
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="1998 COFFEE - POS", page_icon="☕", layout="centered")

# --- 2. CSS TỔNG LỰC (Sửa lỗi chữ mờ & Làm đẹp giao diện) ---
st.markdown("""
    <style>
    /* Ép chữ đen đậm cho toàn bộ nhãn (Label) để nhìn rõ trên mọi chế độ */
    .stSelectbox label, .stRadio label, .stMultiSelect label, p, .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Chỉnh màu chữ trong ô chọn Selectbox */
    div[data-baseweb="select"] > div { color: black !important; font-weight: 600; }

    /* Nút bấm màu nâu cafe chuyên nghiệp */
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background-color: #6F4E37; color: white !important; font-weight: bold;
        border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* Hộp hiển thị Tổng tiền (Metric) */
    div[data-testid="stMetric"] {
        background-color: #ffffff; border: 2px solid #6F4E37;
        padding: 15px; border-radius: 15px; text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] > div { color: #000000 !important; font-size: 1.1rem !important; }
    div[data-testid="stMetricValue"] > div { color: #d32f2f !important; font-weight: 800 !important; }

    /* Chỉnh tab rõ ràng, dễ bấm trên điện thoại */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f0f0; border-radius: 8px 8px 0 0; 
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #6F4E37 !important; color: white !important; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HỆ THỐNG LƯU TRỮ VĨNH VIỄN ---
DB_FILE = "revenue_data.txt"

def get_revenue():
    if not os.path.exists(DB_FILE): return 0.0
    with open(DB_FILE, "r") as f:
        try: return float(f.read())
        except: return 0.0

def save_revenue(amount):
    current = get_revenue()
    with open(DB_FILE, "w") as f:
        f.write(str(current + amount))

def reset_revenue():
    if os.path.exists(DB_FILE): os.remove(DB_FILE)

# --- 4. GIỎ HÀNG & DỮ LIỆU ---
if 'cart' not in st.session_state: st.session_state.cart = []

# Menu cập nhật chuẩn tại quầy
menu = {
    "CÀ PHÊ MÁY": {
        "Cà phê đen": {"M": 17000, "L": 24000},
        "Cà phê sữa": {"M": 20000, "L": 27000},
        "Cà phê muối": {"M": 25000, "L": 32000},
        "Bạc xỉu": {"M": 22000, "L": 27000},
        "Cà phê sữa tươi": {"M": 22000, "L": 27000},
        "Cà phê sữa gấu": {"M": None, "L": 33000},
        "Cà phê sữa dừa sương sáo": {"M": 29000, "L": 35000},
    },
    "MATCHA/CACAO/MÔN": {
        "Matcha latte": {"M": 22000, "L": 29000},
        "Matcha kem muối": {"M": 27000, "L": 32000},
        "Cacao latte": {"M": 20000, "L": 25000},
        "Cacao muối": {"M": 25000, "L": 30000},
        "Môn latte": {"M": 20000, "L": 25000},
        "Môn muối": {"M": 25000, "L": 30000},
    }
}
tops = {"Thêm matcha": 5000, "Kem Muối": 5000, "Sương Sáo": 5000}

# --- 5. GIAO DIỆN CHÍNH ---
st.title("☕ 1998 COFFEE")
tab1, tab2, tab3 = st.tabs(["⚡ LÊN ĐƠN", "📋 GIỎ HÀNG", "📈 DOANH THU"])

with tab1:
    c = st.selectbox("Chọn nhóm:", list(menu.keys()))
    m = st.selectbox("Chọn món:", list(menu[c].keys()))
    szs = [s for s in ["M", "L"] if menu[c][m][s] is not None]
    sz = st.radio("Chọn Size:", szs, horizontal=True)
    t = st.multiselect("Thêm Topping:", list(tops.keys()))
    
    # Tính giá tạm thời
    p = menu[c][m][sz] + (len(t) * 5000)
    st.markdown(f"### Tạm tính: :red[{p:,}đ]")
    
    if st.button("🛒 THÊM VÀO GIỎ"):
        st.session_state.cart.append({"name": f"{m} ({sz})", "price": p})
        st.toast(f"Đã thêm {m}!")

with tab2:
    if st.session_state.cart:
        total_bill = 0
        st.write("**Chi tiết đơn hàng:**")
        for i, it in enumerate(st.session_state.cart):
            st.write(f"{i+1}. {it['name']} - **{it['price']:,}đ**")
            total_bill += it['price']
        st.divider()
        st.metric("TỔNG TIỀN ĐƠN NÀY", f"{total_bill:,} VNĐ")
        
        if st.button("✅ CHỐT ĐƠN & THANH TOÁN"):
            save_revenue(total_bill) # Lưu vĩnh viễn vào file
            st.session_state.cart = []
            st.success("Đã thanh toán và lưu doanh thu!")
            st.balloons()
            st.rerun()
            
        if st.button("❌ HỦY TOÀN BỘ ĐƠN"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("Giỏ hàng đang trống ông ơi!")

with tab3:
    st.subheader("Báo cáo doanh thu vĩnh viễn")
    r = get_revenue()
    st.metric("TỔNG DOANH THU", f"{r:,} VNĐ")
    st.caption("Dữ liệu này được lưu vĩnh viễn vào file revenue_data.txt")
    
    st.write("---")
    if st.button("🗑️ RESET DOANH THU (SANG NGÀY MỚI)"):
        reset_revenue()
        st.rerun()
