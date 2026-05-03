import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_123")

# Supabase Setup
url = os.environ.get("https://varjyniqlnttcuvmwvvz.supabase.co")
key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhcmp5bmlxbG50dGN1dm13dnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMzc1MzksImV4cCI6MjA5MTcxMzUzOX0.OLOQdw2TBP-xzCdEXGL21jRIFh2s9bNiokr23qYwv1c")

# Check if keys exist before starting
if not url or not key:
    print("CRITICAL ERROR: SUPABASE_URL or SUPABASE_KEY is missing from Render Settings")
else:
    supabase: Client = create_client(url, key)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user_id = session.get('user_id')
        # Fetch user
        res = supabase.table("users").select("*").eq("tcn", user_id).execute()
        
        if not res.data:
            return redirect(url_for('logout'))
        
        # Flex-case normalization
        raw = res.data[0]
        data = {k.lower(): v for k, v in raw.items()}
        
        return render_template('index.html', 
                               tcn=data.get('tcn'), 
                               nickname=data.get('nickname'),
                               first_name=data.get('first_name', ''), 
                               last_name=data.get('last_name', ''))
    except Exception as e:
        print(f"Index Error: {e}")
        return "Database Connection Error. Please check logs.", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tcn_val = request.form.get('tcn')
        try:
            res = supabase.table("users").select("*").eq("tcn", tcn_val).execute()
            if res.data:
                user = res.data[0]
                # Fallback for keys
                session['user_id'] = user.get('tcn') or user.get('TCN')
                session['nickname'] = user.get('nickname') or user.get('Nickname')
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Login Error: {e}")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Use dynamic port for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
