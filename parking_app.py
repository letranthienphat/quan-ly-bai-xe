import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random

# --- 1. KHỞI TẠO HỆ THỐNG LÕI (CORE ENGINE) ---
if 'os' not in st.session_state:
    st.session_state.os = {
        "page": "Desktop",
        "theme_color": "#00f2ff",
        "auto_pay": False,  # Chế độ thanh toán tự động
        "savings": 0.0,      # Quỹ tiết kiệm
        "pin": "1234"
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
    st.session_state.finance_data = pd.DataFrame(columns=["Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú"])

# Hàm chuyển trang an toàn - KHÔNG GÂY MÀN HÌNH ĐEN
def nav_to(page_name):
    st.session_state.os["page"] = page_name
    st.rerun()

# --- 2. GIAO DIỆN HỆ THỐNG ---
st.set_page_config(page_title="Titan Omega V36", layout="wide", page_icon="🛡️")

st.markdown(f"""
<style>
    .stApp {{ background-color: #050505; color: white; }}
    .status-bar {{ 
        padding: 10px 20px; background: #111; border-bottom: 2px solid {st.session_state.os['theme_color']};
        display: flex; justify-content: space-between; font-family: monospace;
    }}
    .metric-box {{
        background: #161b22; padding: 15px; border-radius: 10px; 
        border-left: 5px solid {st.session_state.os['theme_color']};
    }}
    .app-card {{
        background: #21262d; padding: 20px; border-radius: 15px; text-align: center;
        border: 1px solid #30363d; transition: 0.3s; cursor: pointer;
    }}
    .app-card:hover {{ border-color: {st.session_state.os['theme_color']}; transform: translateY(-5px); }}
</style>
""", unsafe_allow_html=True)

# --- 3. THANH TRẠNG THÁI (STATUS BAR) ---
st.markdown(f"""<div class='status-bar'>
    <span>🛡️ TITAN OMEGA OS V36</span>
    <span>💰 Tiết kiệm: {st.session_state.os['savings']:,}đ | {datetime.now().strftime('%H:%M')}</span>
</div>""", unsafe_allow_html=True)
st.write("###")

# --- 4. NAVIGATION LOGIC ---

# 4.1 MÀN HÌNH CHÍNH (DESKTOP)
if st.session_state.os["page"] == "Desktop":
    st.title("🌌 Titan Command Center")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🅿️ QUẢN LÝ XE", use_container_width=True): nav_to("Parking")
    with col2:
        if st.button("💰 QUẢN LÝ TIỀN", use_container_width=True): nav_to("Finance")
    with col3:
        if st.button("⚙️ CÀI ĐẶT", use_container_width=True): nav_to("Settings")

    st.write("---")
    st.subheader("📊 Trạng thái nhanh")
    w1, w2 = st.columns(2)
    with w1:
        st.markdown(f"<div class='metric-box'>Tiết kiệm hiện tại<br><h2>{st.session_state.os['savings']:,.0f} VNĐ</h2></div>", unsafe_allow_html=True)
    with w2:
        busy = len(st.session_state.parking_data[st.session_state.parking_data["Trạng thái"] == "Đã đỗ"])
        st.markdown(f"<div class='metric-box'>Xe trong bãi<br><h2>{busy} / 10</h2></div>", unsafe_allow_html=True)

# 4.2 QUẢN LÝ XE (PARKING)
elif st.session_state.os["page"] == "Parking":
    st.button("🔙 VỀ MENU", on_click=lambda: nav_to("Desktop"))
    st.header("🅿️ Trạm Kiểm Soát Bãi Xe")
    
    cols = st.columns(5)
    for index, row in st.session_state.parking_data.iterrows():
        with cols[index % 5]:
            color = "#f85149" if row["Trạng thái"] == "Đã đỗ" else "#2ea043"
            st.markdown(f"<div style='text-align:center; padding:10px; border:1px solid {color}; border-radius:10px;'>{row['Vị trí']}<br><b>{row['Biển số'] if row['Biển số'] else 'TRỐNG'}</b></div>", unsafe_allow_html=True)
            if st.button("Chi tiết", key=f"p_{index}"):
                st.session_state.selected_slot = index
                nav_to("ParkingDetail")

# 4.3 CHI TIẾT THANH TOÁN (KẾT HỢP TỰ ĐỘNG/THỦ CÔNG)
elif st.session_state.os["page"] == "ParkingDetail":
    idx = st.session_state.selected_slot
    slot = st.session_state.parking_data.iloc[idx]
    
    st.header(f"📍 Xử lý vị trí: {slot['Vị trí']}")
    
    if slot["Trạng thái"] == "Trống":
        bien_so = st.text_input("Nhập biển số xe vào:")
        if st.button("XÁC NHẬN VÀO BÃI"):
            st.session_state.parking_data.at[idx, "Trạng thái"] = "Đã đỗ"
            st.session_state.parking_data.at[idx, "Biển số"] = bien_so.upper()
            st.session_state.parking_data.at[idx, "Giờ vào"] = datetime.now()
            nav_to("Parking")
    else:
        st.warning(f"Xe {slot['Biển số']} đang đỗ.")
        # Tính tiền giả định 20.000đ
        fee = 20000
        st.subheader(f"Phí gửi xe: {fee:,.0f} VNĐ")
        
        mode = "TỰ ĐỘNG" if st.session_state.os["auto_pay"] else "THỦ CÔNG"
        st.info(f"Chế độ thanh toán hiện tại: **{mode}**")

        if st.session_state.os["auto_pay"]:
            if st.button("XÁC NHẬN TRẢ XE (AUTO-PAY)"):
                # Cộng vào tiết kiệm
                st.session_state.os["savings"] += fee
                # Lưu vào lịch sử tài chính
                new_row = {"Ngày": datetime.now().strftime("%Y-%m-%d"), "Loại": "Thu", "Danh mục": "Lương", "Số tiền": fee, "Ghi chú": f"Tiền xe {slot['Biển số']}"}
                st.session_state.finance_data = pd.concat([st.session_state.finance_data, pd.DataFrame([new_row])], ignore_index=True)
                # Reset slot
                st.session_state.parking_data.at[idx, "Trạng thái"] = "Trống"
                st.session_state.parking_data.at[idx, "Biển số"] = ""
                st.success("Đã thanh toán tự động và cộng vào Tiết kiệm!")
                time.sleep(1)
                nav_to("Parking")
        else:
            if st.button("XÁC NHẬN THANH TOÁN THỦ CÔNG"):
                agree = st.checkbox("Tôi đồng ý cộng số tiền này vào quỹ Tiết kiệm")
                if agree:
                    st.session_state.os["savings"] += fee
                    # Lưu vào tài chính
                    new_row = {"Ngày": datetime.now().strftime("%Y-%m-%d"), "Loại": "Thu", "Danh mục": "Lương", "Số tiền": fee, "Ghi chú": f"Tiền xe {slot['Biển số']}"}
                    st.session_state.finance_data = pd.concat([st.session_state.finance_data, pd.DataFrame([new_row])], ignore_index=True)
                    st.session_state.parking_data.at[idx, "Trạng thái"] = "Trống"
                    st.session_state.parking_data.at[idx, "Biển số"] = ""
                    st.balloons()
                    nav_to("Parking")
                else:
                    st.warning("Vui lòng tích đồng ý để hoàn tất.")
    
    if st.button("HỦY BỎ"): nav_to("Parking")

# 4.4 QUẢN LÝ TIỀN (FINANCE - MERGED)
elif st.session_state.os["page"] == "Finance":
    st.button("🔙 VỀ MENU", on_click=lambda: nav_to("Desktop"))
    st.title("💰 Quantum Finance Integrated")
    
    t1, t2, t3 = st.tabs(["📲 NHẬP LIỆU", "📊 THỐNG KÊ", "📋 LỊCH SỬ"])
    
    with t1:
        with st.form("f_form", clear_on_submit=True):
            f_type = st.selectbox("Loại", ["Chi", "Thu"])
            f_amt = st.number_input("Số tiền", min_value=0)
            f_cat = st.selectbox("Danh mục", ["Ăn uống", "Mua sắm", "Lương", "Khác"])
            f_note = st.text_input("Ghi chú")
            if st.form_submit_button("LƯU"):
                new_f = {"Ngày": datetime.now().strftime("%Y-%m-%d"), "Loại": f_type, "Danh mục": f_cat, "Số tiền": f_amt, "Ghi chú": f_note}
                st.session_state.finance_data = pd.concat([st.session_state.finance_data, pd.DataFrame([new_f])], ignore_index=True)
                if f_type == "Thu": st.session_state.os["savings"] += f_amt
                else: st.session_state.os["savings"] -= f_amt
                st.success("Đã ghi sổ!")

    with t2:
        if not st.session_state.finance_data.empty:
            fig = px.pie(st.session_state.finance_data, values='Số tiền', names='Danh mục', title="Cơ cấu tài chính", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("Chưa có dữ liệu.")

    with t3:
        st.dataframe(st.session_state.finance_data, use_container_width=True)

# 4.5 CÀI ĐẶT (SETTINGS)
elif st.session_state.os["page"] == "Settings":
    st.button("🔙 VỀ MENU", on_click=lambda: nav_to("Desktop"))
    st.header("⚙️ Hệ thống Cài đặt")
    st.session_state.os["auto_pay"] = st.toggle("Chế độ thanh toán tự động (Auto-Pay)", st.session_state.os["auto_pay"])
    st.write("Khi bật, tiền xe sẽ tự động cộng vào tiết kiệm mà không cần hỏi lại.")
    if st.button("Xóa sạch dữ liệu (Reset)"):
        st.session_state.clear()
        st.rerun()
