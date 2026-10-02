# ==========================================
# BUỔI 7: QUẢN LÝ ĐẶT PHÒNG KHÁCH SẠN MINI
# ==========================================

# 1. Khai báo dữ liệu ban đầu
danh_sach_phong = [
    {"ma_phong": "P101", "loai_phong": "Don", "gia": 300000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_phong": "P102", "loai_phong": "Doi", "gia": 500000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_phong": "P103", "loai_phong": "VIP", "gia": 900000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_phong": "P104", "loai_phong": "Don", "gia": 300000, "trang_thai": "Trong", "ten_khach": ""}
]

lich_su_doanh_thu = []


# 2. Hàm hỗ trợ nhập số nguyên an toàn sử dụng try-except
def nhap_so_nguyen(loi_nhac):
    while True:
        try:
            val = int(input(loi_nhac))
            if val <= 0:
                print("-> Số lượng/Giá trị phải lớn hơn 0, vui lòng nhập lại.")
                continue
            return val
        except ValueError:
            print("-> Dữ liệu không hợp lệ, vui lòng nhập lại một số nguyên.")


# 3. Các hàm hiển thị & tìm kiếm
def hien_thi_danh_sach_phong():
    print("\n" + "=" * 65)
    print(f"{'Mã phòng': <10}{'Loại phòng': <12}{'Giá/đêm': <15}{'Trạng thái': <12}{'Khách': <15}")
    print("-" * 65)
    for phong in danh_sach_phong:
        print(f" {phong['ma_phong']: <10}{phong['loai_phong']: <12}{phong['gia']:>10,} VND   {phong['trang_thai']: <12}{phong['ten_khach']: <15}")
    print("=" * 65)

def tim_phong_theo_ma(ma_phong):
    for phong in danh_sach_phong:
        if phong["ma_phong"] == ma_phong:
            return phong
    return None

def xem_phong_trong():
    phong_trong = [phong for phong in danh_sach_phong if phong["trang_thai"] == "Trong"]
    if len(phong_trong) == 0:
        print("-> Hiện không còn phòng trống nào.")
        return
    print("\nCÁC PHÒNG ĐANG TRỐNG:")
    for phong in phong_trong:
        print(f" - Mã: {phong['ma_phong']} | Loại: {phong['loai_phong']} | Giá: {phong['gia']:,} VND/đêm")


# 4. Các hàm nghiệp vụ (Thêm/Đặt/Trả phòng)
def them_phong(ma_phong, loai_phong, gia):
    if tim_phong_theo_ma(ma_phong) is not None:
        print(f"-> Mã phòng {ma_phong} đã tồn tại, không thể thêm.")
        return
    danh_sach_phong.append({
        "ma_phong": ma_phong,
        "loai_phong": loai_phong,
        "gia": gia,
        "trang_thai": "Trong",
        "ten_khach": ""
    })
    print(f"-> Đã thêm phòng {ma_phong} thành công.")

def dat_phong(ma_phong, ten_khach):
    phong = tim_phong_theo_ma(ma_phong)
    if phong is None:
        print(f"-> Không tìm thấy phòng {ma_phong}.")
        return
    if phong["trang_thai"] == "Đã đặt":
        print(f"-> Phòng {ma_phong} đã có khách, không thể đặt.")
        return
    phong["trang_thai"] = "Đã đặt"
    phong["ten_khach"] = ten_khach
    print(f"-> Đặt phòng {ma_phong} cho khách {ten_khach} thành công.")

def tra_phong(ma_phong, so_dem):
    phong = tim_phong_theo_ma(ma_phong)
    if phong is None:
        print(f"-> Không tìm thấy phòng {ma_phong}.")
        return
    if phong["trang_thai"] == "Trong":
        print(f"-> Phòng {ma_phong} đang trống, không có khách để trả phòng.")
        return
    
    thanh_tien = phong["gia"] * so_dem
    lich_su_doanh_thu.append({
        "ma_phong": ma_phong,
        "ten_khach": phong["ten_khach"],
        "so_dem": so_dem,
        "thanh_tien": thanh_tien
    })
    print(f"-> Khách {phong['ten_khach']} trả phòng {ma_phong} sau {so_dem} đêm.")
    print(f"-> Tổng tiền phải thanh toán: {thanh_tien:,} VND")
    
    phong["trang_thai"] = "Trong"
    phong["ten_khach"] = ""


# 5. Hàm thống kê doanh thu
def thong_ke_doanh_thu():
    if len(lich_su_doanh_thu) == 0:
        print("-> Chưa có giao dịch trả phòng nào.")
        return
    tong_doanh_thu = 0
    print("\nLỊCH SỬ GIAO DỊCH:")
    for gd in lich_su_doanh_thu:
        print(f" - Phòng {gd['ma_phong']} | Khách: {gd['ten_khach']} | Số đêm: {gd['so_dem']} | Thành tiền: {gd['thanh_tien']:,} VND")
        tong_doanh_thu += gd["thanh_tien"]
    print(f"\n>>> TỔNG DOANH THU: {tong_doanh_thu:,} VND")


# 6. Menu & Điều khiển chương trình
def hien_thi_menu():
    print("\n===== QUẢN LÝ ĐẶT PHÒNG KHÁCH SẠN MINI =====")
    print("1. Hiển thị danh sách tất cả phòng")
    print("2. Xem các phòng đang trống")
    print("3. Thêm phòng mới")
    print("4. Đặt phòng cho khách")
    print("5. Trả phòng / Thanh toán")
    print("6. Thống kê doanh thu")
    print("0. Thoát chương trình")

def chay_chuong_trinh():
    while True:
        hien_thi_menu()
        lua_chon = input("Nhập lựa chọn của bạn: ").strip()
        
        if lua_chon == "1":
            hien_thi_danh_sach_phong()
        elif lua_chon == "2":
            xem_phong_trong()
        elif lua_chon == "3":
            ma_phong = input("Nhập mã phòng mới: ").strip().upper()
            loai_phong = input("Nhập loại phòng (Don/Doi/VIP): ").strip().title()
            gia = nhap_so_nguyen("Nhập giá phòng/đêm: ")
            them_phong(ma_phong, loai_phong, gia)
        elif lua_chon == "4":
            ma_phong = input("Nhập mã phòng cần đặt: ").strip().upper()
            ten_khach = input("Nhập tên khách: ").strip().title()
            dat_phong(ma_phong, ten_khach)
        elif lua_chon == "5":
            ma_phong = input("Nhập mã phòng cần trả: ").strip().upper()
            so_dem = nhap_so_nguyen("Nhập số đêm đã ở: ")
            tra_phong(ma_phong, so_dem)
        elif lua_chon == "6":
            thong_ke_doanh_thu()
        elif lua_chon == "0":
            print("Cảm ơn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("-> Lựa chọn không hợp lệ, vui lòng chọn lại.")

# Chạy chương trình
if __name__ == "__main__":
    chay_chuong_trinh()