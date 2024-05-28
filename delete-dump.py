import paramiko
import os

# Configuration
HOSTNAME = 'your_server_ip_or_hostname'
USERNAME = 'your_username'
PRIVATE_KEY_PATH = '/path/to/private/key'
DUMP_DIRECTORY = '/path/to/dump/directory'
DUMP_FILE_PATTERN = '*.dmp'  # Adjust the pattern to match your dump files


def delete_dump_files(hostname, username, private_key_path, dump_directory, dump_file_pattern):
    # Initialize the SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

        # Connect to the server using the private key
        ssh.connect(hostname, username=username, pkey=private_key)

        # Find and delete the dump files
        delete_command = f"find {dump_directory} -type f -name '{dump_file_pattern}' -delete"
        stdin, stdout, stderr = ssh.exec_command(delete_command)

        # Read the output and error streams
        out = stdout.read().decode()
        err = stderr.read().decode()

        if err:
            print(f"Error deleting files: {err}")
        else:
            print(f"Deleted dump files from {dump_directory}")

    except Exception as e:
        print(f"Failed to connect or delete files: {str(e)}")
    finally:
        # Close the SSH connection
        ssh.close()


if __name__ == '__main__':
    delete_dump_files(HOSTNAME, USERNAME, PRIVATE_KEY_PATH,
                      DUMP_DIRECTORY, DUMP_FILE_PATTERN)
