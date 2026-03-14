import os
import gradio as gr  # השורה הזו הייתה חסרה!
from groq import Groq
from dotenv import load_dotenv

# טעינת המשתנים מהקובץ
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# בדיקה בטרמינל
if not api_key:
    print("❌ שגיאה: לא נמצא מפתח API בקובץ ה-env!")
else:
    print(f"✅ מפתח API נטען (מתחיל ב: {api_key[:8]}...)")

# הגדרת הלקוח
client = Groq(api_key=api_key)

def translate_to_cli(user_text):
    if not user_text:
        return "נא להזין טקסט..."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a PowerShell expert. Return ONLY the command. No backticks, no markdown."
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה: {str(e)}"

# ממשק Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## ⚡ PowerShell Generator")
    inp = gr.Textbox(label="מה תרצה לעשות?", placeholder="למשל: יצירת תיקייה חדשה בשם 'data'")
    out = gr.Textbox(label="הפקודה המוכנה")
    btn = gr.Button("צור פקודה", variant="primary")
    
    btn.click(fn=translate_to_cli, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch(server_port=7860)