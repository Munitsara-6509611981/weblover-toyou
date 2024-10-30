import socket

# กำหนดพอร์ตจากเลขท้ายรหัสนักศึกษา 981+5000
port = 5981

# สร้างเซิร์ฟเวอร์
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1)

print(f"Server started on port {port}. Waiting for connection...")

try:
    while True:
        # รอรับการเชื่อมต่อจากไคลเอนต์
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} received.")

        # รับ HTTP request message
        request = client_socket.recv(1024).decode('utf-8')
        print("HTTP Request Received:")
        print(request)

        # ตรวจสอบการร้องขอไฟล์ mypage.htm หรือ root directory
        if "GET /mypage.htm" in request or "GET / " in request:
            try:
                # อ่านเนื้อหาจากไฟล์ mypage.htm
                with open("mypage.htm", "r", encoding="utf-8") as file:
                    content = file.read()

                # สร้าง HTTP Response message พร้อมเนื้อหาจาก mypage.htm
                response = f"""\
HTTP/1.0 200 OK
Content-Type: text/html

{content}
"""
            except FileNotFoundError:
                # กรณีที่ไม่พบไฟล์ mypage.htm
                response = """\
HTTP/1.0 404 Not Found
Content-Type: text/html

<h1>404 Not Found</h1>
<p>The file mypage.htm was not found on the server.</p>
"""

            # ส่ง HTTP Response กลับไปยังไคลเอนต์
            client_socket.sendall(response.encode('utf-8'))

        # ตรวจสอบการร้องขอไฟล์ .png
        elif "GET /" in request and ".png" in request:
            try:
                # แยกชื่อไฟล์ออกจาก request
                requested_file = request.split("GET /")[1].split(" ")[0]
                with open(requested_file, "rb") as file:
                    content = file.read()

                # สร้าง HTTP Response message พร้อมเนื้อหาจากไฟล์ .png
                response = b"HTTP/1.0 200 OK\r\nContent-Type: image/png\r\n\r\n" + content

                # ส่ง response แบบไบนารีไปยังไคลเอนต์
                client_socket.sendall(response)

            except FileNotFoundError:
                # กรณีที่ไม่พบไฟล์ .png ที่ร้องขอ
                response = """\
HTTP/1.0 404 Not Found
Content-Type: text/html

<h1>404 Not Found</h1>
<p>The requested image was not found on the server.</p>
"""
                client_socket.sendall(response.encode('utf-8'))

        else:
            # กรณีไม่พบหน้าอื่น ๆ
            response = """\
HTTP/1.0 404 Not Found
Content-Type: text/html

<h1>404 Not Found</h1>
<p>The requested page was not found on the server.</p>
"""
            client_socket.sendall(response.encode('utf-8'))

        # ปิดการเชื่อมต่อ
        client_socket.close()
        print("Connection closed.\n")

except KeyboardInterrupt:
    print("Server shutting down...")
finally:
    server_socket.close()
