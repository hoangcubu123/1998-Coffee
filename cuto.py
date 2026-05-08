import streamlit as st
import os

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="1998 COFFEE - POS", page_icon="☕", layout="centered")

# --- 2. CSS ĐẶC TRỊ LỖI CHỮ MỜ TRONG Ô CHỌN ---
st.markdown("""
    <style>
    /* 1. Ép tất cả nhãn (Label) thành màu trắng sáng */
    .stSelectbox label, .stRadio label, .stMultiSelect label, p, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* 2. ĐẶC TRỊ: Chỉnh chữ TRONG ô Selectbox thành màu trắng hoặc vàng Gold */
    div[data-baseweb="select"] > div {
        color: #D4AF37 !important; /* Chữ khi đã chọn sẽ có màu vàng Gold */
        background-color: #262730 !important; /* Nền ô chọn tối lại cho chuyên nghiệp */
        font-weight: 600 !important;
    }
    
    /* Chỉnh danh sách xổ xuống (Dropdown list) */
    div[data-baseweb="popover"] ul {
        background-color: #262730 !important;
    }
    div[data-baseweb="popover"] li {
        color: #FFFFFF !important; /* Chữ trong danh sách xổ xuống màu trắng */
    }

    /* 3. Nút bấm màu Vàng Gold sang trọng */
    div.stButton > button {
        width: 100%; border-radius: 12px; height: 3.8em;
        background-color: #D4AF37; color: #000000 !important;
        font-weight: bold; border: none;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }

    /* 4. Chỉnh Tab cho nổi bật */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HỆ THỐNG LƯU TRỮ (GIỮ NGUYÊN ĐỂ KHÔNG MẤT DOANH THU) ---
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

# --- 4. GIỎ HÀNG & MENU ---
if 'cart' not in st.session_state: st.session_state.cart = []

menu = {
    "CÀ PHÊ MÁY": {
        "Cà phê đen": {"M": 17000, "L": 24000},
        "Cà phê sữa": {"M": 20000, "L": 27000},
        "Cà phê muối": {"M": 25000, "L": 32000},
        "Bạc xỉu": {"M": 22000, "L": 27000},
        "Cà phê sữa tươi": {"M": 22000, "L": 27000},
        "Cà phê sữa gấu": {"M": None, "L": 33000},
    },
    "MATCHA/CACAO/MÔN": {
        "Matcha latte": {"M": 22000, "L": 29000},
        "Cacao latte": {"M": 20000, "L": 25000},
        "Môn latte": {"M": 20000, "L": 25000},
    }
}
tops = {"Thêm matcha": 5000, "Kem Muối": 5000, "Sương Sáo": 5000}

# --- 5. GIAO DIỆN ---
st.title("☕ 1998 COFFEE")
st.markdown("📍 *145 Bà Huyện Thanh Quan, Q3*")

tab1, tab2, tab3 = st.tabs(["⚡ LÊN ĐƠN", "📋 GIỎ HÀNG", "📈 DOANH THU"])

with tab1:
    st.subheader("🛠 Chọn món tại đây")
    cat = st.selectbox("1. Chọn nhóm đồ uống:", list(menu.keys()))
    m = st.selectbox("2. Chọn tên món:", list(menu[cat].keys()))
    
    szs = [s for s in ["M", "L"] if menu[cat][m][s] is not None]
    sz = st.radio("3. Kích cỡ (Size):", szs, horizontal=True)
    
    t = st.multiselect("4. Thêm Topping:", list(tops.keys()))
    
    p = menu[cat][m][sz] + (len(t) * 5000)
    st.markdown(f"## Tạm tính: <span style='color:#D4AF37'>{p:,}đ</span>", unsafe_allow_html=True)
    
    if st.button("🛒 THÊM VÀO GIỎ HÀNG"):
        st.session_state.cart.append({"name": f"{m} ({sz})", "price": p})
        st.toast(f"Đã thêm {m}!")

with tab2:
    if st.session_state.cart:
        total = 0
        for i, it in enumerate(st.session_state.cart):
            st.write(f"{i+1}. **{it['name']}** - `{it['price']:,}đ`")
            total += it['price']
        st.divider()
        st.write(f"### Tổng đơn: :red[{total:,}đ]")
        if st.button("✅ CHỐT ĐƠN & LƯU DOANH THU"):
            save_revenue(total)
            st.session_state.cart = []
            st.success("Đã xong!")
            st.rerun()
    else:
        st.info("Trống trơn à ông!")

with tab3:
    st.subheader("Doanh thu tích lũy")
    rev = get_revenue()
    st.write(f"## {rev:,} VNĐ")
    if st.button("🗑️ RESET"):
        reset_revenue()
        st.rerun()
