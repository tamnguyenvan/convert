from PIL import Image
import os

input_folder = 'inputs'
output_folder = 'outputs'

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + '.tiff'
        output_path = os.path.join(output_folder, output_filename)

        with Image.open(input_path) as img:
            # Chuyển sang CMYK
            img_cmyk = img.convert('CMYK')
            # Lưu ảnh TIFF với dpi 300
            img_cmyk.save(output_path, format='TIFF', dpi=(300, 300))

        print(f'Converted {filename} to {output_filename} with 300 dpi and CMYK color space')

