# Hướng dẫn sử dụng

## Mô tả
Script này giúp bạn chuyển đổi tất cả các file ảnh PNG trong thư mục `inputs` sang định dạng TIFF, đồng thời thiết lập độ phân giải (dpi) theo x = 300, y = 300.

## Yêu cầu
- Windows
- Đã có file thực thi `convert.exe` (được đóng gói bằng PyInstaller)
- Thư mục `inputs` chứa các file PNG cần chuyển đổi

## Cách sử dụng

1. Chuẩn bị thư mục `inputs`  
   Đặt tất cả file PNG bạn muốn chuyển đổi vào thư mục `inputs` nằm cùng cấp với file `convert.exe`.

2. Double click


3. Kết quả  
Sau khi chạy xong, các file TIFF sẽ được lưu trong thư mục `outputs` cùng cấp với `convert.exe`.

## Lưu ý
- Nếu thư mục `outputs` chưa tồn tại, chương trình sẽ tự động tạo.
- Độ phân giải ảnh đầu ra luôn là 300 dpi cho cả chiều ngang và chiều dọc.
- Đảm bảo các file trong thư mục `inputs` có định dạng `.png`.



