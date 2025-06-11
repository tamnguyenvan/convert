import os
from PIL import Image, ImageCms

# --- CẤU HÌNH ---
# Tên các thư mục và file profile
inputs_dir = 'inputs'
outputs_dir = 'outputs'
srgb_profile_path = 'sRGB_v4_ICC_preference.icc'  # Profile nguồn
cmyk_profile_path = 'CoatedFOGRA27.icc'       # Profile đích (hỏi nhà in!)

# --- THIẾT LẬP BAN ĐẦU ---

# 1. Tạo thư mục outputs nếu nó chưa tồn tại
os.makedirs(outputs_dir, exist_ok=True)

# 2. Kiểm tra và tải các profile màu một lần để tăng hiệu suất
try:
    # Tải profile vào bộ nhớ
    srgb_profile = ImageCms.getOpenProfile(srgb_profile_path)
    cmyk_profile = ImageCms.getOpenProfile(cmyk_profile_path)
    # Lấy dữ liệu bytes của profile CMYK để nhúng vào file khi lưu
    cmyk_profile_bytes = cmyk_profile.tobytes()
except FileNotFoundError:
    print("LỖI: Không tìm thấy file ICC profile.")
    print(f"Hãy chắc chắn rằng '{srgb_profile_path}' và '{cmyk_profile_path}' tồn tại.")
    exit() # Thoát chương trình nếu không có profile

# --- VÒNG LẶP XỬ LÝ ẢNH ---

print(f"Bắt đầu quét thư mục '{inputs_dir}'...")

# Lấy danh sách các file trong thư mục inputs
try:
    file_list = os.listdir(inputs_dir)
except FileNotFoundError:
    print(f"LỖI: Thư mục '{inputs_dir}' không tồn tại. Vui lòng tạo và đặt ảnh vào đó.")
    exit()

for filename in file_list:
    # 3. Chỉ xử lý các file có đuôi .png (không phân biệt hoa thường)
    if filename.lower().endswith('.png'):
        input_path = os.path.join(inputs_dir, filename)
        # Tạo tên file output bằng cách thay đuôi .png thành .tiff
        output_filename = os.path.splitext(filename)[0] + '.tiff'
        output_path = os.path.join(outputs_dir, output_filename)

        print(f"-> Đang xử lý file: '{filename}'")

        try:
            # Mở ảnh PNG (có kênh Alpha)
            img = Image.open(input_path)
            
            # Crop bbox
            bbox = img.getbbox()
            img = img.crop(bbox)

            # Đảm bảo ảnh ở chế độ RGBA
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Tách kênh Alpha (độ trong suốt)
            alpha_channel = img.getchannel('A')

            # Chuyển ảnh sang RGB để làm việc với profile
            rgb_img = img.convert('RGB')

            # Thực hiện chuyển đổi màu sắc có quản lý
            img_cmyk = ImageCms.profileToProfile(
                rgb_img,
                inputProfile=srgb_profile, # Dùng profile đã tải
                outputProfile=cmyk_profile, # Dùng profile đã tải
                renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                outputMode='CMYK'
            )

            # Gắn lại kênh Alpha vào ảnh CMYK
            img_cmyk.putalpha(alpha_channel)

            # Lưu file TIFF, nhúng profile màu và giữ độ trong suốt
            img_cmyk.save(
                output_path,
                format='TIFF',
                dpi=(300, 300),
                save_all=True,
                icc_profile=cmyk_profile_bytes # Dùng dữ liệu profile đã chuẩn bị
            )
            print(f"   => Thành công: '{output_filename}'")
            print(list(Image.open(output_path).info.keys()))

        except Exception as e:
            print(f"   *** Lỗi khi xử lý file '{filename}': {e}")
            # Bỏ qua file lỗi và tiếp tục với file tiếp theo
            continue

print("\nHoàn tất quá trình chuyển đổi!")
