import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random

# --- CONFIG ---
GROQ_API_KEY = "your_groq_api_key_here"
WAIT_TIME = 600 # 10 minutes
MODEL_ID = "llama-3.3-70b-versatile" # Verify active ID in Groq Console

SOURCES = {
    "MEXT/Embassy": "https://www.in.emb-japan.go.jp/education/japanese_government_scholarships.html",
    "Social/Protest News": "https://www.japantimes.co.jp/news/national/social-issues/",
    "Saitama/Kurdish Tensions": "https://www.tokyoweekender.com/japan-life/news-and-opinion/",
    "Immigration/PR Laws": "https://english.visajapan.jp/qa/news2026.html"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/121.0.0.0"
]

def fetch_intel(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        time.sleep(random.uniform(2, 4)) 
        r = requests.get(url, timeout=20, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return f"[{url}] " + soup.get_text(separator=' ', strip=True)[:2500]
        return ""
    except:
        return ""

def compile_global_brief(data):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    SITUATION REPORT FOR ADITYA (JEE/CS/NATIONAL SHOOTER):
    Synthesize this data into ONE dense, professional paragraph. 
    Focus on: 
    1. MEXT 2027 application window (India focus).
    2. Political climate: PM Takaichi's 'Orderly Coexistence' & Sanseito's 'Japanese First' rhetoric.
    3. Anti-immigrant protests: Tensions in Saitama/Kawaguchi involving the Kurdish community.
    4. New PR Laws: Revocation for unpaid taxes/insurance starting 2027.
    
    DATA: {data}
    """
    
    payload = {"model": MODEL_ID, "messages": [{"role": "user", "content": prompt}]}
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        res_data = res.json()
        if 'choices' in res_data:
            return res_data['choices'][0]['message']['content']
        # If 'choices' is missing, it's an error; return the error message
        return f"GROQ API ERROR: {res_data.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"SYSTEM CRASH: {str(e)}"

if __name__ == "__main__":
    print(f"--- JAPAN GLOBAL SCOUT ACTIVE [{datetime.now().strftime('%H:%M')}] ---")
    while True:
        raw_intel = ""
        for name, link in SOURCES.items():
            print(f"Scouting {name}...")
            raw_intel += fetch_intel(link) + " "
        
        brief = compile_global_brief(raw_intel)
        log_ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"INTEL_{log_ts}.log", "w", encoding="utf-8") as f:
            f.write(brief)
        
        print(f"Log Saved: INTEL_{log_ts}.log\nBrief: {brief[:100]}...")
        time.sleep(WAIT_TIME + random.randint(10, 60))
