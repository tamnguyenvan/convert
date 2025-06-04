from PIL import Image
import os

input_folder = 'inputs'
output_folder = 'outputs'

# Tạo thư mục output nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + '.tiff'
        output_path = os.path.join(output_folder, output_filename)

        with Image.open(input_path) as img:
            # Thiết lập dpi khi lưu ảnh TIFF
            img.save(output_path, format='TIFF', dpi=(300, 300))

        print(f'Converted {filename} to {output_filename} with 300 dpi')

