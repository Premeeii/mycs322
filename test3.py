import socket

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
        # เตรียม HTTP/1.0 response สำหรับหน้า mypage.htm
        response = (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Connection: close\r\n\r\n"
            "<html><body>"
            "<h1>Kittapas Chocktanatorn 6509540065</h1>"
            "<h1>CS322</h1>"
            "<p>นี่คือหน้าสำหรับแนะนำตัวนักศึกษา</p>"
            "<p>ชื่อ: กฤตภาส โชคธนธรณ์</p>"
            "<p>รหัสนักศึกษา: 6509540065</p>"
            "<p>สาขา: วิทยาการคอมพิวเตอร์</p>"
            "<img src='myimage/image.gif' alt='Sample Image' width='300' height='500'>"
            "</body></html>"
        )
        client_connection.sendall(response.encode('utf-8'))
    elif "GET /myimage/image.gif" in request:  # เปลี่ยนเป็น image.gif
        # เตรียม HTTP/1.0 response สำหรับไฟล์รูปภาพ image.gif
        try:
            file_path = "myimage/image.gif"
            with open("image.gif", "rb") as image_file:
                image_data = image_file.read()
            response = (
                "HTTP/1.0 200 OK\r\n"
                "Content-Type: image/gif\r\n"  # เปลี่ยน Content-Type เป็น image/gif
                f"Content-Length: {len(image_data)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode('utf-8') + image_data
            client_connection.sendall(response)
        except FileNotFoundError:
            # กรณีไม่พบไฟล์รูปภาพ
            response = "HTTP/1.0 404 Not Found\r\n\r\nFile not found"
            client_connection.sendall(response.encode('utf-8'))
    else:
        # กรณีร้องขอหน้าอื่นๆ ที่ไม่มีในระบบ
        response = "HTTP/1.0 404 Not Found\r\n\r\nPage not found"
        client_connection.sendall(response.encode('utf-8'))
    
    # ปิดการเชื่อมต่อ
    client_connection.close()
    print("Connection close...")

