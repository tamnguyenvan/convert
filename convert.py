import os
import subprocess
from PIL import Image

def convert_png_to_cmyk_tiff_with_alpha(input_folder='inputs', output_folder='outputs'):
    os.makedirs(output_folder, exist_ok=True)
    temp_folder = os.path.join(output_folder, '_temp')
    os.makedirs(temp_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith('.png'):
            continue

        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, base_name + '.tiff')
        cmyk_path = os.path.join(temp_folder, base_name + '_cmyk.tiff')
        alpha_path = os.path.join(temp_folder, base_name + '_alpha.tiff')

        # 1. Extract alpha channel
        with Image.open(input_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            alpha = img.getchannel('A')
            alpha.save(alpha_path)

        # 2. Convert to CMYK with ImageMagick (without alpha)
        subprocess.run([
            'magick', input_path,
            '-alpha', 'off',
            '-colorspace', 'CMYK',
            '-density', '300',
            cmyk_path
        ], check=True)

        # 3. Combine CMYK and alpha as multi-page TIFF
        subprocess.run([
            'magick', cmyk_path, alpha_path,
            output_path
        ], check=True)

        print(f'✅ Converted: {filename} → {base_name}.tiff (CMYK + alpha)')

    # Optional: Cleanup temp files
    import shutil
    shutil.rmtree(temp_folder)

# Gọi hàm
input_folder = "inputs"
output_folder = "outputs"
convert_png_to_cmyk_tiff_with_alpha(input_folder, output_folder)

