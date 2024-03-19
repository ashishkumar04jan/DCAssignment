from xmlrpc.client import ServerProxy

class FileClient:

    def __init__(self, server_ip, server_port):

        self.server_ip = server_ip

        self.server_port = server_port

        self.server_proxy = ServerProxy(f"http://{self.server_ip}:{self.server_port}")

    def getFileContent(self, filename):
        print("client getFileContent:", filename)
        try:

            # Call getFileContent on the server

            return self.server_proxy.getFileContent(filename)

        except Exception as e:

            print("Error:", e)


def main():
    import sys

    if len(sys.argv) < 4:
        print("Usage: python file_client.py <server_ip> <server_port> <filename>")

        return

    server_ip = sys.argv[1]

    server_port = int(sys.argv[2])

    filename = sys.argv[3]

    # Create a FileClient instance

    client = FileClient(server_ip, server_port)

    # Call getFileContent on the client

    file_content = client.getFileContent(filename)
    print("main:", file_content)
    if file_content is not None:
        with open(filename, "w") as file:
            file.write(file_content)
        print("File content:", file_content)


if __name__ == "__main__":
    main()
