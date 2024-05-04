import paramiko
import sys

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
    sender_name = sys.argv[1]

    with open("user_id.txt", "r") as dir_file:
        receiver_name = dir_file.read().strip()

    # create an SFTP client object
    sftp = ssh_client.open_sftp()

    # The directory will follow this convention to store the file in the server
    directory_name = sender_name + "->" + receiver_name

    try:
        sftp.chdir(directory_name)
    except FileNotFoundError:
        print(f"Directory '{directory_name}' not found. There is no file sent by {sender_name}, all the files fetched.")
        sys.exit(1)

    for filename in sftp.listdir():
        try:
            sftp.get(filename, filename)
            sftp.remove(filename)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error occurred while processing '{filename}': {e}")

except paramiko.AuthenticationException as auth_exception:
    print("Authentication failed:", auth_exception)
except paramiko.SSHException as ssh_exception:
    print("Unable to establish SSH connection:", ssh_exception)
except FileNotFoundError as file_not_found_exception:
    print("File not found:", file_not_found_exception)
except Exception as e:
    print("An error occurred:", e)
finally:
    try:
        # close the connection
        sftp.close()
        ssh_client.close()
    except NameError:
        pass  # If sftp or ssh_client is not defined, it means the connection was never established, so no need to close anything