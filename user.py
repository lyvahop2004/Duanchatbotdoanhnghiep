from flask import Flask, request, render_template, redirect, url_for,flash
import json
import os

app = Flask(__name__)
# tạm



# Gọi đến user.json
USER_FILE = 'user.json'

# Helper function to load users from the JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Helper function to save users to the JSON file
def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

@app.route('/')
def user_list():
    users = load_users()
    return render_template('/admin/User/user.html', users=users)

# thêm mới
@app.route('/admin/User/create', methods=['GET', 'POST'])
def create_user():
    error_message = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sodt = request.form['sodt']
        password = request.form['password']
        
        users = load_users()
        for user in users:
            if user['email'] == email:
                error_message = "Email đã tồn tại. Vui lòng chọn email khác."
                return render_template('/admin/User/create.html', error=error_message)
            if user['sodt'] == sodt:
                error_message = "Số điện thoại đã tồn tại. Vui lòng chọn số khác."
                return render_template('/admin/User/create.html', error=error_message)

        new_user = {
            "id": len(users) + 1,
            "name": name,
            "email": email,
            "sodt": sodt,
            "password": password
        }
        users.append(new_user)
        save_users(users)
        return redirect(url_for('user_list'))

    return render_template('/admin/User/create.html', error=error_message)




# sửa
@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    users = load_users()  # Load all users from the JSON file
    user = next((u for u in users if u['id'] == user_id), None)

    if not user:
        return "User not found", 404

    if request.method == 'POST':
        # Update the user's details
        user['name'] = request.form['name']
        user['email'] = request.form['email']
        user['sodt'] = request.form['sodt']
        user['password'] = request.form['password']

        # Save the updated users list to the JSON file
        save_users(users)

        # Redirect back to the user list
        return redirect(url_for('user_list'))

    # Render the edit form with the current user details
    return render_template('/admin/User/edit.html', user=user)


# sửa
# xóa
@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Tải danh sách người dùng hiện tại
    users = load_users()
    
    # Tìm và xóa người dùng có user_id được chỉ định
    updated_users = [user for user in users if user['id'] != user_id]
    
    # Lưu danh sách người dùng đã được cập nhật vào file JSON
    save_users(updated_users)

    # Chuyển hướng trở lại trang danh sách người dùng
    return redirect(url_for('user_list'))

# xóa

if __name__ == '__main__':
    app.run(debug=True)
