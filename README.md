![image](https://github.com/user-attachments/assets/fe353887-d271-4e5c-b60a-91149b15c283)



# Trích Xuất Bình Luận Facebook

Đây là một ứng dụng Python cho phép bạn trích xuất bình luận từ một bài đăng trên Facebook và lưu chúng vào tệp CSV. Ứng dụng cũng cung cấp giao diện người dùng để tương tác với công cụ.

## Tính năng

- Lấy bình luận từ một bài đăng trên Facebook dựa trên ID bài đăng
- Hiển thị các bình luận đã lấy trong ứng dụng
- Sao chép các bình luận vào clipboard
- Xuất các bình luận ra tệp CSV
- Tìm kiếm và lọc các bình luận
- Mở liên kết Facebook của bình luận trực tiếp từ ứng dụng
- Tùy chỉnh cài đặt ứng dụng (access token, page ID, limit)

## Yêu cầu

- Python 3.x

## Cài đặt

1. Clone repository hoặc tải mã nguồn.
2. Tạo virtualenv (tùy chọn, nhưng được khuyến khích):
   ```
   python -m venv env
   ```

3. Kích hoạt Virtualenv:

     ```
     env\Scripts\activate
     ```
4. Cài đặt các gói Python cần thiết bằng pip:
```
   pip install -r requirements.txt
```

4. Tạo tệp `config.ini` trong cùng thư mục với tệp `main.py` và thêm cấu hình sau:
   [DEFAULT]
   ACCESS_TOKEN_PROFILE = your_access_token
   PAGE_ID = your_page_id
   LIMIT = 100
Thay thế `your_access_token` bằng access token API Facebook của bạn, `your_page_id` bằng ID của trang Facebook bạn muốn trích xuất bình luận, và `100` bằng giới hạn số lượng bình luận muốn lấy.

## Sử dụng

1. Chạy script `main.py` để khởi động ứng dụng.
2. Nhập ID của bài đăng Facebook bạn muốn trích xuất bình luận vào trường "Post ID".
3. Nhấp vào nút "Get Comments" để lấy bình luận.
4. Các bình luận sẽ được hiển thị trong khung bên phải của ứng dụng.
5. Bạn có thể sử dụng nút "Copy" để sao chép các bình luận vào clipboard, nút "Save to CSV" để xuất các bình luận ra tệp CSV, và nút "Open CSV" để mở tệp CSV đã lưu trước đó.
6. Trường "Search Comment" cho phép bạn lọc các bình luận hiển thị dựa trên từ khóa tìm kiếm.
7. Nút "Setting" cho phép bạn thay đổi cài đặt ứng dụng, như access token, page ID, và limit.

## Đóng góp

Nếu bạn phát hiện bất kỳ vấn đề nào hoặc có đề xuất cải tiến, vui lòng tạo một issue mới hoặc gửi pull request.

Hy vọng bản dịch này hữu ích cho bạn! Nếu bạn cần thêm bất kỳ điều gì, hãy cho tôi biết nhé. 😊


#######################################################################################################

## Facebook Comments Extractor

This is a Python application that allows you to extract comments from a Facebook post and save them to a CSV file. It also provides a user interface for interacting with the tool.

## Features

- Fetch comments from a Facebook post based on the post ID
- Display the fetched comments in the application
- Copy the comments to the clipboard
- Export the comments to a CSV file
- Search and filter the comments
- Open a comment's Facebook link directly from the application
- Customize the application settings (access token, page ID, limit)

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository or download the source code.
2. Create virtualenv (optional, but recommended):
   ```
   python -m venv env
   ```

3. Activate Virtualenv:

     ```
     env\Scripts\activate
     ```
4 Install the required Python packages using pip:
```
   pip install -r requirements.txt
```

4. Create a `config.ini` file in the same directory as the `main.py` file and add the following configuration:
   [DEFAULT]
   ACCESS_TOKEN_PROFILE = your_access_token
   PAGE_ID = your_page_id
   LIMIT = 100
Replace `your_access_token` with your Facebook API access token, `your_page_id` with the ID of the Facebook page you want to extract comments from, and `100` with the desired limit of comments to fetch.

## Usage

1. Run the `main.py` script to start the application.
2. Enter the ID of the Facebook post you want to extract comments from in the "Post ID" field.
3. Click the "Get Comments" button to fetch the comments.
4. The comments will be displayed in the right-hand frame of the application.
5. You can use the "Copy" button to copy the comments to the clipboard, the "Save to CSV" button to export the comments to a CSV file, and the "Open CSV" button to open a previously saved CSV file.
6. The "Search Comment" field allows you to filter the displayed comments based on the search term.
7. The "Setting" button allows you to modify the application settings, such as the access token, page ID, and limit.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to create a new issue or submit a pull request.


   
