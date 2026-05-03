import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "shull_secret_2026")

# Supabase Setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch full details from 'users' table using the TCN in session
    user_id = session.get('user_id')
    try:
        response = supabase.table("users").select("*").eq("tcn", user_id).single().execute()
        user_data = response.data
        
        if not user_data:
            return redirect(url_for('logout'))

        # Passing all variables to the HTML
        return render_template('index.html', 
                               tcn=user_data.get('tcn'),
                               nickname=user_data.get('nickname'),
                               first_name=user_data.get('first_name'),
                               last_name=user_data.get('last_name'))
    except Exception as e:
        print(f"Error fetching user: {e}")
        return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Add your login and registration routes here...

if __name__ == '__main__':
    app.run(debug=True)
