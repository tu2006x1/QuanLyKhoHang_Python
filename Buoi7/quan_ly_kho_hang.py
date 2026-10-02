# ==========================================
# ĐỒ ÁN NHỎ: QUẢN LÝ KHO HÀNG MINI
# ==========================================

# 1. Khai báo dữ liệu ban đầu
danh_sach_hang_hoa = [
    {"ma_sp": "SP01", "ten_sp": "Laptop Dell", "so_luong": 10, "don_gia": 15000000, "danh_muc": "Maytinh"},
    {"ma_sp": "SP02", "ten_sp": "Chuot Khong Day", "so_luong": 50, "don_gia": 250000, "danh_muc": "Phu Kien"},
    {"ma_sp": "SP03", "ten_sp": "Ban Bieu Co", "so_luong": 30, "don_gia": 800000, "danh_muc": "Phu Kien"},
    {"ma_sp": "SP04", "ten_sp": "Man Hinh 27 inch", "so_luong": 5, "don_gia": 4500000, "danh_muc": "Manhinh"}
]

lich_su_xuat_kho = []


# 2. Hàm hỗ trợ nhập số nguyên an toàn sử dụng try-except
def nhap_so_nguyen(loi_nhac):
    while True:
        try:
            val = int(input(loi_nhac))
            if val <= 0:
                print("-> Giá trị phải lớn hơn 0, vui lòng nhập lại.")
                continue
            return val
        except ValueError:
            print("-> Dữ liệu không hợp lệ, vui lòng nhập lại một số nguyên.")


# 3. Các hàm hiển thị & tìm kiếm
def hien_thi_danh_sach_sp():
    print("\n" + "=" * 70)
    print(f"{'Mã SP': <10}{'Tên sản phẩm': <20}{'Danh mục': <15}{'Số lượng': <10}{'Đơn giá (VND)': <15}")
    print("-" * 70)
    for sp in danh_sach_hang_hoa:
        print(f" {sp['ma_sp']: <10}{sp['ten_sp']: <20}{sp['danh_muc']: <15}{sp['so_luong']: <10}{sp['don_gia']:>12,} VND")
    print("=" * 70)

def tim_sp_theo_ma(ma_sp):
    for sp in danh_sach_hang_hoa:
        if sp["ma_sp"] == ma_sp:
            return sp
    return None

def xem_sp_sap_het():
    sp_can_nhap = [sp for sp in danh_sach_hang_hoa if sp["so_luong"] < 10]
    if len(sp_can_nhap) == 0:
        print("-> Kho hàng vẫn đảm bảo số lượng, chưa có sản phẩm nào sắp hết.")
        return
    print("\nCÁC SẢN PHẨM CẦN NHẬP THÊM (Số lượng < 10):")
    for sp in sp_can_nhap:
        print(f" - Mã: {sp['ma_sp']} | Tên: {sp['ten_sp']} | Số lượng còn: {sp['so_luong']}")


# 4. Các hàm nghiệp vụ kho (Thêm SP / Nhập kho / Xuất kho)
def them_sp_moi(ma_sp, ten_sp, danh_muc, so_luong, don_gia):
    if tim_sp_theo_ma(ma_sp) is not None:
        print(f"-> Mã sản phẩm {ma_sp} đã tồn tại trong hệ thống!")
        return
    danh_sach_hang_hoa.append({
        "ma_sp": ma_sp,
        "ten_sp": ten_sp,
        "danh_muc": danh_muc,
        "so_luong": so_luong,
        "don_gia": don_gia
    })
    print(f"-> Đã thêm sản phẩm {ten_sp} ({ma_sp}) vào kho thành công.")

def nhập_them_hang(ma_sp, so_luong_them):
    sp = tim_sp_theo_ma(ma_sp)
    if sp is None:
        print(f"-> Không tìm thấy sản phẩm có mã {ma_sp}.")
        return
    sp["so_luong"] += so_luong_them
    print(f"-> Đã nhập thêm {so_luong_them} sản phẩm {sp['ten_sp']}. Tổng tồn kho hiện tại: {sp['so_luong']}")

def xuat_kho(ma_sp, so_luong_xuat):
    sp = tim_sp_theo_ma(ma_sp)
    if sp is None:
        print(f"-> Không tìm thấy sản phẩm có mã {ma_sp}.")
        return
    if sp["so_luong"] < so_luong_xuat:
        print(f"-> Khong đủ hàng trong kho! Hiện chỉ còn {sp['so_luong']} sản phẩm.")
        return
    
    sp["so_luong"] -= so_luong_xuat
    tong_tien = so_luong_xuat * sp["don_gia"]
    
    lich_su_xuat_kho.append({
        "ma_sp": ma_sp,
        "ten_sp": sp["ten_sp"],
        "so_luong": so_luong_xuat,
        "tong_tien": tong_tien
    })
    
    print(f"-> Xuất kho thành công {so_luong_xuat} {sp['ten_sp']}.")
    print(f"-> Giá trị đơn xuất kho: {tong_tien:,} VND")


# 5. Hàm thống kê giá trị kho
def thong_ke_kho():
    tong_gia_tri = sum(sp["so_luong"] * sp["don_gia"] for sp in danh_sach_hang_hoa)
    tong_san_pham = sum(sp["so_luong"] for sp in danh_sach_hang_hoa)
    
    print("\nTHỐNG KÊ TỔNG QUAN KHO HÀNG:")
    print(f" - Tổng số mặt hàng khác nhau: {len(danh_sach_hang_hoa)}")
    print(f" - Tổng số lượng hàng hóa tồn kho: {tong_san_pham} sản phẩm")
    print(f" - TỔNG GIÁ TRỊ TÀI SẢN TRONG KHO: {tong_gia_tri:,} VND")


# 6. Menu & Điều khiển chương trình
def hien_thi_menu():
    print("\n===== HỆ THỐNG QUẢN LÝ KHO HÀNG =====")
    print("1. Hiển thị danh sách tất cả sản phẩm")
    print("2. Xem các sản phẩm sắp hết hàng (< 10)")
    print("3. Thêm sản phẩm mới vào danh mục")
    print("4. Nhập thêm hàng vào kho")
    print("5. Xuất kho sản phẩm")
    print("6. Thống kê tổng giá trị kho hàng")
    print("0. Thoát chương trình")

def chay_chuong_trinh():
    while True:
        hien_thi_menu()
        lua_chon = input("Nhập lựa chọn của bạn: ").strip()
        
        if lua_chon == "1":
            hien_thi_danh_sach_sp()
        elif lua_chon == "2":
            xem_sp_sap_het()
        elif lua_chon == "3":
            ma_sp = input("Nhập mã SP mới: ").strip().upper()
            ten_sp = input("Nhập tên SP: ").strip().title()
            danh_muc = input("Nhập danh mục: ").strip().title()
            so_luong = nhap_so_nguyen("Nhập số lượng ban đầu: ")
            don_gia = nhap_so_nguyen("Nhập đơn giá (VND): ")
            them_sp_moi(ma_sp, ten_sp, danh_muc, so_luong, don_gia)
        elif lua_chon == "4":
            ma_sp = input("Nhập mã SP cần nhập thêm: ").strip().upper()
            so_luong = nhap_so_nguyen("Nhập số lượng bổ sung: ")
            nhập_them_hang(ma_sp, so_luong)
        elif lua_chon == "5":
            ma_sp = input("Nhập mã SP cần xuất kho: ").strip().upper()
            so_luong = nhap_so_nguyen("Nhập số lượng xuất: ")
            xuat_kho(ma_sp, so_luong)
        elif lua_chon == "6":
            thong_ke_kho()
        elif lua_chon == "0":
            print("Cảm ơn bạn đã sử dụng hệ thống quản lý kho hàng!")
            break
        else:
            print("-> Lựa chọn không hợp lệ, vui lòng chọn lại.")

# Chạy chương trình
if __name__ == "__main__":
    chay_chuong_trinh()