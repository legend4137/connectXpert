# Import Module
import ftplib
import sys

# Information about the server which will be in the debian package
HOSTNAME = "172.31.14.180"
USERNAME = "dooploop"
PASSWORD = "qwertyuiop12345"

try:
    # Connect FTP Server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"

    # The 2nd argument will be the name/id of the person who shared our file
    sender_name = sys.argv[1]

    filename = "user_id.txt"
    with open(filename, "r") as file:
        receiver_name = file.read().strip()

    # The directory will follow this convention to check the file in the server (same as the one created during upload)
    directory_name = sender_name + "->" + receiver_name

    ftp_server.cwd(directory_name)
    files = ftp_server.nlst()
    # Receive and delete each file in the desired directory

    for file_name in files:
        # Open a local file to store the received data
        with open(file_name, "wb") as local_file:
            ftp_server.retrbinary(f"RETR {file_name}", local_file.write)
        
        # Delete the file from the FTP server after receiving
        ftp_server.delete(file_name)
        print(f"File '{file_name}' received and deleted from FTP server.")

except ftplib.all_errors as e:
    print(f"FTP Error: {e}")

except FileNotFoundError:
    print("Error: File not found.")

except ValueError as ve:
    print(ve)

finally:
    # Close the Connection
    if 'ftp_server' in locals():
        ftp_server.quit()