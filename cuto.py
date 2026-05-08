import streamlit as st

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(
    page_title="1998 COFFEE - POS", 
    page_icon="☕",
    layout="centered"
)

# 2. PHẦN CSS ĐỂ CHỈNH MÀU CHỮ (Sửa lỗi mờ chữ trên Dark Mode)
st.markdown("""
    <style>
    /* Nền chính của App */
    .main { background-color: #f5f5f5; }
    
    /* Nút bấm màu nâu cafe, chữ trắng */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #6F4E37;
        color: white !important;
        font-weight: bold;
        border: none;
    }
    
    /* Hộp hiển thị Tổng tiền */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #6F4E37;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Ép màu chữ Label (TỔNG CỘNG) thành đen */
    div[data-testid="stMetricLabel"] > div {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    /* Ép màu con số tiền thành đỏ đậm cho nổi */
    div[data-testid="stMetricValue"] > div {
        color: #d32f2f !important;
        text-align: center;
        font-weight: 800 !important;
    }

    /* Chỉnh màu các tab cho rõ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #eeeeee;
        border-radius: 10px 10px 0px 0px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DỮ LIỆU MENU (Đã cập nhật theo ảnh menu tại quầy)
menu_data = {
    "CÀ PHÊ MÁY": {
        "Cà phê đen": {"M": 17000, "L": 24000},
        "Cà phê sữa": {"M": 20000, "L": 27000},
        "Cà phê muối": {"M": 25000, "L": 32000},
        "Bạc xỉu": {"M": 22000, "L": 27000},
        "Cà phê caramel": {"M": 25000, "L": 30000},
        "Cà phê sữa tươi": {"M": 22000, "L": 27000},
        "Cà phê sữa oatside": {"M": 25000, "L": 30000},
        "Cà phê sữa gấu": {"M": None, "L": 33000},
        "Cà phê mix": {"M": 25000, "L": 30000},
        "Cà phê sữa dừa sương sáo": {"M": 29000, "L": 35000},
    },
    "MATCHA NHẬT": {
        "Matcha latte": {"M": 22000, "L": 29000},
        "Matcha kem muối": {"M": 27000, "L": 32000},
        "Matcha sữa oatside": {"M": 25000, "L": 32000},
        "Matcha sữa gấu": {"M": None, "L": 35000},
        "Matcha sữa dừa": {"M": 27000, "L": 35000},
    },
    "CACAO NGUYÊN CHẤT": {
        "Cacao latte": {"M": 20000, "L": 25000},
        "Cacao muối": {"M": 25000, "L": 30000},
        "Cacao sữa oatside": {"M": 25000, "L": 30000},
        "Cacao sữa gấu": {"M": None, "L": 33000},
    },
    "KHOAI MÔN": {
        "Môn latte": {"M": 20000, "L": 25000},
        "Môn muối": {"M": 25000, "L": 30000},
        "Môn sữa oatside": {"M": 25000, "L": 30000},
        "Môn sữa gấu": {"M": None, "L": 33000},
    }
}

topping_data = {"Thêm matcha": 5000, "Kem Muối": 5000, "Sương Sáo": 5000}

# 4. GIAO DIỆN CHÍNH
st.title("☕ 1998 COFFEE")
st.markdown("📍 *145 Bà Huyện Thanh Quan, Q3*")

tab1, tab2 = st.tabs(["⚡ LÊN ĐƠN", "📋 GIỎ HÀNG"])

with tab1:
    cat_choice = st.selectbox("Nhóm đồ uống:", list(menu_data.keys()))
    item_choice = st.selectbox("Tên món:", list(menu_data[cat_choice].keys()))
    
    # Lọc size khả dụng
    available_sizes = [s for s in ["M", "L"] if menu_data[cat_choice][item_choice][s] is not None]
    size_choice = st.radio("Chọn Size:", available_sizes, horizontal=True)
    
    selected_toppings = st.multiselect("Topping (5k):", list(topping_data.keys()))
    
    # Tính giá
    base_p = menu_data[cat_choice][item_choice][size_choice]
    top_p = len(selected_toppings) * 5000
    total_p = base_p + top_p
    
    st.markdown(f"### Tạm tính: {total_p:,} VNĐ")
    
    if st.button("🛒 XÁC NHẬN THÊM"):
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        
        st.session_state.cart.append({
            "name": f"{item_choice} ({size_choice})",
            "price": total_p
        })
        st.toast(f"Đã thêm {item_choice} vào đơn!")

with tab2:
    if 'cart' in st.session_state and st.session_state.cart:
        grand_total = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"{i+1}. {item['name']} - **{item['price']:,}đ**")
            grand_total += item['price']
        
        st.divider()
        # Phần Metric đã được CSS ép màu đen và đỏ ở trên
        st.metric(label="TỔNG CỘNG", value=f"{grand_total:,} VNĐ")
        
        if st.button("❌ XÓA HẾT ĐƠN"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("Chưa có món nào trong đơn hàng ông ơi!")
