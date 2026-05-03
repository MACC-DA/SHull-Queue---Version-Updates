import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
# Uses a fallback key if the environment variable isn't set yet
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "shull_default_secret_2026")

# Supabase Configuration pulled from Render Environment Variables
SUPABASE_URL = os.environ.get("https://varjyniqlnttcuvmwvvz.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZhcmp5bmlxbG50dGN1dm13dnZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxMzc1MzksImV4cCI6MjA5MTcxMzUzOX0.OLOQdw2TBP-xzCdEXGL21jRIFh2s9bNiokr23qYwv1c")

# Safety check: if keys are missing, the app will print a clear message instead of crashing
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL or SUPABASE_KEY not found in Environment Variables!")
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    try:
        # Fetch user data safely
        query = supabase.table("users").select("*").eq("tcn", user_id).execute()
        
        if not query.data:
            return redirect(url_for('logout'))
            
        user_data = query.data[0] # Get the first matching user

        return render_template('index.html', 
                               tcn=user_data.get('tcn', 'N/A'),
                               nickname=user_data.get('nickname', 'User'),
                               first_name=user_data.get('first_name', ''),
                               last_name=user_data.get('last_name', ''))
    except Exception as e:
        print(f"Database Error: {e}")
        return "Internal Server Error", 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Render uses the PORT environment variable automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
