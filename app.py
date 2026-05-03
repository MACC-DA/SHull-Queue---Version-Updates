from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = "SHull_Secret_Key_2026" # Change this to any random string

# Replace with your actual Supabase Credentials
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user_nickname' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', nickname=session['user_nickname'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    status = None
    message = False

    if request.method == 'POST':
        tcn = request.form.get('tcn')
        nickname = request.form.get('nickname')

        # Search Supabase for the user
        response = supabase.table("users").select("*").eq("tcn", tcn).eq("nickname", nickname).execute()

        if response.data:
            # Check if admin has approved (Assuming a 'status' column in your DB)
            user_data = response.data[0]
            if user_data.get('approved') == False:
                status = 'needs_approval' # Logic for login2.JPG
                message = True
            else:
                session['user_nickname'] = user_data['nickname']
                return redirect(url_for('index'))
        else:
            status = 'not_registered' # Logic for login3.JPG
            message = True

    return render_template('login.html', status=status, message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        tcn = request.form.get('tcn')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nickname = request.form.get('nickname')

        # Insert into Supabase
        data = {
            "tcn": tcn,
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "approved": False # Default to false for login2.JPG scenario
        }
        
        try:
            supabase.table("users").insert(data).execute()
            # Redirect to login with a success message
            return render_template('login.html', status='registered', message=True)
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_nickname', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)