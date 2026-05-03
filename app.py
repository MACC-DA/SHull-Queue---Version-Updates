from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
# It is better to use an environment variable for the secret key as well
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "SHull_Secret_Key_2026")

# Replace these with your actual credentials or use Environment Variables in Render
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://varjyniqlnttcuvmwvvz.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhcmp5bmlxbG50dGN1dm13dnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMzc1MzksImV4cCI6MjA5MTcxMzUzOX0.OLOQdw2TBP-xzCdEXGL21jRIFh2s9bNiokr23qYwv1c")
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

        response = supabase.table("users").select("*").eq("tcn", tcn).eq("nickname", nickname).execute()

        if response.data:
            user_data = response.data[0]
            if user_data.get('approved') == False:
                status = 'needs_approval' 
                message = True
            else:
                session['user_nickname'] = user_data['nickname']
                return redirect(url_for('index'))
        else:
            status = 'not_registered'
            message = True

    return render_template('login.html', status=status, message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        tcn = request.form.get('tcn')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nickname = request.form.get('nickname')

        data = {
            "tcn": tcn,
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "approved": False 
        }
        
        try:
            supabase.table("users").insert(data).execute()
            return render_template('login.html', status='registered', message=True)
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_nickname', None)
    return redirect(url_for('login'))

# --- FIX START HERE ---
if __name__ == '__main__':
    # Render requires the app to listen on 0.0.0.0 and a dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# --- FIX END HERE ---
