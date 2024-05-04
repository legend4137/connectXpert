# server.py
import socket
import tkinter as tk
import threading
import pyautogui

def screen_share(conn):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.thumbnail((1280, 1024))
            screenshot_bytes = screenshot.tobytes()
            conn.send(len(screenshot_bytes).to_bytes(4, byteorder='big'))
            conn.sendall(screenshot_bytes)
        except:
            break

def receive_mouse_movement(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            x, y = map(int, data.split())
            pyautogui.moveTo(x, y)
        except:
            break

def receive_keyboard_input(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            pyautogui.write(data)
        except:
            break

def start_server():
    server_socket = socket.socket()
    server_socket.bind(('172.31.55.146', 12345))
    server_socket.listen()

    print("Waiting for connection...")
    conn, address = server_socket.accept()
    print("Connection from:", address)

    threading.Thread(target=screen_share, args=(conn,)).start()
    threading.Thread(target=receive_mouse_movement, args=(conn,)).start()
    threading.Thread(target=receive_keyboard_input, args=(conn,)).start()

    root = tk.Tk()
    root.title('Remote Desktop Server')
    root.geometry('960x540')
    root.mainloop()

start_server()
