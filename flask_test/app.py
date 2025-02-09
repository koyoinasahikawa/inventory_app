from flask import Flask, request, render_template_string, redirect, url_for, session
import subprocess

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # セッションの秘密鍵

# 仮のユーザーデータ（実際はDBを使用）
USER_DATA = {"testuser": "password123"}

# ログインフォーム（HTMLをPythonの文字列で定義）
LOGIN_FORM = '''
    <h1>ログイン</h1>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        <label>ID: <input type="text" name="username" value="{{ username }}"></label><br>
        <label>パスワード: <input type="password" name="password"></label><br>
        <input type="submit" value="ログイン">
    </form>
    <p><a href="/">ホームへ戻る</a></p>
'''

def get_current_git_branch():
    """現在のGitブランチを取得する関数"""
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
        return branch
    except subprocess.CalledProcessError:
        return "Gitブランチの取得に失敗しました"

@app.route('/')
def home():
    if 'username' in session:
        return f'<h1>HOME</h1><p>ログイン中: {session["username"]}</p><p><a href="/logout">ログアウト</a></p>'
    return '<h1>HOME</h1><p>現在ログインしていません。</p><p><a href="/login">ログインページへ</a></p>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username  # セッションに保存
            return redirect(url_for('dashboard'))
        else:
            error = "IDまたはパスワードが間違っています"
            return render_template_string(LOGIN_FORM, error=error, username=username)
    
    return render_template_string(LOGIN_FORM, error=None, username="")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        git_branch = get_current_git_branch()  # 現在のGitブランチを取得
        return f'<h1>ダッシュボード</h1><p>ようこそ {session["username"]} さん</p><p>現在のGitブランチ: {git_branch}</p><p><a href="/logout">ログアウト</a></p>'
    return '<h1>ダッシュボード</h1><p>ログインしていません。</p><p><a href="/login">ログインページへ</a></p>'

@app.route('/logout')
def logout():
    if 'username' in session:
        username = session.pop('username', None)  # セッションから削除
        return f'<h1>ログアウトしました</h1><p>さようなら、{username} さん</p><p><a href="/">ホームへ戻る</a></p>'
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
