import os, threading, re, json, time
from datetime import datetime
import customtkinter as ctk
from curl_cffi import requests as crequests

# --- LEGACY KERNEL REPAIR ---
os.environ['TCL_LIBRARY'] = r"C:\Users\my\AppData\Local\Programs\Python\Python38\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\my\AppData\Local\Programs\Python\Python38\tcl\tk8.6"

class JapanReconV12(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🎌 JAPAN RECON v12.0 | MARCH 2026")
        self.geometry("1000x950")
        ctk.set_appearance_mode("dark")
        self.accent = "#00FF41" 

        self.setup_ui()

    def setup_ui(self):
        # Header
        ctk.CTkLabel(self, text="JAPAN STRATEGIC INTELLIGENCE TERMINAL", 
                     font=("Courier", 28, "bold"), text_color=self.accent).pack(pady=(20, 10))
        
        # --- NEW: NAME SECTION ---
        self.name_entry = ctk.CTkEntry(self, placeholder_text="OPERATOR NAME (e.g., ADITYA YADAV)", 
                                      width=500, border_color=self.accent)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "YOUR NAME") # Defaulting to your name

        # Key Section
        self.key_entry = ctk.CTkEntry(self, placeholder_text="ENTER GROQ_API_KEY", 
                                     width=500, show="*", border_color=self.accent)
        self.key_entry.pack(pady=5)
        
        # Button Container
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        self.btn = ctk.CTkButton(self.btn_frame, text="INITIATE OMNI-SYNC", 
                                 fg_color=self.accent, text_color="black", 
                                 font=("Courier", 14, "bold"), command=self.execute)
        self.btn.grid(row=0, column=0, padx=10)

        # --- NEW: CLEAR LOG BUTTON ---
        self.clear_btn = ctk.CTkButton(self.btn_frame, text="CLEAR TERMINAL", 
                                       fg_color="#FF3131", text_color="white", 
                                       font=("Courier", 14, "bold"), command=self.clear_terminal)
        self.clear_btn.grid(row=0, column=1, padx=10)

        # Terminal Output
        self.terminal = ctk.CTkTextbox(self, width=950, height=600, font=("Consolas", 12), 
                                       fg_color="#000", text_color=self.accent, 
                                       border_width=1, border_color="#333")
        self.terminal.pack(padx=20, pady=10)

    def log(self, msg):
        self.after(0, lambda: self.terminal.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n"))
        self.after(0, lambda: self.terminal.see("end"))

    # --- NEW: CLEAR FUNCTION ---
    def clear_terminal(self):
        self.terminal.delete("1.0", "end")
        self.log(">>> TERMINAL PURGED. READY FOR NEW RECON.")

    def clean_html(self, raw_html):
        text = re.sub(r'<(script|style|nav|footer|header).*?>.*?</\1>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^<]+?>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def execute(self):
        if not self.key_entry.get():
            self.log(">>> [ERR] MISSION ABORTED: GROQ_KEY_MISSING")
            return
        
        operator = self.name_entry.get() if self.name_entry.get() else "UNKNOWN"
        self.log(f">>> [AUTH] ACCESS GRANTED TO OPERATOR: {operator}")
        self.btn.configure(state="disabled", text="INFILTRATING...")
        threading.Thread(target=self.recon_cycle, daemon=True).start()

    def recon_cycle(self):
        self.log(">>> [INIT] SPOOFING BROWSER SIGNATURE...")
        intel_dump = ""
        queries = [
            "MEXT 2027 India application dates research student",
            "Sanae Takaichi Trump meeting March 19 2026 White House",
            "Khamenei death Tehran strike update March 2 2026",
            "Japan News Yomiuri March 2 2026 economy"
        ]

        try:
            for q in queries:
                self.log(f">>>> [SCAN] SEARCHING: {q}")
                r = crequests.get(f"https://www.google.com/search?q={q.replace(' ', '+')}", 
                                  impersonate="chrome120", timeout=25)
                if r.status_code == 200:
                    cleaned = self.clean_html(r.text)
                    intel_dump += f"\n--- [QUERY: {q}] ---\n{cleaned[:3000]}\n"
                    self.log(f">>> [OK] {q} DATA SECURED.")
                    time.sleep(1)
            self.process_with_ai(intel_dump)
        except Exception as e:
            self.log(f">>> [FATAL_ERR] RELAY_ERROR: {str(e)}")
        
        self.btn.configure(state="normal", text="INITIATE OMNI-SYNC")

    def process_with_ai(self, raw_intel):
        self.log(">>> [AI] SYNTHESIZING DATA...")
        key = self.key_entry.get()
        operator = self.name_entry.get()
        
        system_role = (
            f"You are a Strategic Intel Officer for {operator}. DATE: March 2, 2026. "
            "HARD TRUTHS: Khamenei killed Feb 28; MEXT 2027 India deadline May 13; "
            "Takaichi-Trump summit March 19. Anchor your briefing in these facts."
        )

        models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        for model_id in models:
            try:
                r = crequests.post("https://api.groq.com/openai/v1/chat/completions",
                                   headers={"Authorization": f"Bearer {key}"},
                                   json={
                                       "model": model_id,
                                       "messages": [
                                           {"role": "system", "content": system_role},
                                           {"role": "user", "content": f"Briefing for {operator}. Data: {raw_intel}"}
                                       ]
                                   }, timeout=30)
                if r.status_code == 200:
                    summary = r.json()['choices'][0]['message']['content']
                    self.log(f"\n[MODEL: {model_id}]\n" + "="*60 + f"\nREPORT FOR {operator}:\n" + summary + "\n" + "="*60)
                    return 
                elif r.status_code == 429:
                    self.log(f">>> [WARN] {model_id} RATE LIMITED. SWITCHING...")
            except Exception as e:
                self.log(f">>> [ERR] UPLINK ERROR: {str(e)}")

if __name__ == "__main__":
    app = JapanReconV12()
    app.mainloop()
