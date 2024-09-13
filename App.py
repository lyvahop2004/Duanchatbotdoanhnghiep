from flask import Flask, render_template, request
import requests
import json
import os

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Đường dẫn đến file JSON lưu trữ cuộc hội thoại và từ khóa
JSON_FILE = "db.json"
DULIEU_FILE = "dulieu.json"

# Khóa API
API_KEY = "AIzaSyBm35WccL1JACjJ0R53I64tc93KvpoGmEg"

# Hàm để khởi tạo file JSON nếu chưa tồn tại
def initialize_json_file():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)

    if not os.path.exists(DULIEU_FILE):
        with open(DULIEU_FILE, 'w') as f:
            # Tạo dữ liệu mẫu trong dulieu.json
            sample_data = [
                {"field": "quần áo", "keywords": ["quần áo", "thời trang", "fashion", "áo", "giày"]},
                {"field": "it", "keywords": ["công nghệ", "máy tính", "màn hình", "AI"]}
            ]
            json.dump(sample_data, f, indent=4)

# Đọc file JSON để lấy danh sách lĩnh vực và từ khóa
def read_dulieu_json():
    try:
        with open(DULIEU_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {DULIEU_FILE}: {e}")
        return []

# Lấy danh sách lĩnh vực từ file dulieu.json
def get_allowed_topics():
    data = read_dulieu_json()
    return [item["field"] for item in data]

# Lấy từ khóa cho lĩnh vực được chọn từ dulieu.json
def get_topic_keywords(topic):
    data = read_dulieu_json()
    for item in data:
        if item["field"].lower() == topic.lower():
            return item["keywords"]
    return []

# Kiểm tra câu hỏi của người dùng có thuộc lĩnh vực được chọn không
def is_question_in_topic(user_input, topic):
    # Lấy từ khóa cho lĩnh vực đã chọn
    keywords = get_topic_keywords(topic)
    # Kiểm tra xem câu hỏi của người dùng có chứa từ khóa của lĩnh vực hiện tại không
    for keyword in keywords:
        if keyword.lower() in user_input.lower():
            return True
    return False

# Chức năng chatbot
def chatbot_response(user_input):
    try:
        # Lấy danh sách lĩnh vực hợp lệ từ dulieu.json
        allowed_topics = get_allowed_topics()
        
        # Ví dụ: Chọn lĩnh vực mặc định (hoặc có thể thay đổi để chọn từ danh sách)
        selected_topic = "quần áo"

        # Kiểm tra xem lĩnh vực đã được chọn hay chưa
        if not selected_topic or selected_topic not in allowed_topics:
            return f"Lĩnh vực '{selected_topic}' không được phép."

        # Kiểm tra xem câu hỏi có thuộc lĩnh vực được chọn không
        if not is_question_in_topic(user_input, selected_topic):
            return f"Câu hỏi của bạn không thuộc doanh nghiệp của chúng tôi. Công ty chúng tôi cung cấp các dịch vụ về '{selected_topic}'. Vui lòng hỏi về lĩnh vực '{selected_topic}'."

        # URL API được sử dụng để gửi yêu cầu
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

        # Headers: Chỉ định rằng nội dung của yêu cầu phải ở định dạng JSON
        headers = {
            'Content-Type': 'application/json',
        }

        # Dữ liệu được gửi đến API
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_input
                        }
                    ]
                }
            ]
        }

        # Gửi yêu cầu POST đến API
        response = requests.post(url, headers=headers, json=payload)

        # Kiểm tra lỗi HTTP
        response.raise_for_status()

        # Xử lý phản hồi
        response_data = response.json()
        text = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No content found')

        # Lưu cuộc hội thoại vào file JSON
        try:
            with open(JSON_FILE, 'r+') as f:
                data = json.load(f)
                data.append({"user": user_input, "bot": text, "topic": selected_topic})
                f.seek(0)
                json.dump(data, f, indent=4)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except IOError as e:
            print(f"I/O error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return text.strip()

    except requests.exceptions.HTTPError as http_err:
        # Ghi lại nội dung phản hồi lỗi
        print(f"Error details: {response.text}")
        return f"HTTP Error: {str(http_err)}"
    except requests.exceptions.RequestException as req_err:
        return f"Request Error: {str(req_err)}"
    except Exception as e:
        return f"General Error: {str(e)}"

# Định tuyến cho trang chủ
@app.route("/")
def index():
    return render_template("index.html")

# Route để lấy phản hồi từ chatbot
@app.route("/get", methods=["GET"])
def get_bot_response():
    user_input = request.args.get('msg')
    if not user_input:
        return "No message provided", 400
    return chatbot_response(user_input)

# Khởi động ứng dụng Flask
if __name__ == "__main__":
    initialize_json_file()
    app.run(port=5000, debug=True)
