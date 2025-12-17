import streamlit as st
import time
import datetime
import random

# --- 1. KHỞI TẠO HỆ THỐNG LÕI (KERNEL) ---
if 'page' not in st.session_state: st.session_state.page = "Lock"
if 'is_locked' not in st.session_state: st.session_state.is_locked = True
if 'pin_code' not in st.session_state: st.session_state.pin_code = "1234" # Mã PIN mặc định
if 'os_version' not in st.session_state: st.session_state.os_version = "27.0"
if 'update_available' not in st.session_state: st.session_state.update_available = False
if 'installed_apps' not in st.session_state: 
    st.session_state.installed_apps = ["Parking", "Botany", "Settings", "Store"]

# Giả lập phát hiện bản cập nhật mới (Ví dụ: Boss đang dùng 27.0, bản mới là 28.0)
CURRENT_STABLE_VER = "28.0"
if st.session_state.os_version != CURRENT_STABLE_VER:
    st.session_state.update_available = True

# --- 2. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan Kernel OS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; }}
    .stButton>button {{
        width: 100%; height: 60px; border-radius: 10px;
        background: #111; color: #00f2ff; border: 1px solid #00f2ff33;
    }}
    .status-bar {{ 
        background: rgba(0,0,0,0.5); padding: 5px 15px; 
        border-bottom: 1px solid #333; position: fixed; top: 0; width: 100%; z-index: 999;
    }}
    .update-banner {{
        background: #ff4b4b; color: white; padding: 10px; 
        text-align: center; border-radius: 5px; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. MÀN HÌNH KHÓA (LOCK SCREEN WITH PIN) ---
if st.session_state.page == "Lock":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>🔒 TITAN SECURE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pin_input = st.text_input("NHẬP MÃ PIN BẢO MẬT", type="password")
        if st.button("XÁC NHẬN MỞ KHÓA"):
            if pin_input == st.session_state.pin_code:
                st.session_state.page = "Desktop"
                st.rerun()
            else:
                st.error("Mã PIN không chính xác!")
        st.caption("Gợi ý: Mã mặc định là 1234")

# --- 4. MÀN HÌNH CHÍNH (DESKTOP) ---
elif st.session_state.page == "Desktop":
    # Thanh trạng thái (Status Bar)
    mem_used = random.randint(60, 85)
    st.markdown(f"""
        <div class='status-bar'>
            <span>🔋 92% | 💾 RAM: {mem_used}% | 🛡️ Version: {st.session_state.os_version}</span>
        </div>
    """, unsafe_allow_html=True)
    st.write("###") # Khoảng trống cho Status Bar
    
    # THÔNG BÁO CẬP NHẬT KHẨN CẤP
    if st.session_state.update_available:
        st.markdown(f"""
            <div class='update-banner'>
                ⚠️ PHÁT HIỆN BẢN CẬP NHẬT BẢO MẬT {CURRENT_STABLE_VER}! 
                Hệ thống yêu cầu nâng cấp ngay để tránh mất dữ liệu.
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔥 NÂNG CẤP VÀ KHỞI ĐỘNG LẠI"):
            with st.status("Đang tải bản vá bảo mật...", expanded=True) as s:
                time.sleep(2)
                s.update(label="Đang giải nén Kernel...", state="running")
                time.sleep(2)
                s.update(label="Đang cài đặt... 85%", state="running")
                time.sleep(1.5)
                st.session_state.os_version = CURRENT_STABLE_VER
                st.session_state.update_available = False
                st.session_state.page = "Reboot"
                st.rerun()

    st.title("🛡️ TITAN KERNEL")
    
    # App Drawer
    cols = st.columns(4)
    for idx, app in enumerate(st.session_state.installed_apps):
        with cols[idx % 4]:
            if st.button(f"📦 {app}"):
                st.session_state.page = app
                st.rerun()
    
    st.divider()
    if st.button("⚙️ HỆ THỐNG"):
        st.session_state.page = "Settings"
        st.rerun()

# --- 5. MÀN HÌNH KHỞI ĐỘNG LẠI (REBOOT) ---
elif st.session_state.page == "Reboot":
    st.markdown("<h2 style='text-align:center; margin-top:150px;'>🌀 ĐANG KHỞI ĐỘNG LẠI...</h2>", unsafe_allow_html=True)
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        progress.progress(i + 1)
    st.session_state.page = "Lock"
    st.rerun()

# --- 6. CÀI ĐẶT BẢO MẬT (SETTINGS) ---
elif st.session_state.page == "Settings":
    st.button("🔙 QUAY LẠI", on_click=lambda: setattr(st.session_state, 'page', 'Desktop'))
    st.header("⚙️ Cài đặt & Bảo mật")
    
    with st.expander("🔐 Thay đổi mã PIN"):
        new_pin = st.text_input("Mã PIN mới", type="password")
        if st.button("LƯU MÃ PIN"):
            st.session_state.pin_code = new_pin
            st.success("Đã cập nhật mã PIN thành công!")
            
    with st.expander("📊 Thông tin bộ nhớ"):
        st.write(f"Bộ nhớ hệ thống: 128GB")
        st.write(f"Đã dùng: {random.randint(20, 30)}GB")
        st.progress(25)
        st.caption("Dữ liệu bãi xe chiếm 0.5% dung lượng.")

# --- CÁC APP KHÁC ---
else:
    st.header(f"🖥️ Ứng dụng: {st.session_state.page}")
    if st.button("🔙 THOÁT"):
        st.session_state.page = "Desktop"
        st.rerun()
