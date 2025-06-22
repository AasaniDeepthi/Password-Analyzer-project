import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os

LOG_FILE = "firewall_log.txt"

class FirewallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Firewall Monitor")

        self.log_area = scrolledtext.ScrolledText(root, width=80, height=25, state='disabled')
        self.log_area.pack(padx=10, pady=10)

        self.start_btn = tk.Button(root, text="Start Firewall", command=self.start_firewall)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(root, text="Stop Firewall", command=self.stop_firewall, state='disabled')
        self.stop_btn.pack(side=tk.LEFT)

        self.update_logs()

    def start_firewall(self):
        self.process = subprocess.Popen(["sudo", "python3", "firewall.py"])
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

    def stop_firewall(self):
        if self.process:
            self.process.terminate()
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

    def update_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = f.read()
            self.log_area.config(state='normal')
            self.log_area.delete(1.0, tk.END)
            self.log_area.insert(tk.END, logs)
            self.log_area.config(state='disabled')
        self.root.after(2000, self.update_logs)

if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallGUI(root)
    root.mainloop()
