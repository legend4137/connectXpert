#!/usr/bin/env python
import os
import ftplib
import time
import paramiko
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import imaplib
import email
import socket
import tkinter as tk
import threading
import pyautogui
from PIL import Image, ImageTk


# Information about the server which will be in the debian package
HOSTNAME = "172.31.14.180"
USERNAME = "dooploop"
PASSWORD = "qwertyuiop12345"


def receive_server(name):
    try:
        # Connect FTP Server
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"

        # The 2nd argument will be the name/id of the person who shared our file
        sender_name = name

        filename = "user_id.txt"
        with open(filename, "r") as file:
            receiver_name = file.read().strip()

        # The directory will follow this convention to check the file in the server (same as the one created during upload)
        directory_name = sender_name + "->" + receiver_name

        foldername = "user_dest.txt"
        try :
            with open(foldername, "r") as file:
                save_directory = file.read().strip()
        except FileNotFoundError:
            pass
        
        ftp_server.cwd(directory_name)
        files = ftp_server.nlst()
        # Receive and delete each file in the desired directory

        for file_name in files:
            # Open a local file to store the received data
            if save_directory:
                local_path = os.path.join(save_directory, file_name)
                
                with open(local_path, "wb") as local_file:
                    ftp_server.retrbinary(f"RETR {file_name}", local_file.write)
            else:
                with open(file_name, "wb") as local_file:
                    ftp_server.retrbinary(f"RETR {file_name}", local_file.write)
            
            # Delete the file from the FTP server after receiving
            ftp_server.delete(file_name)
            print(f"File '{file_name}' received and deleted from FTP server.")

        time.sleep(3)
        # Close the Connection
        if 'ftp_server' in locals():
            ftp_server.quit()

    except ftplib.all_errors as e:
        print(f"FTP Error: {e}")

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError as ve:
        print(ve)

        

def send_server(file_path, name):
    try:
        # Connect FTP Server
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"

        # The 3rd argument will be the file we want to share with the other person
        filename = file_path

        with open("user_id.txt", "r") as dir_file:
            sender_name = dir_file.read().strip()
      

        # The 2nd argument will br the name of the id of the person whom we want to share our file
        receiver_name = name

        # The directory will follow this convention to store the file in the server
        directory_name = sender_name + "->" + receiver_name


        # Checking if the directory already exists
        existing_directories = ftp_server.nlst()
        if directory_name in existing_directories:
            print("")
        else:
            ftp_server.mkd(directory_name)

        # Uploading the file in the desired directory
        with open(filename, "rb") as file:
            ftp_server.storbinary(f"STOR {directory_name}/{os.path.basename(filename)}", file)

        print("Successfully Sent")

        time.sleep(3)
        # Close the Connection
        if 'ftp_server' in locals():
            ftp_server.quit()

    except ftplib.all_errors as error:
        print(f"FTP Error: {error}")

    except IndexError:
        print("Error: Missing command-line arguments. Please provide receiver name and filename.")

    except FileNotFoundError:
        print("Error: File not found.")


def register_id(name):
    # Take input from the user
    # user_name = input("Enter user_id: ")
    user_name = name

    # Define the filename
    user_filename = "user_id.txt"

    # Write the input to a text file
    with open(user_filename, "w") as file:
        file.write(user_name)


    print("Successfully Regsitered")

def register_dest(destination):
    # Take input from the user
    # user_name = input("Enter user_id: ")
    file_path = destination

    # Define the filename
    user_filename = "user_dest.txt"

    # Write the input to a text file
    with open(user_filename, "w") as file:
        file.write(file_path)


    print("Successfully Regsitered")
    time.sleep(3)


# Function for sending files
def send():
    receiver_name = input("Enter receiver name: ")
    file_path = input("Enter file path: ").replace('"', '')
    send_server(file_path, receiver_name)

# Function for receiving files
def receive():
    sender_name = input("Enter sender name: ")
    receive_server(sender_name)

# Function for receiving files
def sftp__receive():
    sender_name = input("Enter sender name: ")
    sftp_receive(sender_name)

# Function for receiving files
def sftp__send():
    receiver_name = input("Enter receiver name: ")
    file_path = input("Enter file path: ").replace('"', '')
    sftp_send(file_path, receiver_name)

# Function for registering user_id
def user_id():
    choice = input("setup/change user_id(Y/n): ")
    if choice == "Y":
        name = input("Enter User_ID: ")
        register_id(name)

    choice = input("setup/change directory(Y/n): ")
    if choice == "Y":
        directory = input("Enter directory: ").replace('"', '')
        register_dest(directory)


def sftp_send(file_path, name):

    with open("user_id.txt", "r") as dir_file:
        sender_name = dir_file.read().strip()
    try:
        # create ssh client 
        ssh_client = paramiko.SSHClient()

        # remote server credentials
        host = "172.31.14.180"
        username = "dooploop"
        password = "qwertyuiop12345"
        port = 22

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host,port=port,username=username,password=password)

        # The 2nd argument will br the name/id of the person whom we want to share our file
        receiver_name = name

        # create an SFTP client object
        sftp = ssh_client.open_sftp()

        filename = file_path
        # The directory will follow this convention to store the file in the server
        directory_name = sender_name + "->" + receiver_name

        # Check if the directory exists, if not, create it
        try:
            sftp.stat(directory_name)
        except FileNotFoundError:
            sftp.mkdir(directory_name)

        # download a file from the remote server
        sftp.put(filename,f"{directory_name}/{os.path.basename(filename)}")

        time.sleep(3)
        sftp.close()
        ssh_client.close()

    except paramiko.AuthenticationException as auth_exception:
        print("Authentication failed:", auth_exception)
    except paramiko.SSHException as ssh_exception:
        print("Unable to establish SSH connection:", ssh_exception)
    except FileNotFoundError as file_not_found_exception:
        print("File not found:", file_not_found_exception)
    except Exception as e:
        print("An error occurred:", e)


def sftp_receive(name):
 
    try:
        # create ssh client 
        ssh_client = paramiko.SSHClient()

        # remote server credentials
        host = "172.31.14.180"
        username = "dooploop"
        password = "qwertyuiop12345"
        port = 22

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, port=port, username=username, password=password)

        # The 2nd argument will be the name/id of the person whom we want to share our file
        sender_name = name

        file_path = 'user_id.txt'
        try:
            with open(file_path, "r") as dir_file:
                receiver_name = dir_file.read().strip()
        except FileNotFoundError:
            pass
        # create an SFTP client object
        sftp = ssh_client.open_sftp()

        # The directory will follow this convention to store the file in the server
        directory_name = sender_name + "->" + receiver_name

        foldername = "user_dest.txt"
        try :
            with open(foldername, "r") as file:
                save_directory = file.read().strip()
        except FileNotFoundError:
            pass

        try:
            sftp.chdir(directory_name)
        except FileNotFoundError:
            print(f"Directory '{directory_name}' not found. There is no file sent by {sender_name}, all the files fetched.")

        for filename in sftp.listdir():
            try:
                if save_directory:
                    local_file = os.path.join(save_directory, filename)
                    sftp.get(filename, local_file)
                    sftp.remove(filename)
                else:
                    sftp.get(filename, filename)
                    sftp.remove(filename)

                
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except Exception as e:
                print(f"Error occurred while processing '{filename}': {e}")

        time.sleep(3)
        sftp.close()
        ssh_client.close()

    except paramiko.AuthenticationException as auth_exception:
        print("Authentication failed:", auth_exception)
    except paramiko.SSHException as ssh_exception:
        print("Unable to establish SSH connection:", ssh_exception)
    except FileNotFoundError as file_not_found_exception:
        print("File not found:", file_not_found_exception)
    except Exception as e:
        print("An error occurred:", e)

def send_email(sender_email,sender_password,recipient_email,subject,message,attachment):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attachment:
        attachment_part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as attachment_file:
            attachment_part.set_payload(attachment_file.read())
        encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', f'attachment; filename= {attachment}')
        msg.attach(attachment_part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Mail sent successfully")
    time.sleep(3)

def send_mail():
    sender_email = input('Enter your email: ')
    sender_password = getpass.getpass('Enter your password(APP PASSWORD(Google Authetication)): ')
    recipient_email = input('Enter recipient email address: ')
    subject = input('Enter email subject: ')
    message = input('Enter email message: ')
    attachment = input('Enter attachment file path (press Enter if none): ')

    send_email(sender_email,sender_password,recipient_email,subject,message,attachment)

def fetch_emails(email_address, password):
  
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    mail.select('inbox')

    # Search for unseen emails
    _, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()[::-1]  # Reverse order to get latest emails first

    for email_id in email_ids:
        _, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        print('From:', msg['From'])
        print('Subject:', msg['Subject'])
        print('Body:', msg.get_payload())

    mail.logout()
    print("DONE")
    time.sleep(3)


def mail_view():
    email_address = input('Enter your email: ')
    password = getpass.getpass('Enter your password(APP PASSWORD(Google Authetication)): ')

    fetch_emails(email_address, password)

def screen_share(conn):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.thumbnail((480, 270))
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
    host_ip = input("Enter your IP address: ")
    server_socket.bind((f'{host_ip}', 12356))
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

def screen_server():
    start_server()


def screen_client():
    root = tk.Tk()
    root.title('Remote Desktop Client')

    host_ip = input("Enter IP Address of Server: ")
    client_socket = socket.socket()
    client_socket.connect((host_ip, 12356))

    label = tk.Label(root)
    label.pack()

    def display_screenshot():
        while True:
            try:
                img_size = int.from_bytes(client_socket.recv(4), byteorder='big')
                screenshot_bytes = b''
                while len(screenshot_bytes) < img_size:
                    screenshot_bytes += client_socket.recv(img_size - len(screenshot_bytes))
                screenshot = Image.frombytes("RGB", (480, 270), screenshot_bytes)
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



    # threading.Thread(target=display_screenshot, args=(client_socket, label)).start()

    # root.bind('<Motion>', lambda event: move_mouse(event, client_socket))
    # root.bind('<Key>', lambda event: send_keyboard_input(event, client_socket))

    threading.Thread(target=display_screenshot).start()

    root.bind('<Motion>', move_mouse)
    root.bind('<Key>', send_keyboard_input)

    
    root.mainloop()

options = {
    "send": send,
    "receive": receive,
    "id": user_id,
    "secure-send": sftp__send,
    "secure-receive":sftp__receive,
    "email": send_mail,
    "inbox": mail_view,
    "client": screen_client,
    "server": screen_server,
}

    # Parse arguments
print(""" connectXpert 0.7.0
      --------------------------------------------------------------------------
      FTP sending type "send"
      FTP receiving type "receive"
      SFTP sending type "secure-send"
      SFTP receiving type "secure-receive"
      EMAIL sending type "mail"
      EMAIL receiving type "inbox"
      for screensharing type "client"  for viewer (make sure server and client are running at same time)
      for screesharing type "server" for displayer (make sure server and client are running at same time)
      For ID and Destination type "id"
    ----------------------------------------------------------------------------
      Once any task is done, app closes....so no worries 
    ----------------------------------------------------------------------------
      Enter your ID and Destination folder(optional) when installed by choosing (id) which can be changed later on 
    ----------------------------------------------------------------------------
    To access all services please install ftplib, paramiko, os
    smtplib, email, imaplib, socket, tk, pyautogui, PIL, time
    getpass, threading""")

option = input("Choose an option (): ").lower()
if option in options:
    options[option]()

else:
    print("Invalid option")

