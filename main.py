import customtkinter as ctk
import webbrowser
import subprocess
import os
import time
import json

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
config_file = os.path.join(os.getenv("APPDATA"), "chrome_adam_config.json")

def show_support_popup():
    result = {"choice": None}
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Chrome Adam")
    root.resizable(False, False)

    # 1. Main Message (The Calligraphic Note)
    message = ctk.CTkLabel(
        root,
        text="If this tool has saved you time, your support keeps it running\nand helps add new features.",
        font=("Lucida Calligraphy", 15, "bold"), 
        text_color="#E0E0E0",
    )
    message.pack(pady=(20, 10), padx=20)

    # --- ROW 1: GitHub Info ---
    github_frame = ctk.CTkFrame(root, fg_color="transparent")
    github_frame.pack(pady=(0, 10))

    ctk.CTkLabel(github_frame, text="Setup Guide: ", font=("Segoe UI", 11)).pack(side="left")

    github_btn = ctk.CTkButton(
        github_frame,
        text="View on GitHub",
        width=80,
        height=24,
        fg_color="transparent",
        text_color="#7aa2f7",
        hover_color="#24283b",
        command=lambda: webbrowser.open("https://github.com/victor-folorunso/chrome-adam")
    )
    github_btn.pack(side="left")

    # --- ROW 2: Action Buttons ---
    action_frame = ctk.CTkFrame(root, fg_color="transparent")
    action_frame.pack(fill="x", padx=30, pady=(10, 20))
    
    def on_support():
        result["choice"] = "support"
        webbrowser.open("https://paystack.shop/pay/chrome-adam")
        root.destroy()

    def on_decline():
        result["choice"] = "decline"
        root.destroy()

    continue_btn = ctk.CTkButton(
        action_frame,
        text="Use Without Supporting",
        font=("Segoe UI", 12),
        height=40,
        corner_radius=8,
        fg_color="#2b2b2b",
        hover_color="#3a3a3a",
        command=on_decline,
    )
    continue_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

    support_btn = ctk.CTkButton(
        action_frame,
        text="Support Chrome-Adam",
        font=("Segoe UI", 12, "bold"),
        height=40,
        corner_radius=8,
        command=on_support,
    )
    support_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

    # --- AUTO-FIT LOGIC ---
    root.update_idletasks()
    # Get the width and height the widgets actually NEED
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.mainloop()
    return result["choice"]

def get_launch_count():
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                data = json.load(f)
                return data.get("launches", 0)
        except:
            return 0
    return 0


def increment_launch_count():
    count = get_launch_count() + 1
    try:
        with open(config_file, "w") as f:
            json.dump({"launches": count}, f)
    except Exception as e:
        print(f"Could not save config: {e}")
    return count

def launch_profiles():
    profile_folders = [
        f
        for f in os.listdir(user_data_dir)
        if os.path.isdir(os.path.join(user_data_dir, f)) and f.startswith("Profile")
    ]

    for profile in profile_folders:
        try:
            subprocess.Popen(
                [
                    chrome_path,
                    f"--profile-directory={profile}",
                    f"--user-data-dir={user_data_dir}",
                ],
                creationflags=subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP,
            )
            time.sleep(1)
        except:
            pass


# Main execution
count = increment_launch_count()
# Show popup every 50 launches
if count > 0 and count % 1 == 0:
    user_choice = show_support_popup()
    
    if user_choice == "support":
        print("User chose to support. Blocking execution.")
    else:
        # User declined or closed window, proceed as normal
        launch_profiles()
else:
    # It wasn't the 50th launch, just run normally
    launch_profiles()