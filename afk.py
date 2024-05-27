import pyautogui
import random
import time
import tkinter as tk
from threading import Thread
import json

running = False

def smooth_move(x, y, duration):
    start_x, start_y = pyautogui.position()
    steps = int(duration * 100)
    for i in range(steps):
        current_x = start_x + (x - start_x) * (i / steps)
        current_y = start_y + (y - start_y) * (i / steps)
        pyautogui.moveTo(current_x, current_y)
        time.sleep(duration / steps)

def random_smooth_mouse_movement():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    duration = random.uniform(0.5, 2.0)
    smooth_move(x, y, duration)

def random_key_press(keys):
    key = random.choice(keys)
    pyautogui.press(key)

def random_mouse_click():
    x, y = pyautogui.position()
    pyautogui.click(x, y, clicks = 1, intervl = 0.25)

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileExistsError:
        config = {
            "predefined": {
                "wasd": ["w", "a", "s", "d"],
                "spacebar": ["space"],
                "mouse": ["mouse_movement", "mouse_click"]
            },
            "custom": []
        }
        with open('config.json','w') as f:
            json.dump(config, f, indent = 4)
    return config

config = load_config()
selected_actions = []

def start():
    global running
    running = True
    Thread(target=main).start()

def stop():
    global running
    running = False

def main():
    actions = {
        "mouse_movement": random_smooth_mouse_movement,
        "mouse_click": random_mouse_click,
        "key_press": lambda: random_key_press(selected_actions)
    }
    try:
        while running:
            action_key = random.choice(selected_actions)
            action = actions.get(action_key, lambda: random_key_press([action_key]))
            action()
            time.sleep(random.uniform(1,5))
    except KeyboardInterrupt:
        print("program stopped by user")

root = tk.Tk()
root.title("AFK Preventer")

def update_selection_actions():
    selected_actions.clear()
    if wasd_var.get():
        selected_actions.extend(config["predefined"]["wasd"])
    if spacebar_var.get():
        selected_actions.extend(config["predefined"]["spacebar"])
    if mouse_var.get():
        selected_actions.extend(config["predefined"]["mouse"])
    selected_actions.extend(custom_actions_entry.get().split(','))

wasd_var = tk.BooleanVar()
spacebar_var = tk.BooleanVar()
mouse_var = tk.BooleanVar()

wasd_check = tk.Checkbutton(root, test="WASD", variable=wasd_var, command=update_selection_actions)
wasd_check.pack()

spacebar_check = tk.Checkbutton(root, text='Spacebar', variable=spacebar_var, command=update_selection_actions)
spacebar_check.pack()

mouse_check = tk.Checkbutton(root, text="Mouse Movements and Clicks", variable=mouse_var, command=update_selection_actions)
mouse_check.pack()

custom_actions_label = tk.Label(root, text="Custom Actions (comma-separated):")
custom_actions_label.pack()

custom_actions_entry = tk.Entry(root)
custom_actions_entry.pack()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

root.mainloop()