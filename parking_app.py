import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. KHỞI TẠO HỆ THỐNG AN TOÀN ---
if 'os' not in st.session_state:
    st.session_state.os = {
        "page": "Desktop",
        "theme": "#00f2ff",
        "savings": 0.0,
        "wallet": 0.0,
        "auto_save": False
    }

if 'parking_data' not in st.session_state:
    st.session_state.parking_data = pd.DataFrame({
        "ID": range(1, 11),
        "Vị trí": [f"Khu A-{i+1}" for i in range(10)],
        "Trạng thái": ["Trống"] * 10,
        "Biển số": [""] * 10,
        "Giờ vào": [None] * 10
    })

if 'finance_data' not in st.session_state:
    # Cấu trúc y hệt bản cũ của Boss để đảm bảo tính năng
    st.session_state.finance_data = pd.DataFrame(columns=["Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú"])

def nav(p):
    st.session_state.os["page"] = p
    st.rerun()

# --- 2. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan Ultimate V37", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .status-bar {{ 
        padding: 8px 20px; background: #161b22; border-bottom: 2px solid {st.session_state.os['theme']};
        display: flex; justify-content: space-between; font-family: 'Courier New', monospace;
    }}
    .app-card {{
        background: #21262d; padding: 25px; border-radius: 15px; text-align: center;
        border: 1px solid #30363d; transition: 0.3s;
    }}
    .app-card:hover {{ border-color: {st.session_state.os['theme']}; transform: scale(1.02); }}
</style>
""", unsafe_allow_html=True)

# --- 3. THANH TRẠNG THÁI ---
st.markdown(f"""<div class='status-bar'>
    <span>🛰️ TITAN OS V37 (STABLE)</span>
    <span>💰 Ví: {st.session_state.os['wallet']:,.0f}đ | 💎 Tiết kiệm: {st.session_state.os['savings']:,.0f}đ</span>
</div>""", unsafe_allow_html=True)
st.write("###")

# --- 4. NAVIGATION LOGIC ---

# 4.1 DESKTOP
if st.session_state.os["page"] == "Desktop":
    st.title("🛡️ Titan Ultimate Dash")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        if st.button("🅿️ QUẢN LÝ XE", use_container_width=True): nav("Parking")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        if st.button("💰 QUẢN LÝ TIỀN", use_container_width=True): nav("Finance")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        if st.button("⚙️ CÀI ĐẶT", use_container_width=True): nav("Settings")

    st.divider()
    # Biểu đồ dòng tiền (Dùng thư viện gốc Streamlit để tránh lỗi Module)
    if not st.session_state.finance_data.empty:
        st.subheader("📊 Xu hướng Tài chính")
        chart_data = st.session_state.finance_data.copy()
        chart_data['Số tiền'] = chart_data['Số tiền'].astype(float)
        st.line_chart(chart_data, x="Ngày", y="Số tiền", color="Loại")

# 4.2 QUẢN LÝ XE (PARKING)
elif st.session_state.os["page"] == "Parking":
    st.button("🔙 VỀ MENU", on_click=lambda: nav("Desktop"))
    st.header("🅿️ Trạm Kiểm Soát")
    
    cols = st.columns(5)
    for idx, row in st.session_state.parking_data.iterrows():
        with cols[idx % 5]:
            is_busy = row["Trạng thái"] == "Đã đỗ"
            btn_label = f"{row['Vị trí']}\n({row['Biển số'] if is_busy else 'TRỐNG'})"
            if st.button(btn_label, key=f"p_{idx}", type="primary" if is_busy else "secondary"):
                st.session_state.selected_slot = idx
                nav("SlotDetail")

# 4.3 CHI TIẾT XE & THANH TOÁN LIÊN KẾT
elif st.session_state.os["page"] == "SlotDetail":
    idx = st.session_state.selected_slot
    slot = st.session_state.parking_data.iloc[idx]
    st.header(f"📍 Vị trí {slot['Vị trí']}")

    if slot["Trạng thái"] == "Trống":
        bs = st.text_input("Nhập biển số xe:")
        if st.button("XÁC NHẬN VÀO"):
            st.session_state.parking_data.at[idx, "Trạng thái"] = "Đã đỗ"
            st.session_state.parking_data.at[idx, "Biển số"] = bs.upper()
            st.session_state.parking_data.at[idx, "Giờ vào"] = datetime.now()
            nav("Parking")
    else:
        st.warning(f"Xe {slot['Biển số']} đang đỗ")
        fee = 30000 # Mặc định 30k
        st.subheader(f"Phí thanh toán: {fee:,.0f} VNĐ")
        
        target = st.radio("Cộng tiền vào đâu?", ["Ví chính", "Quỹ Tiết kiệm"])
        
        if st.button("XÁC NHẬN THANH TOÁN"):
            # Cập nhật tiền
            if target == "Ví chính": st.session_state.os["wallet"] += fee
            else: st.session_state.os["savings"] += fee
            
            # Ghi vào lịch sử Finance (Giữ nguyên logic Boss yêu cầu)
            new_entry = pd.DataFrame([{"Ngày": datetime.now().strftime("%Y-%m-%d"), "Loại": "Thu", "Danh mục": "Lương", "Số tiền": fee, "Ghi chú": f"Tiền xe {slot['Biển số']}"}])
            st.session_state.finance_data = pd.concat([st.session_state.finance_data, new_entry], ignore_index=True)
            
            # Giải phóng chỗ
            st.session_state.parking_data.at[idx, "Trạng thái"] = "Trống"
            st.session_state.parking_data.at[idx, "Biển số"] = ""
            st.balloons()
            nav("Parking")
    
    st.button("HỦY BỎ", on_click=lambda: nav("Parking"))

# 4.4 QUẢN LÝ TIỀN (FINANCE MODULE - NÂNG CẤP)
elif st.session_state.os["page"] == "Finance":
    st.button("🔙 VỀ MENU", on_click=lambda: nav("Desktop"))
    st.title("💰 Quantum Finance V15")
    
    t1, t2, t3 = st.tabs(["📲 NHẬP LIỆU", "📊 THỐNG KÊ", "📋 LỊCH SỬ"])
    
    with t1:
        with st.form("input_form", clear_on_submit=True):
            f_type = st.selectbox("Loại", ["Chi", "Thu"])
            f_amt = st.number_input("Số tiền", min_value=0, step=5000)
            f_cat = st.selectbox("Danh mục", ["Ăn uống", "Di chuyển", "Lương", "Mua sắm", "Khác"])
            f_note = st.text_input("Ghi chú")
            if st.form_submit_button("LƯU VÀO HỆ THỐNG"):
                new_f = pd.DataFrame([{"Ngày": datetime.now().strftime("%Y-%m-%d"), "Loại": f_type, "Danh mục": f_cat, "Số tiền": f_amt, "Ghi chú": f_note}])
                st.session_state.finance_data = pd.concat([st.session_state.finance_data, new_f], ignore_index=True)
                if f_type == "Thu": st.session_state.os["wallet"] += f_amt
                else: st.session_state.os["wallet"] -= f_amt
                st.success("Đã ghi nhận giao dịch!")

    with t2:
        df = st.session_state.finance_data
        if not df.empty:
            st.metric("TỔNG SỐ DƯ (VÍ + TIẾT KIỆM)", f"{st.session_state.os['wallet'] + st.session_state.os['savings']:,.0f} VNĐ")
            st.write("Cơ cấu danh mục (Bảng):")
            st.table(df.groupby('Danh mục')['Số tiền'].sum())
            st.bar_chart(df, x="Danh mục", y="Số tiền")
        else: st.info("Chưa có dữ liệu.")

    with t3:
        st.dataframe(st.session_state.finance_data, use_container_width=True)
        if st.button("Xóa lịch sử"):
            st.session_state.finance_data = pd.DataFrame(columns=["Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú"])
            st.rerun()

# 4.5 SETTINGS
elif st.session_state.os["page"] == "Settings":
    st.button("🔙 VỀ MENU", on_click=lambda: nav("Desktop"))
    st.header("⚙️ Cấu hình hệ thống")
    st.session_state.os["theme"] = st.color_picker("Màu chủ đạo", st.session_state.os["theme"])
    if st.button("KHỞI ĐỘNG LẠI OS (RESET)"):
        st.session_state.clear()
        st.rerun()
