# Một chatbot cơ bản bằng Python
def chatbot():
    print("Xin chào! Tôi là chatbot. Tôi có thể gúp gì cho bạn.")

    while True:
        # Nhận tin nhắn từ người dùng
        user_input = input("Bạn: ")

        # Điều kiện thoát khỏi vòng lặp
        if user_input.lower() in ['thoát', 'exit', 'bye']:
            print("Chatbot: Tạm biệt! Hẹn gặp lại.")
            break

        # Các câu trả lời mẫu
        if "hello" in user_input.lower():
            print("Chatbot: Xin chào!")
        elif "bạn tên gì" in user_input.lower():
            print("Chatbot: Tôi là một chatbot đơn giản.")
        elif "mấy giờ rồi" in user_input.lower():
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f"Chatbot: Bây giờ là {current_time}")
        else:
            print("Chatbot: Xin lỗi, tôi chưa hiểu câu hỏi của bạn.")

# Chạy chatbot
chatbot()
