import streamlit as st
import pandas as pd
import datetime
import time
import random

# --- 1. CORE OS ENGINE ---
if 'page' not in st.session_state: st.session_state.page = "Desktop"
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'limit_min' not in st.session_state: st.session_state.limit_min = 45
if 'xp' not in st.session_state: st.session_state.xp = 100
if 'theme_color' not in st.session_state: st.session_state.theme_color = "#00f2ff"
if 'dev_clicks' not in st.session_state: st.session_state.dev_clicks = 0
if 'is_dark' not in st.session_state: st.session_state.is_dark = True

# --- 2. LOGIC PIN & SỨC KHỎE ---
elapsed = (time.time() - st.session_state.start_time) / 60
battery = max(0, 100 - int((elapsed / st.session_state.limit_min) * 100))

if battery <= 0:
    st.session_state.page = "RestMode"

# --- 3. GIAO DIỆN SIÊU CẤP (CYBER-TECH) ---
st.set_page_config(page_title="Titan Omega OS", layout="wide")
theme_bg = "#050505" if st.session_state.is_dark else "#f0f2f6"
theme_txt = st.session_state.theme_color if st.session_state.is_dark else "#333333"

st.markdown(f"""
<style>
    .stApp {{ background-color: {theme_bg}; color: {theme_txt}; }}
    .stButton>button {{
        width: 100%; height: 75px; border-radius: 12px;
        background: {"#111" if st.session_state.is_dark else "#fff"}; 
        color: {st.session_state.theme_color}; 
        border: 1px solid {st.session_state.theme_color}44;
        font-weight: bold; transition: 0.3s;
    }}
    .stButton>button:hover {{ 
        border-color: {st.session_state.theme_color}; 
        box-shadow: 0 0 20px {st.session_state.theme_color}66; 
    }}
    .status-bar {{ font-family: 'Courier New'; text-align: right; padding: 5px; color: {st.session_state.theme_color}; }}
    .app-card {{ padding: 15px; border-radius: 15px; background: rgba(255,255,255,0.05); border: 1px solid #444; }}
</style>
""", unsafe_allow_html=True)

# --- 4. HỆ THỐNG ĐIỀU HƯỚNG ---

# MÀN HÌNH NGHỈ MẮT (BATTERY 0%)
if st.session_state.page == "RestMode":
    st.markdown("<h1 style='text-align:center; color:orange;'>🔋 HỆ THỐNG ĐANG SẠC...</h1>", unsafe_allow_html=True)
    st.write("---")
    st.warning("Hết thời gian sử dụng an toàn. Boss hãy nghỉ mắt để bảo vệ sức khỏe!")
    if st.button("🔌 SẠC NHANH (10 GIÂY)"):
        with st.spinner("Đang nạp năng lượng Bio..."):
            time.sleep(10)
            st.session_state.start_time = time.time()
            st.session_state.page = "Desktop"
            st.rerun()

# MÀN HÌNH CHÍNH (DESKTOP)
elif st.session_state.page == "Desktop":
    st.markdown(f"<div class='status-bar'>🛡️ OMEGA v24 | 🔋 {battery}% | {datetime.datetime.now().strftime('%H:%M')}</div>", unsafe_allow_html=True)
    st.title("🛡️ TITAN OMEGA OS")
    
    # Ứng dụng chính (Grid 4x2)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🅿️\nPARKING\n(Bãi Xe)"): st.session_state.page = "Parking"; st.rerun()
        if st.button("💎\nFINANCE\n(Tài Chính)"): st.session_state.page = "Finance"; st.rerun()
    with c2:
        if st.button("🌳\nBOTANY\n(Trồng Cây)"): st.session_state.page = "Garden"; st.rerun()
        if st.button("🌐\nBROWSER\n(Trình Duyệt)"): st.session_state.page = "Browser"; st.rerun()
    with c3:
        if st.button("📖\nGUIDE\n(Hướng Dẫn)"): st.session_state.page = "Guide"; st.rerun()
        if st.button("⚙️\nSETTINGS\n(Cài Đặt)"): st.session_state.page = "Settings"; st.rerun()
    with c4:
        if st.button("🛠️\nTOOLS\n(Công Cụ)"): st.session_state.page = "Tools"; st.rerun()
        if st.button("🌙\nLOCK\n(Khóa)"): st.session_state.page = "Lock"; st.rerun()

# APP: TÀI CHÍNH (MỚI)
elif st.session_state.page == "Finance":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("💎 Quản Lý Tài Chính Giả Lập")
    st.metric("Tổng doanh thu bãi xe", "15.400.000 VNĐ", "+12%")
    st.write("Biểu đồ tăng trưởng (Dữ liệu Cloud)")
    st.line_chart([10, 15, 12, 18, 20, 25])

# APP: TRỒNG CÂY (NÂNG CẤP)
elif st.session_state.page == "Garden":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🌳 Eco-Botany Studio")
    st.write(f"Cấp độ làm vườn: **Lv.{st.session_state.xp // 100}**")
    st.progress(st.session_state.xp % 100 / 100)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.camera_input("Chụp ảnh cây hôm nay")
    with col_g2:
        if st.button("💧 Tưới nước"): st.session_state.xp += 15; st.toast("Cây xanh thêm một chút!"); st.rerun()
        if st.button("☀️ Phơi nắng"): st.session_state.xp += 10; st.toast("Quang hợp thành công!"); st.rerun()

# APP: CÀI ĐẶT & TÍNH NĂNG ẨN
elif st.session_state.page == "Settings":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("⚙️ Control Panel")
    
    # Tính năng ẩn kiểu Android
    st.subheader("Thông tin thiết bị")
    if st.button(f"Mã bản dựng: TITAN-OMEGA-2025-RE"):
        st.session_state.dev_clicks += 1
        if st.session_state.dev_clicks >= 7:
            st.success("🎯 BẠN LÀ NHÀ PHÁT TRIỂN SIÊU CẤP!")
        elif st.session_state.dev_clicks > 3:
            st.toast(f"Còn {7 - st.session_state.dev_clicks} bước nữa...")

    if st.session_state.dev_clicks >= 7:
        st.divider()
        st.subheader("🔥 Developer Options (Hidden)")
        st.session_state.theme_color = st.color_picker("Đổi màu Neon hệ thống:", st.session_state.theme_color)
        if st.button("🚀 Overclock CPU (Giao diện nhanh hơn)"): st.toast("Đang ép xung...")
        st.session_state.limit_min = st.number_input("Cài lại thời gian Pin (phút):", 1, 300, st.session_state.limit_min)
        if st.button("Tắt chế độ Dev"): st.session_state.dev_clicks = 0; st.rerun()

    st.divider()
    st.subheader("Cá nhân hóa")
    if st.button("🌓 Đổi Giao diện Sáng/Tối"):
        st.session_state.is_dark = not st.session_state.is_dark
        st.rerun()

# CÁC APP KHÁC (STUB)
elif st.session_state.page == "Parking":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("🅿️ Quản Lý Xe")
    st.info("Tính năng bãi xe đang hoạt động ngầm...")

elif st.session_state.page == "Guide":
    if st.button("🔙 HOME"): st.session_state.page = "Desktop"; st.rerun()
    st.header("📖 Hướng Dẫn Titan Omega")
    st.write("- **Pin:** Sẽ tụt theo thời gian bạn cài trong Settings.")
    st.write("- **Trồng cây:** Chăm sóc cây để lên Level.")
    st.write("- **Ẩn:** Nhấn 7 lần vào 'Mã bản dựng' trong Cài đặt để đổi màu OS.")

elif st.session_state.page == "Lock":
    st.write("# Hệ thống đã khóa")
    if st.button("MỞ KHÓA"): st.session_state.page = "Desktop"; st.rerun()
