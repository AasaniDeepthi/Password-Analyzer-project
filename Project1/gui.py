import os
import tkinter as tk
from tkinter import ttk, messagebox
from app.generator import generate_wordlist
from app.analyzer import analyze_password
import subprocess
from datetime import datetime
import uuid

def launch_gui():
    root = tk.Tk()
    root.title("Password Strength & Wordlist Tool")
    root.geometry("600x500")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # ---------- Wordlist Generator Tab ----------
    gen_frame = ttk.Frame(notebook)
    notebook.add(gen_frame, text="Generate Wordlist")

    entries = {}
    labels = ["Full Name", "Birthdate", "Pet Name", "Favourite Book", "Bike/Car Name"]
    for idx, label in enumerate(labels):
        ttk.Label(gen_frame, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
        entry = ttk.Entry(gen_frame, width=40)
        entry.grid(row=idx, column=1, pady=5)
        entries[label] = entry

    # Add Other Info (optional) field
    optional_label = "Other Info (optional)"
    ttk.Label(gen_frame, text=optional_label).grid(row=len(labels), column=0, padx=10, pady=5, sticky='w')
    optional_entry = ttk.Entry(gen_frame, width=40)
    optional_entry.grid(row=len(labels), column=1, pady=5)
    entries[optional_label] = optional_entry

    output_label = ttk.Label(gen_frame, text="Output File Name (optional):")
    output_label.grid(row=len(labels)+1, column=0, padx=10, pady=5, sticky='w')
    output_entry = ttk.Entry(gen_frame, width=30)
    output_entry.grid(row=len(labels)+1, column=1, pady=5)

    def generate_and_save():
        user_inputs = [e.get() for e in entries.values() if e.get().strip()]
        wordlist = generate_wordlist(user_inputs)

        if not wordlist:
            messagebox.showerror("No Passwords", "No passwords were generated.")
            return

        os.makedirs("wordlists", exist_ok=True)
        filename = output_entry.get().strip()
        if not filename:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:6]
            filename = f"wordlist_{now}_{unique_id}.txt"
        elif not filename.endswith(".txt"):
            filename += ".txt"

        filepath = os.path.join("wordlists", filename)

        if os.path.exists(filepath):
            if not messagebox.askyesno("Overwrite?", f"File '{filename}' exists. Overwrite?"):
                return

        with open(filepath, 'w') as f:
            for word in wordlist:
                f.write(word + '\n')

        messagebox.showinfo("Saved", f"Wordlist saved to:\n{os.path.abspath(filepath)}")
        try:
            os.startfile(os.path.abspath(filepath))  # Windows
        except:
            subprocess.call(['open', os.path.abspath(filepath)])  # macOS/Linux

    ttk.Button(gen_frame, text="Generate Wordlist", command=generate_and_save).grid(
        row=len(labels)+2, column=0, columnspan=2, pady=10
    )

    # ---------- Password Analyzer Tab ----------
    analyzer_frame = ttk.Frame(notebook)
    notebook.add(analyzer_frame, text="Analyze Password")

    ttk.Label(analyzer_frame, text="Enter Password:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    password_entry = ttk.Entry(analyzer_frame, show='*', width=40)
    password_entry.grid(row=0, column=1, pady=10)

    show_var = tk.BooleanVar()
    def toggle_password():
        password_entry.config(show='' if show_var.get() else '*')

    ttk.Checkbutton(analyzer_frame, text="Show Password", variable=show_var, command=toggle_password).grid(
        row=1, column=1, sticky='w', padx=10
    )

    result_text = tk.Text(analyzer_frame, height=10, width=60)
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def analyze():
        pwd = password_entry.get().strip()
        if not pwd:
            messagebox.showerror("Error", "Please enter a password.")
            return
        result = analyze_password(pwd)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Password: {result['password']}\n")
        result_text.insert(tk.END, f"Score (0=Weak, 4=Strong): {result['score']}\n")
        result_text.insert(tk.END, f"Estimated Crack Time: {result['crack_time']}\n\n")
        if result['feedback']['warning']:
            result_text.insert(tk.END, f"⚠️ Warning: {result['feedback']['warning']}\n")
        if result['feedback']['suggestions']:
            result_text.insert(tk.END, f"💡 Suggestions: " + ", ".join(result['feedback']['suggestions']))

    ttk.Button(analyzer_frame, text="Analyze", command=analyze).grid(row=2, column=0, columnspan=2)

    root.mainloop()

if __name__ == '__main__':
    launch_gui()