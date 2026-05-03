import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
# Secure key for session management
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "shull_2026_secure")

# Supabase Connection
url = os.environ.get("https://varjyniqlnttcuvmwvvz.supabase.co")
key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhcmp5bmlxbG50dGN1dm13dnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMzc1MzksImV4cCI6MjA5MTcxMzUzOX0.OLOQdw2TBP-xzCdEXGL21jRIFh2s9bNiokr23qYwv1c")
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    try:
        # Fetch user data from Supabase
        res = supabase.table("users").select("*").eq("tcn", user_id).execute()
        
        if not res.data:
            return redirect(url_for('logout'))
        
        # FLEXIBLE CASE FIX: Convert all DB keys to lowercase
        raw_data = res.data[0]
        user_data = {k.lower(): v for k, v in raw_data.items()}

        return render_template('index.html', 
                               tcn=user_data.get('tcn'), 
                               nickname=user_data.get('nickname'),
                               first_name=user_data.get('first_name', ''), 
                               last_name=user_data.get('last_name', ''))
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tcn_input = request.form.get('tcn')
        try:
            res = supabase.table("users").select("*").eq("tcn", tcn_input).execute()
            if res.data:
                user = res.data[0]
                # Store in session (handles both tcn and TCN)
                session['user_id'] = user.get('tcn') or user.get('TCN')
                session['nickname'] = user.get('nickname') or user.get('Nickname')
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Login error: {e}")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
