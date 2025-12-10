"""Quick GUI test to verify Tkinter is working"""
import tkinter as tk

# Create simple test window
root = tk.Tk()
root.title("🎮 LED Controller Test")
root.geometry("900x700")
root.configure(bg='#1a1a1a')

# Title
title = tk.Label(
    root,
    text="🎮 Virtual AI LED Controller",
    font=('Arial', 24, 'bold'),
    bg='#1a1a1a',
    fg='#00FF00'
)
title.pack(pady=30)

# Create 6 LED circles
colors = [
    ("#00FF00", "LED 1 - Green"),
    ("#FF0000", "LED 2 - Red"),
    ("#0000FF", "LED 3 - Blue"),
    ("#FFFF00", "LED 4 - Yellow"),
    ("#FF00FF", "LED 5 - Magenta"),
    ("#00FFFF", "LED 6 - Cyan")
]

frame = tk.Frame(root, bg='#1a1a1a')
frame.pack(expand=True)

for idx, (color, label) in enumerate(colors):
    row = idx // 2
    col = idx % 2
    
    led_frame = tk.Frame(frame, bg='#1a1a1a')
    led_frame.grid(row=row, column=col, padx=30, pady=20)
    
    # Label
    lbl = tk.Label(led_frame, text=label, font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='#FFFFFF')
    lbl.pack()
    
    # LED circle
    canvas = tk.Canvas(led_frame, width=100, height=100, bg='#1a1a1a', highlightthickness=0)
    canvas.pack(pady=5)
    canvas.create_oval(10, 10, 90, 90, fill=color, outline='#555555', width=2)
    
    # Status
    status = tk.Label(led_frame, text="TEST", font=('Arial', 10), bg='#1a1a1a', fg='#00FF00')
    status.pack()

# Instructions
info = tk.Label(
    root,
    text="If you see this window with 6 colored LEDs, Tkinter is working!\nClose this window to continue.",
    font=('Arial', 10),
    bg='#1a1a1a',
    fg='#888888'
)
info.pack(pady=20)

root.mainloop()
