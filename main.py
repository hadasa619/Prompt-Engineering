import os
import ssl
import httpx
import gradio as gr
from dotenv import load_dotenv

# ביטול אימות SSL בצורה אגרסיבית עבור נטפרי
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl_context = ssl._create_unverified_context()

load_dotenv()

def translate_to_cli(user_text):
    api_key = os.getenv("GEMINI_API_KEY")
    
    # כתובת ה-URL הכי פשוטה שיש למודל הפלאש
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    
    # שליחת המפתח כפרמטר בשאילתה (Query Parameter)
    params = {'key': api_key}
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Translate this to a Windows PowerShell command: {user_text}. Return ONLY the command."}]
        }]
    }

    try:
        # שימוש ב-client פשוט ללא הגדרות מסובכות
        with httpx.Client(verify=False) as client:
            response = client.post(url, params=params, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                # הדפסת השגיאה המדויקת מהשרת לטרמינל
                print(f"Server Response: {response.text}")
                return f"שגיאה {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"שגיאה בתקשורת: {str(e)}"

with gr.Blocks() as demo:
    input_box = gr.Textbox(label="מה את רוצה לעשות?")
    output_box = gr.Textbox(label="הפקודה")
    btn = gr.Button("שלח")
    btn.click(translate_to_cli, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    demo.launch(server_port=7860)