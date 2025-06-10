import os
from PIL import Image, ImageCms
import tifffile
import numpy as np

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
            cmyk_array = np.array(img_cmyk) # Shape sẽ là (height, width, 4)
            cmyk_array_transposed = numpy.transpose(cmyk_array, (2, 0, 1)) # Chuyển thành (4, height, width)

            # Ghi file TIFF bằng tifffile
            tifffile.imwrite(
                output_path,
                cmyk_array_transposed,
                photometric='cmyk',
                resolution=(300, 300, 'INCH'), # Đặt DPI rõ ràng
                metadata={'ICCProfile': cmyk_profile_bytes} # Nhúng profile màu
            )
            print(f"   => Thành công: '{output_filename}'")

        except Exception as e:
            print(f"   *** Lỗi khi xử lý file '{filename}': {e}")
            # Bỏ qua file lỗi và tiếp tục với file tiếp theo
            continue

print("\nHoàn tất quá trình chuyển đổi!")
