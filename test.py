import httpx

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyAsOtCXwUark_Ctu3F3WLyapEdiFeMRlVQ"
payload = {"contents": [{"parts": [{"text": "hi"}]}]}

try:
    with httpx.Client(verify=False) as client:
        res = client.post(url, json=payload)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")