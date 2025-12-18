import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. KHỞI TẠO HỆ THỐNG AN TOÀN (FIX KEYERROR) ---
if 'os' not in st.session_state:
    st.session_state.os = {
        "page": "Desktop",
        "theme": "#00f2ff",
        "os_version": "35.0",
        "is_locked": False,
        "pin": "1234"
    }

# Khởi tạo dữ liệu bãi xe (20 chỗ)
if 'parking_data' not in st.session_state:
    st.session_state.parking_data = pd.DataFrame({
        "ID": range(1, 21),
        "Vị trí": [f"Khu A-{i+1:02d}" for i in range(20)],
        "Trạng thái": ["Trống"] * 20,
        "Biển số": [""] * 20,
        "Giờ vào": [None] * 20,
        "Doanh thu": [0.0] * 20
    })

# Khởi tạo lịch sử doanh thu
if 'revenue_history' not in st.session_state:
    st.session_state.revenue_history = 0.0

def nav(p):
    st.session_state.os["page"] = p
    st.rerun()

# --- 2. GIAO DIỆN CHUẨN ---
st.set_page_config(page_title="Titan Parking v35", layout="wide")

# Lấy version an toàn để không bao giờ bị KeyError
current_ver = st.session_state.os.get("os_version", "35.0")
theme_color = st.session_state.os.get("theme", "#00f2ff")

st.markdown(f"""
<style>
    .stApp {{ background-color: #0b0e11; color: white; }}
    .status-bar {{ padding: 10px; background: #1a1c23; border-bottom: 2px solid {theme_color}; text-align: right; font-family: monospace; }}
    .slot-box {{
        padding: 15px; border-radius: 12px; border: 1px solid #343a40;
        text-align: center; margin-bottom: 10px; transition: 0.3s;
        background: #161b22;
    }}
    .metric-card {{
        background: #21262d; padding: 20px; border-radius: 10px; border-left: 5px solid {theme_color};
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. THANH TRẠNG THÁI ---
st.markdown(f"<div class='status-bar'>🛡️ KERNEL STABLE | 🛰️ v{current_ver} | 🔑 {st.session_state.os.get('page')} | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---

# 4.1 MÀN HÌNH CHÍNH
if st.session_state.os["page"] == "Desktop":
    st.title("🌌 Titan Command Center")
    
    # Widgets nhanh
    c1, c2, c3 = st.columns(3)
    with c1:
        empty = len(st.session_state.parking_data[st.session_state.parking_data["Trạng thái"] == "Trống"])
        st.markdown(f"<div class='metric-card'><h3>Chỗ trống</h3><h2>{empty} / 20</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>Doanh thu</h3><h2>{st.session_state.revenue_history:,.0f} VNĐ</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h3>Thời gian</h3><h2>{datetime.datetime.now().strftime('%d/%m/%Y')}</h2></div>", unsafe_allow_html=True)

    st.write("---")
    # Menu App
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("🅿️ QUẢN LÝ XE", use_container_width=True): nav("Parking")
    with m2:
        if st.button("🌳 VƯỜN HẸ", use_container_width=True): nav("Garden")
    with m3:
        if st.button("📈 THỐNG KÊ", use_container_width=True): nav("Stats")
    with m4:
        if st.button("⚙️ CÀI ĐẶT", use_container_width=True): nav("Settings")

# 4.2 QUẢN LÝ BÃI XE (PARKING)
elif st.session_state.os["page"] == "Parking":
    st.button("🔙 QUAY LẠI", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Trạm Kiểm Soát Bãi Xe")

    # Bộ lọc tìm kiếm
    search_query = st.text_input("🔍 Tìm kiếm biển số xe:", placeholder="Nhập biển số...")

    # Hiển thị Grid bãi xe
    cols = st.columns(5)
    for index, row in st.session_state.parking_data.iterrows():
        is_match = search_query.upper() in row["Biển số"].upper() if search_query else True
        if not is_match: continue
            
        with cols[index % 5]:
            status = row["Trạng thái"]
            color = "#2ea043" if status == "Trống" else "#f85149"
            
            st.markdown(f"""<div class='slot-box' style='border-top: 4px solid {color};'>
                <small>{row['Vị trí']}</small><br>
                <b style='color:{color};'>{'TRỐNG' if status == 'Trống' else row['Biển số']}</b>
            </div>""", unsafe_allow_html=True)
            
            if st.button("Chi tiết", key=f"slot_{index}", use_container_width=True):
                st.session_state.selected_slot = index
                nav("Detail")

# 4.3 CHI TIẾT VÀ XỬ LÝ XE (CHECK-IN/CHECK-OUT)
elif st.session_state.os["page"] == "Detail":
    idx = st.session_state.selected_slot
    slot = st.session_state.parking_data.iloc[idx]
    
    st.header(f"📍 Chi tiết vị trí: {slot['Vị trí']}")
    
    if slot["Trạng thái"] == "Trống":
        st.info("Trạng thái: Đang trống. Vui lòng nhập thông tin để nhận xe.")
        bien_so = st.text_input("Biển số xe:", placeholder="30A-12345")
        if st.button("XÁC NHẬN CHO XE VÀO"):
            if bien_so:
                st.session_state.parking_data.at[idx, "Trạng thái"] = "Đã đỗ"
                st.session_state.parking_data.at[idx, "Biển số"] = bien_so.upper()
                st.session_state.parking_data.at[idx, "Giờ vào"] = datetime.datetime.now()
                st.success("Đã ghi nhận xe vào bãi!")
                time.sleep(1)
                nav("Parking")
            else:
                st.warning("Bạn chưa nhập biển số!")
    else:
        st.warning(f"Xe đang đỗ: {slot['Biển số']}")
        vào_lúc = slot["Giờ vào"]
        st.write(f"Thời gian vào: {vào_lúc.strftime('%H:%M:%S - %d/%m/%Y')}")
        
        # Tính tiền
        duration = datetime.datetime.now() - vào_lúc
        hours = max(1, duration.seconds // 3600 + (1 if duration.seconds % 3600 > 0 else 0))
        price = hours * 10000 # 10k mỗi giờ
        
        st.subheader(f"💰 Phí gửi xe: {price:,.0f} VNĐ")
        st.caption(f"(Thời gian gửi: {hours} giờ)")
        
        if st.button("XÁC NHẬN TRẢ XE & THU TIỀN"):
            st.session_state.revenue_history += price
            st.session_state.parking_data.at[idx, "Trạng thái"] = "Trống"
            st.session_state.parking_data.at[idx, "Biển số"] = ""
            st.session_state.parking_data.at[idx, "Giờ vào"] = None
            st.balloons()
            st.success(f"Đã thu {price:,.0f} VNĐ. Chúc quý khách thượng lộ bình an!")
            time.sleep(1)
            nav("Parking")

    if st.button("HỦY BỎ"): nav("Parking")

# 4.4 CÀI ĐẶT (SETTINGS)
elif st.session_state.os["page"] == "Settings":
    st.button("🔙 QUAY LẠI", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Cài đặt hệ thống")
    
    tab1, tab2 = st.tabs(["Cấu hình", "Dữ liệu"])
    with tab1:
        st.session_state.os["theme"] = st.color_picker("Đổi màu chủ đạo", st.session_state.os["theme"])
        st.write(f"Phiên bản Kernel: {st.session_state.os['os_version']}")
    with tab2:
        if st.button("XÓA TẤT CẢ DỮ LIỆU XE"):
            del st.session_state.parking_data
            st.rerun()

# 4.5 VƯỜN HẸ (GARDEN)
elif st.session_state.os["page"] == "Garden":
    st.button("🔙 QUAY LẠI", on_click=lambda: nav("Desktop"))
    st.header("🌳 Khu Vườn Hẹ Của Boss")
    st.write("Đừng quên tưới nước cho hẹ sau khi quản lý bãi xe nhé!")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Allium_tuberosum_flowers.jpg/800px-Allium_tuberosum_flowers.jpg", caption="Hẹ đang phát triển tốt!", width=400)
    if st.button("Tưới nước 💦"): st.toast("Hẹ đã được uống nước!")
