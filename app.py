import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "shull_secure_key_2026")

# Supabase Setup
SUPABASE_URL = os.environ.get("https://varjyniqlnttcuvmwvvz.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhcmp5bmlxbG50dGN1dm13dnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMzc1MzksImV4cCI6MjA5MTcxMzUzOX0.OLOQdw2TBP-xzCdEXGL21jRIFh2s9bNiokr23qYwv1c")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    try:
        # Fetch user details to show in sidebar
        response = supabase.table("users").select("*").eq("tcn", user_id).execute()
        if not response.data:
            return redirect(url_for('logout'))
        
        user = response.data[0]
        return render_template('index.html', 
                               tcn=user.get('tcn'), 
                               nickname=user.get('nickname'),
                               first_name=user.get('first_name'), 
                               last_name=user.get('last_name'))
    except Exception as e:
        print(f"Index Error: {e}")
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tcn = request.form.get('tcn')
        # Simple login logic: find user by TCN
        response = supabase.table("users").select("*").eq("tcn", tcn).execute()
        if response.data:
            user = response.data[0]
            if user.get('approved'):
                session['user_id'] = user['tcn']
                session['nickname'] = user['nickname']
                return redirect(url_for('index'))
            return "Account pending approval."
        return "Invalid TCN."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Your registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
