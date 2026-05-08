import streamlit as st
import os
from datetime import datetime

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="1998 COFFEE - POS", page_icon="☕", layout="centered")

# --- 2. CSS "SIÊU CẤP" CHỈNH MÀU CHO NỀN TỐI ---
st.markdown("""
    <style>
    /* Ép màu chữ tiêu đề (Label) thành màu trắng sáng cho dễ đọc */
    .stSelectbox label, .stRadio label, .stMultiSelect label, p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 2px #000; /* Thêm bóng cho chữ nổi lên */
    }
    
    /* Chỉnh màu cho các mục đã chọn bên trong ô (Selectbox/Multiselect) */
    div[data-baseweb="select"] > div {
        color: #000000 !important; /* Chữ trong ô chọn để màu đen cho dễ nhìn trên nền trắng của ô */
        font-weight: 500;
    }

    /* Nút bấm màu Vàng Gold cho sang chảnh trên nền đen */
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 3.8em;
        background-color: #D4AF37; /* Màu Gold */
        color: #000000 !important; /* Chữ đen trên nền vàng cho nổi */
        font-weight: bold;
        border: 2px solid #FFFFFF;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFD700;
        border: 2px solid #D4AF37;
    }

    /* Tab menu: Sửa màu chữ Tab để không bị mờ */
    .stTabs [data-baseweb="tab"] p {
        color: #BBBBBB !important; /* Chữ tab chưa chọn màu xám nhẹ */
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important; /* Chữ tab đang chọn màu trắng */
        font-size: 1.2rem !important;
    }

    /* Hộp hiển thị Tổng tiền (Metric) */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E; /* Nền hộp đen xám */
        border: 2px solid #D4AF37;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] > div { color: #FFFFFF !important; }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; font-weight: 800 !important; }
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

# --- 4. KHỞI TẠO & DỮ LIỆU ---
if 'cart' not in st.session_state: st.session_state.cart = []

menu = {
    "CÀ PHÊ MÁY": {
        "Cà phê đen": {"M": 17000, "L": 24000},
        "Cà phê sữa": {"M": 20000, "L": 27000},
        "Cà phê muối": {"M": 25000, "L": 32000},
        "Bạc xỉu": {"M": 22000, "L": 27000},
        "Cà phê sữa tươi": {"M": 22000, "L": 27000},
        "Cà phê sữa gấu": {"M": None, "L": 33000},
        "Cà phê mix": {"M": 25000, "L": 30000},
        "Cà phê sữa dừa sương sáo": {"M": 29000, "L": 35000},
    },
    "MATCHA/CACAO/MÔN": {
        "Matcha latte": {"M": 22000, "L": 29000},
        "Matcha kem muối": {"M": 27000, "L": 32000},
        "Cacao latte": {"M": 20000, "L": 25000},
        "Môn latte": {"M": 20000, "L": 25000},
        "Môn muối": {"M": 25000, "L": 30000},
    }
}
tops = {"Thêm matcha": 5000, "Kem Muối": 5000, "Sương Sáo": 5000}

# --- 5. GIAO DIỆN CHÍNH ---
st.title("☕ 1998 COFFEE")
st.markdown("📍 *145 Bà Huyện Thanh Quan, Q3*")

tab1, tab2, tab3 = st.tabs(["⚡ LÊN ĐƠN", "📋 GIỎ HÀNG", "📈 DOANH THU"])

with tab1:
    st.markdown("### 🛠 Tùy chọn món")
    cat = st.selectbox("Chọn nhóm đồ uống:", list(menu.keys()))
    m = st.selectbox("Tên món:", list(menu[cat].keys()))
    
    szs = [s for s in ["M", "L"] if menu[cat][m][s] is not None]
    sz = st.radio("Kích cỡ (Size):", szs, horizontal=True)
    
    t = st.multiselect("Thêm Topping đi ông:", list(tops.keys()))
    
    p = menu[cat][m][sz] + (len(t) * 5000)
    st.markdown(f"## Tạm tính: <span style='color:#D4AF37'>{p:,}đ</span>", unsafe_allow_html=True)
    
    if st.button("🛒 THÊM VÀO ĐƠN HÀNG"):
        st.session_state.cart.append({"name": f"{m} ({sz})", "price": p})
        st.toast(f"Đã thêm {m} vào giỏ!")

with tab2:
    if st.session_state.cart:
        total_bill = 0
        st.markdown("### 📝 Danh sách món đang chọn:")
        for i, it in enumerate(st.session_state.cart):
            st.write(f"{i+1}. **{it['name']}** - `{it['price']:,}đ`")
            total_bill += it['price']
        
        st.divider()
        st.metric("TỔNG TIỀN ĐƠN NÀY", f"{total_bill:,} VNĐ")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ CHỐT & THANH TOÁN"):
                save_revenue(total_bill)
                st.session_state.cart = []
                st.success("Đã ghi nhận doanh thu!")
                st.rerun()
        with col2:
            if st.button("❌ XÓA ĐƠN"):
                st.session_state.cart = []
                st.rerun()
    else:
        st.info("Chưa có món nào trong đơn hàng ông ơi! Qua tab Lên đơn đi.")

with tab3:
    st.subheader("📊 Báo cáo doanh thu tích lũy")
    r = get_revenue()
    st.metric("TỔNG TIỀN ĐÃ BÁN", f"{r:,} VNĐ")
    
    st.write("---")
    if st.button("🗑️ RESET DOANH THU (CẨN THẬN)"):
        reset_revenue()
        st.rerun()
        st.rerun()
