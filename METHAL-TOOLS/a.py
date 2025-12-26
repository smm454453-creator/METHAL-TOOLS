"""
METHAL TOOLS
Author   : Haikall Adly
Version  : 1.0
GitHub   : https://github.com/smm454453-creator
License  : MIT (Attribution Required)

⚠ Removing this header does not remove authorship.
"""

import os
import sys
import time
import json
import threading
import socket
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- CONFIGURATION & THEME ---
COLOR_BG = "#0b0b0b"
COLOR_FG = "#00ff00" 
COLOR_ACCENT = "#ff0000" 
COLOR_CYAN = "#00ffff" 
FONT_MAIN = ("Consolas", 10)
FONT_BOLD = ("Consolas", 11, "bold")

class MethalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("METHAL INTELLIGENCE SUITE v3.0 [ULTIMATE SYMMETRY]")
        self.root.geometry("1100x650") 
        self.root.configure(bg=COLOR_BG)
        
        self.current_module = None
        self.stop_event = threading.Event()
        self.total_terkirim = 0
        self.ent_target = None
        self.ent_param = None
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_folder = os.path.join(self.base_dir, "LOGS")
        if not os.path.exists(self.log_folder): os.makedirs(self.log_folder)
        self.db_file = os.path.join(self.log_folder, "methal_history.json")
        
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({"ip_tracking": [], "path": [], "banner": [], "vuln": [], "whois": [], "header": []}, f)

        self.setup_ui()
        self.load_home()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=COLOR_BG, bd=1, relief="sunken")
        header.pack(fill="x", padx=10, pady=5)
        tk.Label(header, text="🎇 METHAL MULTI-TOOLS v3.0", bg=COLOR_BG, fg=COLOR_ACCENT, font=("Consolas", 16, "bold")).pack(side="left", pady=10)
        tk.Label(header, text="BUILDER: Haikall", bg=COLOR_BG, fg="white", font=FONT_MAIN).pack(side="right", padx=10)

        container = tk.Frame(self.root, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=10)

        sidebar_outer = tk.Frame(container, bg="#151515", width=220, bd=1, relief="ridge")
        sidebar_outer.pack(side="left", fill="y", pady=5)
        sidebar_outer.pack_propagate(False)

        self.canvas = tk.Canvas(sidebar_outer, bg="#151515", highlightthickness=0, width=220)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_sidebar = tk.Frame(self.canvas, bg="#151515")
        self.canvas.create_window((0, 0), window=self.scrollable_sidebar, anchor="nw", width=220)
        self.scrollable_sidebar.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        tk.Label(self.scrollable_sidebar, text="[ MAIN MENU ]", bg="#151515", fg="white", font=FONT_BOLD).pack(pady=(15, 5))
        self.create_menu_btn(self.scrollable_sidebar, "HOME DASHBOARD", "home", "white")

        
               

        tk.Label(self.scrollable_sidebar, text="[ TYPE: WEB TOOLS ]", bg="#151515", fg=COLOR_CYAN, font=FONT_BOLD).pack(pady=(20, 5))
        self.create_menu_btn(self.scrollable_sidebar, "IP TRACKER", "ip", COLOR_CYAN)
        self.create_menu_btn(self.scrollable_sidebar, "PATH DISCOVERY", "path", COLOR_CYAN)
        self.create_menu_btn(self.scrollable_sidebar, "BANNER GRABBER", "banner", COLOR_CYAN)
        self.create_menu_btn(self.scrollable_sidebar, "VULN SCANNER", "vuln", COLOR_CYAN)
        self.create_menu_btn(self.scrollable_sidebar, "WHOIS AUDITOR", "whois", COLOR_CYAN)
        self.create_menu_btn(self.scrollable_sidebar, "HEADER CHECK", "header", COLOR_CYAN)
        
        tk.Label(self.scrollable_sidebar, text="[ SYSTEM ]", bg="#151515", fg="white", font=FONT_BOLD).pack(pady=(20, 5))
        self.create_menu_btn(self.scrollable_sidebar, "VIEW HISTORY", "history", "magenta")

        self.content_frame = tk.Frame(container, bg=COLOR_BG)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.config_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        self.config_frame.pack(fill="x", pady=5)

        self.terminal = tk.Text(self.content_frame, bg="black", fg=COLOR_FG, font=FONT_MAIN, state='disabled', bd=0, highlightthickness=1, highlightbackground="#333", wrap="none")
        self.terminal.pack(fill="both", expand=True, pady=5)

    def create_menu_btn(self, parent, text, mod_id, color):
        tk.Button(parent, text=text, bg="#222", fg=color, activebackground=color, font=FONT_MAIN, bd=0, pady=8, 
                  command=lambda: self.load_module(mod_id, text)).pack(fill="x", padx=10, pady=2)

    def log(self, text, color=COLOR_FG):
        self.terminal.config(state='normal')
        self.terminal.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n", "color_tag")
        self.terminal.tag_config("color_tag", foreground=color)
        self.terminal.see(tk.END)
        self.terminal.config(state='disabled')

    def draw_thick_table(self, title, rows, color=COLOR_CYAN):
        c1 = 20; c2 = 60
        self.log(f"╔{'═'*(c1+2)}╦{'═'*(c2+2)}╗", color)
        self.log(f"║ {title.center(c1)} ║ {'INFORMASI / DATA'.center(c2)} ║", color)
        self.log(f"╠{'═'*(c1+2)}╬{'═'*(c2+2)}╣", color)
        for key, val in rows:
            v_str = str(val)
            if len(v_str) > c2: v_str = v_str[:c2-3] + "..."
            self.log(f"║ {str(key):<{c1}} ║ {v_str:<{c2}} ║", color)
        self.log(f"╚{'═'*(c1+2)}╩{'═'*(c2+2)}╝", color)

    def load_home(self):
        self.terminal.config(state='normal'); self.terminal.delete('1.0', tk.END); self.terminal.config(state='disabled')
        for w in self.config_frame.winfo_children(): w.destroy()
        tk.Label(self.config_frame, text="METHAL DASHBOARD MAIN MENU", bg=COLOR_BG, fg=COLOR_CYAN, font=FONT_BOLD).pack(pady=10)
        self.draw_thick_table("BUILDER", [("NAMA", "Haikall"), ("VERSI", "3.0 Stable"), ("TAHUN", "2025")], COLOR_ACCENT)
        self.draw_thick_table("IMPORTANT NOTE", [("NOTICE", "Please remember, this tool is not to be misused.")], COLOR_CYAN)

    def show_module_manual(self, mod_id):
        manuals = {

            "ip": [("FUNGSI", "Trace Geolocation IP."), ("PENJELASAN", "Melacak lokasi fisik, ISP, dan koordinat IP."), ("CARA PAKAI", "Input IP -> RUN")],
            "path": [("FUNGSI", "Discovery file sensitif."), ("CARA PAKAI", "Input URL -> RUN")],
            "banner": [("FUNGSI", "Identifikasi port terbuka."), ("CARA PAKAI", "Input IP -> RUN")],
            "vuln": [("FUNGSI", "Vulnerability Scanner."), ("PENJELASAN", "Scan celah keamanan website."), ("CARA PAKAI", "Input URL -> RUN")],
            "whois": [("FUNGSI", "Lookup data registrasi domain."), ("CARA PAKAI", "Input URL -> RUN")],
            "header": [("FUNGSI", "Analisis teknologi server."), ("CARA PAKAI", "Input URL -> RUN")]
        }
        if mod_id in manuals:
            self.draw_thick_table(f"MANUAL: {mod_id.upper()}", manuals[mod_id], COLOR_FG)

    def load_module(self, mod_id, name):
        if mod_id == "home": self.load_home(); return
        self.terminal.config(state='normal'); self.terminal.delete('1.0', tk.END); self.terminal.config(state='disabled')
        for w in self.config_frame.winfo_children(): w.destroy()
        self.current_module = mod_id
        self.show_module_manual(mod_id)
        if mod_id == "history": self.show_all_history(); return
        tk.Label(self.config_frame, text=f"MODUL: {name}", bg=COLOR_BG, fg="white", font=FONT_BOLD).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0,5))
        tk.Label(self.config_frame, text="TARGET:", bg=COLOR_BG, fg="white").grid(row=1, column=0, sticky="w")
        self.ent_target = tk.Entry(self.config_frame, bg="#333", fg="white", width=30)
        self.ent_target.grid(row=1, column=1, padx=5)
        curr_col = 2       

        tk.Button(self.config_frame, text="RUN", bg=COLOR_FG, width=10, command=self.execute).grid(row=1, column=curr_col, padx=5)
        tk.Button(self.config_frame, text="STOP", bg=COLOR_ACCENT, fg="white", width=10, command=lambda: self.stop_event.set()).grid(row=1, column=curr_col+1, padx=5)

    def save_to_history(self, cat, det):
        try:
            with open(self.db_file, "r") as f: data = json.load(f)
            data[cat].append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "detail": det})
            with open(self.db_file, "w") as f: json.dump(data, f, indent=4)
        except: pass

        
    def execute(self):
        if not self.ent_target:
            return

        t = self.ent_target.get()
        if not t:
            return

        self.stop_event.clear()

        if self.current_module == "ip":
            threading.Thread(target=self.run_ip, args=(t,), daemon=True).start()
        elif self.current_module == "path":
            threading.Thread(target=self.run_path, args=(t,), daemon=True).start()
        elif self.current_module == "banner":
            threading.Thread(target=self.run_banner, args=(t,), daemon=True).start()
        elif self.current_module == "vuln":
            threading.Thread(target=self.run_vuln, args=(t,), daemon=True).start()
        elif self.current_module == "whois":
            threading.Thread(target=self.run_whois, args=(t,), daemon=True).start()
        elif self.current_module == "header":
            threading.Thread(target=self.run_header, args=(t,), daemon=True).start()




    def update_attack_table(self, mode, t, j):
        if self.stop_event.is_set(): return
        status = "ON"
        try:
            requests.get(t, timeout=1)
            status = "ON"
        except: status = "DOWN"
        
        self.terminal.config(state='normal'); self.terminal.delete('1.0', tk.END); self.terminal.config(state='disabled')
        self.draw_thick_table(f"LIVE {mode} STATUS", [
            ("WEB/LINK TUJUAN", t),
            ("JUMLAH BOT TERKIRIM", j),
            ("BOT TELAH MASUK", self.total_terkirim),
            ("STATUS WEBSITE", status)
        ], COLOR_ACCENT if status=="DOWN" else COLOR_FG)
        self.root.after(1000, lambda: self.update_attack_table(mode, t, j))       

    def run_ip(self, t):
        try:
            r = requests.get(f"http://ip-api.com/json/{t}").json()
            res = [("ISP", r.get('isp')), ("KOTA", r.get('city')), ("NEGARA", r.get('country')), ("STATUS", r.get('status'))]
            self.draw_thick_table("IP RESULT", res, COLOR_CYAN); self.save_to_history("ip_tracking", f"{t} trace")
        except: self.log("[-] Error IP Trace", COLOR_ACCENT)

    def run_path(self, t):
        self.log(f"[*] Scanning paths on {t}...", COLOR_CYAN)
        found = []; headers = {'User-Agent': 'Mozilla/5.0'}
        host = t if t.startswith("http") else f"http://{t}"
        for p in ["/admin", "/.env", "/config", "/wp-admin", "/phpmyadmin", "/.git"]:
            try:
                r = requests.get(f"{host}{p}", headers=headers, timeout=3)
                if r.status_code == 200: found.append(p)
            except: pass
        self.draw_thick_table("PATH DISCOVERY", [("TARGET", t), ("FOUND", ", ".join(found) if found else "NOT FOUND")], COLOR_CYAN)
        self.save_to_history("path", f"{t} scan")

    def run_banner(self, t):
        res = []
        for p in [21, 22, 80, 443, 3306]:
            try:
                s = socket.socket(); s.settimeout(1); s.connect((t, p)); res.append(f"Port {p}: OPEN"); s.close()
            except: pass
        self.draw_thick_table("BANNER GRAB", [("PORT STATUS", x) for x in res] if res else [("INFO", "No Open Port")], COLOR_CYAN)
        self.save_to_history("banner", f"{t} port scan")

    def run_vuln(self, t):
        try:
            r = requests.get(f"{t}/.env", timeout=3)
            s = "VULNERABLE (.env exposed)" if r.status_code == 200 else "SECURE"
            self.draw_thick_table("VULN SCAN", [("WEB", t), ("RESULT", s)], COLOR_ACCENT if "VULN" in s else COLOR_FG)
            self.save_to_history("vuln", f"{t} check")
        except: self.log("[-] Target unreachable.")

    def run_whois(self, t):
        try:
            ip = socket.gethostbyname(t)
            self.draw_thick_table("WHOIS LOOKUP", [("DOMAIN", t), ("IP ADDR", ip), ("STATUS", "RESOLVED")], COLOR_CYAN)
            self.save_to_history("whois", f"{t} lookup")
        except: self.log("[-] DNS Error.")

    def run_header(self, t):
        try:
            r = requests.get(t, timeout=3)
            res = [("SERVER", r.headers.get('Server', 'Hidden')), ("X-POWERED", r.headers.get('X-Powered-By', 'N/A')), ("TYPE", r.headers.get('Content-Type'))]
            self.draw_thick_table("HEADER ANALYSIS", res, COLOR_CYAN)
            self.save_to_history("header", f"{t} header")
        except: self.log("[-] Header Grab Error.")

    def show_all_history(self):
        self.log("\n[ MEMBUKA DATABASE HISTORY METHAL v3.0 ]", "magenta")
        if not os.path.exists(self.db_file): return
        with open(self.db_file, "r") as f:
            data = json.load(f)
            for cat, logs in data.items():
                if logs:
                    self.draw_thick_table(cat.upper(), [(l['timestamp'], l['detail']) for l in logs[-5:]], "magenta")

if __name__ == "__main__":
    root = tk.Tk(); app = MethalGUI(root); root.mainloop()  