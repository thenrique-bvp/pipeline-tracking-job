from typing import Dict
import requests
import json
from pathlib import Path

def get_total_users_by_category(category: str) -> int:
    base_url = "https://brain.bessemer.io/twitter/users/categorized/paged"
    
    try:
        url = f"{base_url}?page=1&per_page=1&category={category}&new=true"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('total_users', 0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {category}: {e}")
        return 0

def get_counts() -> Dict[str, int]:
    return {
        'founder': get_total_users_by_category('founder'),
        'startup': get_total_users_by_category('startup')
    }

def send_email(email: str, html: str, edition_number: int = 1) -> None:
    data = {
        "recipient": email,
        "subject": f"XTracker - Founder and Startup Leads Edition #{edition_number}",
        "body": html,
    }
    
    try:
        response = requests.post(
            'http://3.144.127.65/send_email',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        print('Email sent successfully:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error sending email:', error)

def generate_email_template(counts: Dict[str, int]) -> str:
    styles = '''
        body {
            margin: 0;
            padding: 0;
            font-family: 'Poppins', Arial, sans-serif;
            background-color: #F4F4F4;
            color: #333;
        }
        .container {
            max-width: 600px;
            width: 90%;
            margin: 30px auto;
            background-color: #FFF;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.12);
        }
        .header {
            background: #204F85;
            color: #FFF;
            text-align: center;
            padding: 30px;
            position: relative;
        }
        .header h1 {
            margin: 10px 0 5px;
            font-size: 28px;
            font-weight: 700;
        }
        .header p {
            font-size: 16px;
            font-weight: 300;
            margin-top: 5px;
            opacity: 0.9;
        }
        .content {
            padding: 35px 25px;
            text-align: center;
            font-weight: 400;
            line-height: 1.5;
        }
        .stats {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 25px;
        }
        .stat-box {
            background-color: #FFF;
            color: #204F85;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #204F85;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 80%
        }
        .box-2 {
            margin-top: 20px;
        }
        .stat-box h1 {
            margin: 10px 0;
            font-size: 34px;
            font-weight: 700;
            color: #204F85;
        }
        .stat-box p {
            font-size: 18px;
            font-weight: 700;
            margin: 10px 0;
        }
        .icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .cta {
            text-align: center;
            margin-top: 35px;
        }
        .cta a {
            display: inline-block;
            padding: 15px 35px;
            background-color: #204F85;
            color: #FFF;
            text-decoration: none;
            font-size: 18px;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        }
        .footer {
            background-color: #F4F4F4;
            text-align: center;
            padding: 25px;
            font-size: 14px;
            color: #666;
            font-weight: 300;
        }
    '''

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 BessieX Tracker - New Companies Added!</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        {styles}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 New Companies Added!</h1>
            <p>BessieX Tracker - Edition #1</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <div class="stat-box">
                    <div class="icon">🏢</div>
                    <h1>{counts["founder"]}</h1>
                    <p>New Founders</p>
                </div>
                <div class="stat-box box-2">
                    <div class="icon">📊</div>
                    <h1>{counts["startup"]}</h1>
                    <p>New Startups</p>
                </div>
            </div>
            
            <div class="cta">
                <a href="https://platform.bessemer.io//x-tracker/overview">View the latest now!</a>
            </div>
        </div>

        <div class="footer">
            <p>💡 Get these companies before it's too late!</p>
        </div>
    </div>
</body>
</html>'''

def get_or_update_edition(increment: bool = False, reset: bool = False) -> int:
    config_file = Path("config.json")
    
    # Criar arquivo se não existir
    if not config_file.exists():
        config = {"edition": 1}
        config_file.write_text(json.dumps(config, indent=2))
        return 1
    
    # Ler configuração atual
    config = json.loads(config_file.read_text())
    
    # Resetar
    if reset:
        config["edition"] = 1
    # Incrementar
    elif increment:
        config["edition"] += 1
    
    # Salvar alterações
    config_file.write_text(json.dumps(config, indent=2))
    
    return config["edition"]
