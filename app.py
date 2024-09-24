from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 预设的管理员和客户的密码
ADMIN_PASSWORD = "admin123"
CUSTOMER_PASSWORDS = ["customer1", "customer2"]  # 可以添加更多客户密码

# 初始化一个简单的表格数据
sheet_data = [
    ["", "", ""],
    ["", "Sample Data", ""],
    ["", "", "Sample Data"]
]


@app.route('/')
def index():
    # 根据用户是否登录，返回不同的界面
    if 'role' in session:
        return render_template('index.html', sheet_data=sheet_data, role=session['role'])
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['role'] = 'admin'
        return redirect(url_for('index'))
    elif password in CUSTOMER_PASSWORDS:
        session['role'] = 'customer'
        return redirect(url_for('index'))
    return "登录失败，密码错误", 403


@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update_sheet():
    if 'role' not in session:
        return "未登录", 403

    # 处理表单数据更新
    data = request.json
    if session['role'] == 'admin':
        # 管理员可以更新整个表格
        global sheet_data
        sheet_data = data['sheet_data']
        return jsonify({"success": True})
    elif session['role'] == 'customer':
        # 客户只能修改空白单元格
        for i, row in enumerate(data['sheet_data']):
            for j, cell in enumerate(row):
                if sheet_data[i][j] == "":  # 只能修改空白部分
                    sheet_data[i][j] = cell
        return jsonify({"success": True})
    return jsonify({"success": False}), 403


if __name__ == '__main__':
    app.run(debug=True)
