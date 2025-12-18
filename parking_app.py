import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. KHỞI TẠO HỆ THỐNG (FIX KEYERROR) ---
if 'os' not in st.session_state:
    st.session_state.os = {
        "page": "Desktop",
        "theme": "#00f2ff",
        "is_dark": True,
        "os_version": "34.0",
        "pin": "1234"
    }

# Khởi tạo dữ liệu bãi xe (Nếu chưa có)
if 'parking_data' not in st.session_state:
    # Tạo 20 vị trí trống mặc định
    st.session_state.parking_data = pd.DataFrame({
        "Vị trí": [f"Slot {i+1}" for i in range(20)],
        "Trạng thái": ["Trống"] * 20,
        "Biển số": [""] * 20,
        "Giờ vào": [None] * 20,
        "Giá tiền (h)": [10000] * 20
    })

def nav(p):
    st.session_state.os["page"] = p
    st.rerun()

# --- 2. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan Parking OS v34", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; }}
    .status-bar {{ padding: 10px; background: #111; border-bottom: 1px solid {st.session_state.os['theme']}44; text-align: right; }}
    .slot-card {{
        padding: 15px; border-radius: 10px; border: 1px solid #333;
        text-align: center; margin-bottom: 10px; transition: 0.3s;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. STATUS BAR ---
st.markdown(f"<div class='status-bar'>🅿️ TITAN PARKING PRO | v{st.session_state.os['os_version']} | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)

# --- 4. NAVIGATION ---

# MÀN HÌNH CHÍNH
if st.session_state.os["page"] == "Desktop":
    st.title("🛡️ TITAN CENTRAL CONTROL")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🅿️ QUẢN LÝ BÃI XE"): nav("Parking")
    with col2:
        if st.button("🌳 VƯỜN HẸ"): nav("Garden")
    with col3:
        if st.button("⚙️ CÀI ĐẶT"): nav("Settings")
    with col4:
        if st.button("🏪 CỬA HÀNG"): nav("Store")

# MÀN HÌNH QUẢN LÝ BÃI XE (TÍNH NĂNG CHÍNH)
elif st.session_state.os["page"] == "Parking":
    st.button("🔙 VỀ MENU CHÍNH", on_click=lambda: nav("Desktop"))
    st.header("🅿️ HỆ THỐNG QUẢN LÝ XE THÔNG MINH")
    
    # Khu vực thống kê nhanh
    empty_slots = len(st.session_state.parking_data[st.session_state.parking_data["Trạng thái"] == "Trống"])
    st.metric("Chỗ trống hiện tại", f"{empty_slots} / 20", f"{empty_slots*5}%")

    # Hiển thị sơ đồ bãi xe dạng Grid
    st.subheader("📍 Sơ đồ bãi xe")
    cols = st.columns(5)
    for index, row in st.session_state.parking_data.iterrows():
        with cols[index % 5]:
            is_empty = row["Trạng thái"] == "Trống"
            color = "green" if is_empty else "red"
            icon = "🅿️" if is_empty else "🚗"
            
            st.markdown(f"""<div class='slot-card' style='border-color: {color};'>
                <h3 style='color:{color};'>{icon}</h3>
                <b>{row['Vị trí']}</b><br>
                <small>{row['Biển số'] if row['Biển số'] else 'Trống'}</small>
            </div>""", unsafe_allow_html=True)
            
            if st.button("Cập nhật", key=f"upd_{index}"):
                st.session_state.current_slot = index
                nav("SlotDetail")

    st.divider()
    st.subheader("📝 Danh sách chi tiết")
    st.dataframe(st.session_state.parking_data, use_container_width=True)

# CHI TIẾT VỊ TRÍ ĐỖ
elif st.session_state.os["page"] == "SlotDetail":
    idx = st.session_state.current_slot
    slot_info = st.session_state.parking_data.iloc[idx]
    
    st.header(f"📍 Chi tiết {slot_info['Vị trí']}")
    
    if slot_info["Trạng thái"] == "Trống":
        st.subheader("Nhận xe vào bãi")
        bien_so = st.text_input("Nhập biển số xe:")
        if st.button("XÁC NHẬN VÀO BÃI"):
            if bien_so:
                st.session_state.parking_data.at[idx, "Trạng thái"] = "Đã đỗ"
                st.session_state.parking_data.at[idx, "Biển số"] = bien_so
                st.session_state.parking_data.at[idx, "Giờ vào"] = datetime.datetime.now().strftime("%H:%M:%S")
                st.success(f"Xe {bien_so} đã vào vị trí {slot_info['Vị trí']}")
                time.sleep(1)
                nav("Parking")
            else:
                st.error("Vui lòng nhập biển số!")
    else:
        st.subheader("Trả xe & Thanh toán")
        st.info(f"Biển số: {slot_info['Biển số']} | Vào lúc: {slot_info['Giờ vào']}")
        
        # Giả lập tính tiền (Ví dụ 10k/h, tối thiểu 10k)
        st.write("💰 Tổng tiền dự kiến: **10,000 VNĐ**")
        
        if st.button("XÁC NHẬN TRẢ XE & THU TIỀN"):
            st.session_state.parking_data.at[idx, "Trạng thái"] = "Trống"
            st.session_state.parking_data.at[idx, "Biển số"] = ""
            st.session_state.parking_data.at[idx, "Giờ vào"] = None
            st.balloons()
            st.success("Đã thanh toán và giải phóng chỗ đỗ!")
            time.sleep(1)
            nav("Parking")

    if st.button("HỦY BỎ"): nav("Parking")

# CÁC MÀN HÌNH KHÁC (GIỮ NGUYÊN ĐỂ TRÁNH LỖI)
elif st.session_state.os["page"] == "Settings":
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Cài đặt hệ thống")
    st.write(f"Phiên bản: {st.session_state.os['os_version']}")
    if st.button("Reset Bãi Xe"):
        del st.session_state.parking_data
        st.rerun()

else:
    st.button("🔙 BACK", on_click=lambda: nav("Desktop"))
    st.info(f"Trang {st.session_state.os['page']} đang được bảo trì.")
