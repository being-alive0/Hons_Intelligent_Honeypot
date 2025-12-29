import pandas as pd
import json
import os
import ml_engine  # Import our new ML module

def analyze_logs(log_file='honeypot_log.json'):
    print("[*] Reading logs...")
    records = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except:
                    continue
    
    if not records:
        print("Log file is empty or missing.")
        return

    df = pd.DataFrame(records)

    # --- Standard Stats ---
    top_ips = df['ip_address'].value_counts().nlargest(5)

    if 'credentials' in df.columns:
        credentials = df['credentials'].explode().dropna()
        user_pass = [f"{c.get('username','')}:{c.get('password','')}" for c in credentials if isinstance(c, dict)]
        top_credentials = pd.Series(user_pass).value_counts().nlargest(5)
    else:
        top_credentials = pd.Series()

    all_commands = []
    if 'commands' in df.columns:
        for cmd_list in df['commands']:
            if isinstance(cmd_list, list):
                for cmd in cmd_list:
                    all_commands.append(cmd)
    
    cmd_df = pd.DataFrame(all_commands, columns=['command'])
    top_commands = cmd_df['command'].value_counts().nlargest(5)
    
    # --- ML Classification Step ---
    print("[*] Running ML Classification & Detailed Analysis...")
    
    attack_details = {}
    
    if not cmd_df.empty:
        # Predict the type for every command
        cmd_df['attack_type'] = cmd_df['command'].apply(ml_engine.predict_attack_type)
        
        # Descriptions for the dashboard popup
        descriptions = {
            "Reconnaissance": "Attempts to gather system info (CPU, users, network) to find vulnerabilities.",
            "Malware Download": "Attempts to fetch malicious binaries or scripts (wget, curl) from external C2 servers.",
            "Destruction": "Commands intended to wipe data, format drives, or crash the system (Denial of Service).",
            "Persistence": "Techniques to maintain access across restarts (e.g., modifying startup scripts/cron).",
            "Privilege Escalation": "Attempts to gain root/admin access using exploits.",
            "Defense Evasion": "Attempts to disable security tools like firewalls or clear system logs.",
            "Unknown/Noise": "Unclassified or generic activity."
        }

        # Group by type to build the detailed view
        for type_name, group in cmd_df.groupby('attack_type'):
            attack_details[type_name] = {
                "count": int(len(group)),
                "description": descriptions.get(type_name, "Security event detected."),
                # specific commands used in this category and their counts
                "commands": group['command'].value_counts().to_dict() 
            }

    print("\n--- ML Results Generated ---")

    # --- Save Data for Dashboard ---
    if not os.path.exists('dashboard_data'):
        os.makedirs('dashboard_data')
        
    top_ips.to_json('dashboard_data/top_ips.json')
    top_credentials.to_json('dashboard_data/top_credentials.json')
    top_commands.to_json('dashboard_data/top_commands.json')
    
    # Save the complex details object (New File)
    with open('dashboard_data/attack_details.json', 'w') as f:
        json.dump(attack_details, f, indent=4)
    
    print("[*] Analysis complete. Data saved.")

if __name__ == '__main__':
    analyze_logs()