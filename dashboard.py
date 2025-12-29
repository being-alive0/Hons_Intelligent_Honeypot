from flask import Flask, render_template
import json
import os

app = Flask(__name__)
DATA_DIR = 'dashboard_data'

def read_json_data(filename):
    """Helper to read JSON data for the dashboard."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except:
            return {}

@app.route('/')
def index():
    top_ips = read_json_data('top_ips.json')
    top_credentials = read_json_data('top_credentials.json')
    top_commands = read_json_data('top_commands.json')
    
    # NEW: Load detailed ML attack data
    attack_details = read_json_data('attack_details.json')
    
    return render_template('index.html', 
                           top_ips=top_ips, 
                           top_credentials=top_credentials, 
                           top_commands=top_commands,
                           attack_details=attack_details)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)