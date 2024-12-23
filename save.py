import socket
import os

# กำหนดพอร์ตโดยใช้เลข 3 ตัวสุดท้ายจากรหัสประจำตัวบวก 5000
PORT = 5000 + 65

# สร้างเซิร์ฟเวอร์ซ็อกเก็ต
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(1)
print(f'Server listening on port {PORT}...')

while True:
    # รอรับการเชื่อมต่อจากไคลแอนท์
    client_connection, client_address = server_socket.accept()
    print(f'Connection from {client_address}')

    # อ่าน HTTP request จากไคลแอนท์
    request = client_connection.recv(1024).decode('utf-8')
    print(f'Request: {request}')

    # ตรวจสอบว่าคำขอเป็น GET /mypage.htm
    if "GET /mypage.htm" in request:
        # เตรียม HTTP/1.0 response สำหรับหน้า mypage.htm โดยการอ่านจากไฟล์
        try:
            if os.path.exists('mypage.htm'):
                with open('mypage.htm', 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                response = (
                    "HTTP/1.0 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    "Connection: close\r\n\r\n" +
                    html_content
                )
                client_connection.sendall(response.encode('utf-8'))
            else:
                response = "HTTP/1.0 404 Not Found\r\n\r\nmypage.htm not found"
                client_connection.sendall(response.encode('utf-8'))
        except Exception as e:
            response = f"HTTP/1.0 500 Internal Server Error\r\n\r\n{str(e)}"
            client_connection.sendall(response.encode('utf-8'))

    elif "GET /myimage/image.gif" in request:  # ตรวจสอบคำขอสำหรับภาพ
        # เตรียม HTTP/1.0 response สำหรับไฟล์รูปภาพ image.gif
        try:
            file_path = "myimage/image.gif"
            if os.path.exists(file_path):
                with open(file_path, "rb") as image_file:
                    image_data = image_file.read()
                response = (
                    "HTTP/1.0 200 OK\r\n"
                    "Content-Type: image/gif\r\n"
                    f"Content-Length: {len(image_data)}\r\n"
                    "Connection: close\r\n\r\n"
                ).encode('utf-8') + image_data
                client_connection.sendall(response)
            else:
                # กรณีไม่พบไฟล์รูปภาพ
                response = "HTTP/1.0 404 Not Found\r\n\r\nFile not found"
                client_connection.sendall(response.encode('utf-8'))
        except Exception as e:
            response = f"HTTP/1.0 500 Internal Server Error\r\n\r\n{str(e)}"
            client_connection.sendall(response.encode('utf-8'))
    else:
        # กรณีร้องขอหน้าอื่นๆ ที่ไม่มีในระบบ
        response = "HTTP/1.0 404 Not Found\r\n\r\nPage not found"
        client_connection.sendall(response.encode('utf-8'))
    
    # ปิดการเชื่อมต่อ
    client_connection.close()
    print("Connection close...")