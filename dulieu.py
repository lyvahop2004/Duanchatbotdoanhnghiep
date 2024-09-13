from flask import Flask, request, jsonify, render_template,redirect,url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'dulieu.json'
# Hàm hỗ trợ tải danh sách người dùng từ tệp JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Hàm hỗ trợ lưu danh sách người dùng vào tệp JSON
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Route trang chủ - hiển thị trang HTML với dữ liệu từ file JSON
@app.route('/')
def index():
    data = load_data()  # Đọc dữ liệu từ file JSON
    return render_template("admin/adddata/index.html", data=data)  # Truyền dữ liệu vào trang HTML

# Route thêm dữ liệu mới
@app.route('/admin/adddata/add_data', methods=['GET', 'POST'])
def add_data():
    error_message = None
    if request.method == 'POST':
        field = request.form['field']
        keywords = request.form['keywords']
        
        # Tải dữ liệu
        data_list = load_data()  # Đổi tên biến để tránh xung đột với biến bên trong vòng lặp
        
        # Kiểm tra nếu lĩnh vực hoặc từ khóa đã tồn tại
        for entry in data_list:  # Đổi tên 'data' thành 'entry' để lặp qua các mục trong danh sách
            if entry['field'] == field:
                error_message = "Lĩnh vực này đã tồn tại. Vui lòng nhập lĩnh vực khác."
                return render_template('/admin/adddata/add_data.html', error=error_message)
            if entry['keywords'] == keywords:
                error_message = "Từ khóa này đã tồn tại. Vui lòng nhập từ khác."
                return render_template('/admin/adddata/add_data.html', error=error_message)

        # Tạo dữ liệu mới
        new_data = {
            "id": len(data_list) + 1,  # Đổi 'data' thành 'data_list' để dùng đúng biến
            "field": field,
            "keywords": keywords
        }

        # Thêm dữ liệu mới vào danh sách
        data_list.append(new_data)

        # Lưu danh sách vào tệp
        save_data(data_list)
        
        return redirect(url_for('index'))

    return render_template('/admin/adddata/add_data.html', error=error_message)


# Route cập nhật dữ liệu
@app.route('/admin/adddata/edit/<int:data_id>', methods=['GET', 'POST'])
def edit_data(data_id):
    datas = load_data()  # Load all users from the JSON file
    data = next((u for u in datas if u['id'] == data_id), None)

    if not data:
        return "User not found", 404

    if request.method == 'POST':
        # Update the user's details
        data['field'] = request.form['field']
        data['keywords'] = request.form['keywords']
        

        # Save the updated users list to the JSON file
        save_data(datas)

        # Redirect back to the user list
        return redirect(url_for('index'))

    # Render the edit form with the current user details
    return render_template('/admin/adddata/edit.html', data=data)
# xóa
@app.route('/admin/adddata/delete/<int:data_id>', methods=['POST'])
def delete_data(data_id):
    # Tải danh sách data hiện tại
    datas = load_data()
    
    # Tìm và xóa datta có data_id được chỉ định
    updated_datas = [data for data in datas if data['id'] != data_id]
    
    # Lưu danh sách data đã được cập nhật vào file JSON
    save_data(updated_datas)

    # Chuyển hướng trở lại trang danh sách data
    return redirect(url_for('index'))

# xóa

if __name__ == "__main__":
    
    app.run(port=5001, debug=True)
