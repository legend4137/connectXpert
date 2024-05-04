# client.py
import socket
import tkinter as tk
import threading
from PIL import Image, ImageTk


def display_screenshot():
    while True:
        try:
            img_size = int.from_bytes(client_socket.recv(4), byteorder='big')
            screenshot_bytes = b''
            while len(screenshot_bytes) < img_size:
                screenshot_bytes += client_socket.recv(img_size - len(screenshot_bytes))
            screenshot = Image.frombytes("RGB", (1280, 1024), screenshot_bytes)
            img = ImageTk.PhotoImage(screenshot)
            label.config(image=img)
            label.image = img
        except:
            break

def move_mouse(event):
    x, y = event.x * 2, event.y * 2
    data = f"{x} {y}"
    client_socket.send(data.encode())

def send_keyboard_input(event):
    data = event.char
    client_socket.send(data.encode())

root = tk.Tk()
root.title('Remote Desktop Client')

client_socket = socket.socket()
client_socket.connect(('172.31.55.146', 12345))

label = tk.Label(root)
label.pack()

threading.Thread(target=display_screenshot).start()

root.bind('<Motion>', move_mouse)
root.bind('<Key>', send_keyboard_input)

root.mainloop()
