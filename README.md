# Steganography
## Giới thiệu: Triển khai Steganography trong các dạng : Text, Image, Audio, Video.

### Tổng quan về thuật toán sử dụng: 
1. LSB (Least Significant Bit)
* Chuyển đổi dữ liệu cần giấu (hidden.txt) thành dạng chuỗi bit.
* Đọc tệp âm thanh .wav và đảm bảo dữ liệu là kiểu int16 hoặc float32.
* Thay thế bit cuối cùng của mỗi mẫu âm thanh bằng bit của thông điệp.
* Lưu tệp âm thanh đã chỉnh sửa.<br>
![Image](https://github.com/user-attachments/assets/5eaea1c6-1b35-45e2-9786-facf90824742)<br>
👉 Ý tưởng: Giấu thông tin bằng cách thay đổi bit thấp nhất của mỗi mẫu âm thanh, giúp thay đổi không đáng kể giá trị sóng âm.

2. Phase Coding
* Chuyển đổi thông điệp thành chuỗi bit.
* Chuyển đổi tệp âm thanh sang miền tần số bằng Fast Fourier Transform (FFT).
* Điều chỉnh pha của các mẫu dựa trên bit của thông điệp (0 → pha 0, 1 → pha π).
* Chuyển đổi lại về miền thời gian và lưu tệp mới.<br>
![Image](https://github.com/user-attachments/assets/09dd44bf-e5ae-4f03-8260-b7e1b126d979)<br>
👉 Ý tưởng: Thay đổi pha của tín hiệu âm thanh để mã hóa thông điệp mà không làm thay đổi cường độ của sóng.

3. Spread Spectrum (Phổ trải)
* Chuyển đổi thông điệp thành chuỗi bit.
* Đọc tệp âm thanh, chuyển đổi về int16 nếu cần.
* Tạo mã trải phổ (spread_code), dùng để XOR với thông điệp nhằm phân tán dữ liệu giấu trên toàn bộ tín hiệu âm thanh.
* Thay thế bit thấp nhất của mỗi mẫu âm thanh bằng bit giấu tin đã XOR.
* Lưu tệp âm thanh đã giấu tin.<br>
![Image](https://github.com/user-attachments/assets/664754d0-7fe1-4578-ad27-ecbc10a7f8c8)<br>
👉 Ý tưởng: Phát tán thông điệp giấu trên phổ tín hiệu rộng hơn, giúp giảm nguy cơ bị phát hiện.




