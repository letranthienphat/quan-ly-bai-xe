import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random

# --- 1. KHỞI TẠO CORE SYSTEM (STATE MANAGEMENT) ---
# Khởi tạo toàn bộ biến môi trường để tránh KeyError
if 'sys' not in st.session_state:
    st.session_state.sys = {
        "page": "LockScreen",       # Trang hiện tại
        "version": "37.5",          # Phiên bản OS
        "theme": "#00f2ff",         # Màu chủ đạo
        "user": "Boss",             # Tên người dùng
        "notifications": [],        # Danh sách thông báo
        "storage_used": 45,         # Giả lập dung lượng ổ cứng (%)
        "cpu_temp": 42              # Giả lập nhiệt độ CPU
    }

if 'wallet' not in st.session_state:
    st.session_state.wallet = {"cash": 5000000.0, "savings": 20000000.0}

# Dữ liệu Bãi xe (Thêm cột VIP)
if 'parking_db' not in st.session_state:
    data = []
    for i in range(20):
        is_vip = True if i < 4 else False # 4 chỗ đầu là VIP
        data.append({
            "id": i,
            "code": f"A-{i+1:02d}",
            "status": "Trống",
            "plate": "",
            "time_in": None,
            "is_vip": is_vip
        })
    st.session_state.parking_db = pd.DataFrame(data)

# Dữ liệu Tài chính
if 'finance_db' not in st.session_state:
    st.session_state.finance_db = pd.DataFrame(columns=["Ngày", "Loại", "Danh mục", "Số tiền", "Ghi chú"])

# Dữ liệu Vườn Hẹ
if 'garden_db' not in st.session_state:
    st.session_state.garden_db = {"water_level": 80, "growth": 35, "last_water": str(datetime.now())}

# --- 2. HÀM HỆ THỐNG (HELPER FUNCTIONS) ---
def navigate(target_page):
    st.session_state.sys["page"] = target_page
    st.rerun()

def notify(message, type="info"):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.sys["notifications"].insert(0, f"[{timestamp}] {message}")
    if len(st.session_state.sys["notifications"]) > 10:
        st.session_state.sys["notifications"].pop() # Giữ lại 10 thông báo mới nhất

# --- 3. CẤU HÌNH GIAO DIỆN (UI/UX) ---
st.set_page_config(page_title="Titan OS V37.5", layout="wide", page_icon="🛡️")

# CSS Cyberpunk & Glassmorphism
st.markdown(f"""
<style>
    .stApp {{ background-color: #0e1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }}
    /* Status Bar */
    .status-bar {{
        background: rgba(22, 27, 34, 0.9); border-bottom: 2px solid {st.session_state.sys['theme']};
        padding: 8px 20px; position: sticky; top: 0; z-index: 999;
        display: flex; justify-content: space-between; align-items: center;
        backdrop-filter: blur(10px);
    }}
    /* Card Style */
    .card {{
        background: #21262d; border: 1px solid #30363d; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; transition: all 0.2s;
    }}
    .card:hover {{ border-color: {st.session_state.sys['theme']}; transform: translateY(-2px); }}
    /* Buttons */
    .stButton>button {{ width: 100%; border-radius: 8px; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 4. THANH TRẠNG THÁI (STATUS BAR) ---
# Luôn hiển thị ở mọi trang trừ LockScreen
if st.session_state.sys["page"] != "LockScreen":
    noti_count = len(st.session_state.sys["notifications"])
    noti_icon = "🔔" if noti_count == 0 else f"📩({noti_count})"
    
    st.markdown(f"""
    <div class='status-bar'>
        <div><b>TITAN OS</b> v{st.session_state.sys['version']}</div>
        <div>
            <span>💵 {st.session_state.wallet['cash']:,.0f}đ</span> | 
            <span>💎 {st.session_state.wallet['savings']:,.0f}đ</span>
        </div>
        <div>{noti_icon} | 🔋 100% | {datetime.now().strftime('%H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Spacer

# --- 5. LOGIC ĐIỀU HƯỚNG & ỨNG DỤNG ---

# === MÀN HÌNH KHÓA ===
if st.session_state.sys["page"] == "LockScreen":
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("<br><br><h1 style='text-align:center'>🔒 TITAN SECURITY</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center'>Vui lòng nhập mật khẩu để truy cập hệ thống quản lý</p>", unsafe_allow_html=True)
        pin = st.text_input("Mật khẩu truy cập", type="password", placeholder="Gợi ý: 1234")
        if st.button("MỞ KHÓA HỆ THỐNG", type="primary"):
            if pin == "1234":
                notify("Đăng nhập thành công!")
                navigate("Desktop")
            else:
                st.error("Mật khẩu sai! Cảnh báo xâm nhập.")

# === MÀN HÌNH CHÍNH (DESKTOP) ===
elif st.session_state.sys["page"] == "Desktop":
    st.title(f"👋 Xin chào, {st.session_state.sys['user']}!")
    
    # Khu vực Widget
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><b>🅿️ Bãi Xe</b><br>Trống: {len(st.session_state.parking_db[st.session_state.parking_db['status']=='Trống'])}/20</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><b>💰 Tổng Tài Sản</b><br>{(st.session_state.wallet['cash'] + st.session_state.wallet['savings']):,.0f} VNĐ</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><b>🌱 Vườn Hẹ</b><br>Độ ẩm: {st.session_state.garden_db['water_level']}%</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><b>💻 CPU Temp</b><br>{st.session_state.sys['cpu_temp']}°C</div>", unsafe_allow_html=True)

    st.divider()
    
    # App Grid (Lưới ứng dụng)
    col_app1, col_app2, col_app3, col_app4 = st.columns(4)
    with col_app1:
        if st.button("🅿️ QUẢN LÝ XE", use_container_width=True): navigate("Parking")
    with col_app2:
        if st.button("💵 TÀI CHÍNH", use_container_width=True): navigate("Finance")
    with col_app3:
        if st.button("🌱 TRỒNG TRỌT", use_container_width=True): navigate("Garden")
    with col_app4:
        if st.button("⚙️ HỆ THỐNG", use_container_width=True): navigate("Settings")

    # Trung tâm thông báo
    with st.expander("📩 Trung tâm thông báo & Nhật ký hệ thống", expanded=False):
        if not st.session_state.sys["notifications"]:
            st.info("Không có thông báo mới.")
        else:
            for msg in st.session_state.sys["notifications"]:
                st.text(msg)
            if st.button("Xóa tất cả thông báo"):
                st.session_state.sys["notifications"] = []
                st.rerun()

# === ỨNG DỤNG: QUẢN LÝ XE (PARKING PRO) ===
elif st.session_state.sys["page"] == "Parking":
    c_head1, c_head2 = st.columns([3,1])
    with c_head1: st.header("🅿️ Quản lý Bãi Xe Cao Cấp")
    with c_head2: 
        if st.button("🔙 Về Desktop"): navigate("Desktop")
    
    # Filter
    filter_status = st.radio("Hiển thị:", ["Tất cả", "Trống", "Đang đỗ", "Khu vực VIP"], horizontal=True)

    # Hiển thị Grid
    cols = st.columns(5)
    for index, row in st.session_state.parking_db.iterrows():
        # Logic lọc
        if filter_status == "Trống" and row['status'] != "Trống": continue
        if filter_status == "Đang đỗ" and row['status'] != "Đã đỗ": continue
        if filter_status == "Khu vực VIP" and not row['is_vip']: continue

        with cols[index % 5]:
            # Style cho từng ô
            bg_color = "#1f6feb" if row['status'] == "Trống" else "#d73a49"
            if row['status'] == "Trống" and row['is_vip']: bg_color = "#b8860b" # Vàng gold cho VIP
            
            st.markdown(f"""
            <div style='background:{bg_color}; padding:10px; border-radius:8px; text-align:center; color:white; margin-bottom:5px'>
                <small>{'⭐ VIP' if row['is_vip'] else 'Khu A'}</small><br>
                <b>{row['code']}</b><br>
                <span style='font-size:12px'>{row['plate'] if row['plate'] else '---'}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Nút hành động
            if st.button("Xử lý", key=f"p_btn_{index}"):
                st.session_state.current_slot_index = index
                navigate("ParkingDetail")

# === ỨNG DỤNG: CHI TIẾT ĐỖ XE ===
elif st.session_state.sys["page"] == "ParkingDetail":
    idx = st.session_state.current_slot_index
    slot = st.session_state.parking_db.iloc[idx]
    
    st.button("🔙 Quay lại Bãi xe", on_click=lambda: navigate("Parking")) # Lambda ở đây OK vì navigate gọi rerun ở cuối
    
    st.subheader(f"📍 Đang xử lý vị trí: {slot['code']} ({'⭐ VIP' if slot['is_vip'] else 'Thường'})")
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        st.markdown("### 📥 Nhận xe vào")
        if slot['status'] == "Trống":
            plate_in = st.text_input("Nhập biển số xe:")
            if st.button("Xác nhận Check-in", type="primary"):
                if plate_in:
                    st.session_state.parking_db.at[idx, 'status'] = "Đã đỗ"
                    st.session_state.parking_db.at[idx, 'plate'] = plate_in.upper()
                    st.session_state.parking_db.at[idx, 'time_in'] = datetime.now()
                    notify(f"Xe {plate_in} đã vào vị trí {slot['code']}")
                    st.success("Đã nhận xe!")
                    time.sleep(0.5)
                    navigate("Parking")
                else:
                    st.warning("Vui lòng nhập biển số!")
        else:
            st.info("Vị trí này đang có xe đỗ.")

    with col_act2:
        st.markdown("### 📤 Trả xe & Thu tiền")
        if slot['status'] == "Đã đỗ":
            st.write(f"Biển số: **{slot['plate']}**")
            st.write(f"Giờ vào: {slot['time_in'].strftime('%H:%M:%S')}")
            
            # Tính tiền (VIP đắt gấp đôi)
            base_price = 50000 if slot['is_vip'] else 20000
            st.metric("Tổng tiền phí", f"{base_price:,} VNĐ")
            
            pay_method = st.radio("Cộng tiền vào đâu?", ["Ví Tiền Mặt", "Quỹ Tiết Kiệm"])
            
            if st.button("Thanh toán & Mở cổng"):
                # 1. Cộng tiền
                if pay_method == "Ví Tiền Mặt":
                    st.session_state.wallet['cash'] += base_price
                else:
                    st.session_state.wallet['savings'] += base_price
                
                # 2. Ghi nhật ký tài chính
                new_rec = pd.DataFrame([{
                    "Ngày": datetime.now().strftime("%Y-%m-%d"),
                    "Loại": "Thu",
                    "Danh mục": "Doanh thu Bãi xe",
                    "Số tiền": base_price,
                    "Ghi chú": f"Xe {slot['plate']} ra khỏi {slot['code']}"
                }])
                st.session_state.finance_db = pd.concat([st.session_state.finance_db, new_rec], ignore_index=True)
                
                # 3. Reset slot
                st.session_state.parking_db.at[idx, 'status'] = "Trống"
                st.session_state.parking_db.at[idx, 'plate'] = ""
                st.session_state.parking_db.at[idx, 'time_in'] = None
                
                notify(f"Thu {base_price:,}đ từ xe {slot['plate']}")
                st.balloons()
                navigate("Parking")
        else:
            st.info("Chưa có xe để thanh toán.")

# === ỨNG DỤNG: TÀI CHÍNH (FINANCE INTEGRATED) ===
elif st.session_state.sys["page"] == "Finance":
    st.button("🔙 Về Desktop", on_click=lambda: navigate("Desktop"))
    st.title("💵 Quản lý Tài Chính V37.5")
    
    # Dashboard nhỏ
    m1, m2, m3 = st.columns(3)
    m1.metric("Tiền mặt đang có", f"{st.session_state.wallet['cash']:,.0f} đ")
    m2.metric("Quỹ Tiết kiệm", f"{st.session_state.wallet['savings']:,.0f} đ", delta="Mục tiêu mua xe")
    m3.metric("Tổng giao dịch", len(st.session_state.finance_db))

    tab1, tab2 = st.tabs(["Ghi chép Giao dịch", "Lịch sử & Báo cáo"])
    
    with tab1:
        with st.form("fin_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                f_type = st.selectbox("Loại giao dịch", ["Chi", "Thu"])
                f_amount = st.number_input("Số tiền (VNĐ)", min_value=1000, step=10000)
            with col_f2:
                f_cat = st.selectbox("Danh mục", ["Ăn uống", "Mua sắm", "Điện nước", "Lương", "Bảo trì bãi xe", "Khác"])
                f_note = st.text_input("Ghi chú chi tiết")
            
            if st.form_submit_button("Lưu giao dịch"):
                # Cập nhật ví
                if f_type == "Thu":
                    st.session_state.wallet['cash'] += f_amount
                else:
                    st.session_state.wallet['cash'] -= f_amount
                
                # Lưu vào DB
                new_rec = pd.DataFrame([{
                    "Ngày": datetime.now().strftime("%Y-%m-%d"),
                    "Loại": f_type,
                    "Danh mục": f_cat,
                    "Số tiền": f_amount,
                    "Ghi chú": f_note
                }])
                st.session_state.finance_db = pd.concat([st.session_state.finance_db, new_rec], ignore_index=True)
                notify(f"Đã ghi nhận {f_type}: {f_amount:,}đ")
                st.rerun()

    with tab2:
        if not st.session_state.finance_db.empty:
            st.dataframe(st.session_state.finance_db, use_container_width=True)
            # Biểu đồ đơn giản (Không dùng Plotly để tránh lỗi)
            st.bar_chart(st.session_state.finance_db, x="Danh mục", y="Số tiền")
            
            if st.button("Xuất báo cáo ra CSV"):
                csv = st.session_state.finance_db.to_csv(index=False).encode('utf-8')
                st.download_button("Tải xuống ngay", csv, "baocao_taichinh.csv", "text/csv")

# === ỨNG DỤNG: VƯỜN HẸ (GARDEN) ===
elif st.session_state.sys["page"] == "Garden":
    st.button("🔙 Về Desktop", on_click=lambda: navigate("Desktop"))
    st.header("🌱 Vườn Hẹ Thông Minh")
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Allium_tuberosum_flowers.jpg/640px-Allium_tuberosum_flowers.jpg", caption="Hẹ đang lớn")
    with col_g2:
        water = st.session_state.garden_db['water_level']
        growth = st.session_state.garden_db['growth']
        
        st.write("💧 **Độ ẩm đất:**")
        st.progress(water / 100)
        
        st.write("🌿 **Tiến độ thu hoạch:**")
        st.progress(growth / 100)
        
        st.info(f"Tưới lần cuối: {st.session_state.garden_db['last_water']}")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("💦 Tưới nước"):
                st.session_state.garden_db['water_level'] = 100
                st.session_state.garden_db['last_water'] = str(datetime.now())
                st.toast("Cây đã được tưới mát!")
                st.rerun()
        with btn_col2:
            if st.button("✂️ Thu hoạch & Bán"):
                if growth >= 100:
                    earnings = 500000
                    st.session_state.wallet['cash'] += earnings
                    st.session_state.garden_db['growth'] = 0
                    notify(f"Thu hoạch hẹ thành công! Lãi: {earnings:,}đ")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Cây chưa đủ lớn để thu hoạch!")

# === ỨNG DỤNG: CÀI ĐẶT HỆ THỐNG (SETTINGS) ===
elif st.session_state.sys["page"] == "Settings":
    st.button("🔙 Về Desktop", on_click=lambda: navigate("Desktop"))
    st.header("⚙️ Control Panel")
    
    s1, s2 = st.tabs(["Hệ thống", "Dữ liệu"])
    
    with s1:
        st.subheader("Trạng thái phần cứng giả lập")
        st.write("Ổ cứng (Disk Usage):")
        st.progress(st.session_state.sys["storage_used"] / 100)
        st.caption(f"Đã dùng {st.session_state.sys['storage_used']}% của 1TB")
        
        st.session_state.sys["theme"] = st.color_picker("Đổi màu giao diện", st.session_state.sys["theme"])
        if st.button("Kiểm tra cập nhật OS"):
            with st.spinner("Đang kết nối máy chủ Titan..."):
                time.sleep(2)
            st.success("Hệ thống đang ở phiên bản mới nhất (V37.5)")

    with s2:
        st.warning("Khu vực nguy hiểm")
        if st.button("Format System (Xóa tất cả dữ liệu)"):
            st.session_state.clear()
            st.rerun()

# Fallback nếu trang không tồn tại
else:
    st.error("Lỗi 404: Trang không tìm thấy")
    if st.button("Về trang chủ"): navigate("Desktop")
