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
    ssh_client.connect(hostname=host,port=port,username=username,password=password)

    # The 2nd argument will br the name/id of the person whom we want to share our file
    receiver_name = sys.argv[1]

    with open("user_id.txt", "r") as dir_file:
        sender_name = dir_file.read().strip()

    # create an SFTP client object
    sftp = ssh_client.open_sftp()

    filename = sys.argv[2]
    # The directory will follow this convention to store the file in the server
    directory_name = sender_name + "->" + receiver_name

    # Check if the directory exists, if not, create it
    try:
        sftp.stat(directory_name)
    except FileNotFoundError:
        sftp.mkdir(directory_name)

    # download a file from the remote server
    files = sftp.put(filename,f"{directory_name}/{filename}")

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
