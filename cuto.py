import streamlit as st

# 1. Cấu hình giao diện (Dark mode & Layout gọn)
st.set_page_config(
    page_title="1998 COFFEE - POS", 
    page_icon="☕",
    layout="centered"
)

# Thêm CSS để giao diện trên điện thoại đẹp hơn
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #6F4E37;
        color: white;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Dữ liệu Menu (Giữ nguyên từ bản trước của ông)
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
        "Cacao sữa gấu": {"M": None, "L": 33000},
    },
    "KHOAI MÔN": {
        "Môn latte": {"M": 20000, "L": 25000},
        "Môn muối": {"M": 25000, "L": 30000},
        "Môn sữa gấu": {"M": None, "L": 33000},
    }
}

topping_data = {"Thêm matcha": 5000, "Kem Muối": 5000, "Sương Sáo": 5000}

# --- GIAO DIỆN CHÍNH ---
st.title("☕ 1998 COFFEE")
st.write("📍 145 Bà Huyện Thanh Quan, Q3")

# Dùng Tabs cho đỡ rối màn hình điện thoại
tab1, tab2 = st.tabs(["⚡ Lên đơn", "📋 Giỏ hàng"])

with tab1:
    cat_choice = st.selectbox("Chọn nhóm:", list(menu_data.keys()))
    item_choice = st.selectbox("Chọn món:", list(menu_data[cat_choice].keys()))
    
    # Kiểm tra Size
    sizes = [s for s in ["M", "L"] if menu_data[cat_choice][item_choice][s] is not None]
    size_choice = st.radio("Chọn Size:", sizes, horizontal=True)
    
    selected_toppings = st.multiselect("Topping (+5k):", list(topping_data.keys()))
    
    # Tính tiền món hiện tại
    price = menu_data[cat_choice][item_choice][size_choice] + len(selected_toppings)*5000
    
    st.subheader(f"Giá: {price:,} VNĐ")
    
    if st.button("🛒 THÊM VÀO ĐƠN"):
        if 'cart' not in st.session_state: st.session_state.cart = []
        st.session_state.cart.append({"name": f"{item_choice} ({size_choice})", "price": price})
        st.toast(f"Đã thêm {item_choice}!")

with tab2:
    if 'cart' in st.session_state and st.session_state.cart:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"{i+1}. {item['name']} - **{item['price']:,}đ**")
            total += item['price']
        
        st.divider()
        st.metric("TỔNG CỘNG", f"{total:,} VNĐ")
        
        if st.button("❌ XÓA HẾT"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.write("Giỏ hàng đang trống ông ơi!")