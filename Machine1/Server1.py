from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import os
import sys


class FileServer:
    def __init__(self, next_server_address=None, next_server_port=None):
        self.next_server_address = next_server_address
        self.next_server_port = next_server_port
        self.visited_servers = set()  # Keep track of visited servers

    def getFileContent(self, filename):
        print("server1 getFileContent:", filename)
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("server1 FileNotFoundError", filename)
            # File not found locally, forward the request to the next nearest server
            return self.forwardRequestToNextServer(filename)

    def forwardRequestToNextServer(self, filename):
        print("server1 forwardRequestToNextServer:", filename)
        if (self.next_server_address, self.next_server_port) in self.visited_servers:
            print("server1 Already visited server. Cannot forward request.")
            return None

        try:
            # Create an XML-RPC client to connect to the next nearest server
            next_server_proxy = ServerProxy(f"http://{self.next_server_address}:{self.next_server_port}")

            # Mark the current server as visited
            self.visited_servers.add((self.next_server_address, self.next_server_port))

            # Call getFileContent on the next nearest server
            return next_server_proxy.getFileContent(filename)
        except Exception as e:
            print("server1 Error forwarding request:", e)
            return None



def main():
    if len(sys.argv) < 4:
        print("Usage: python file_server.py <server_ip> <server_port> <next_server_ip> <next_server_port>")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    next_server_ip = sys.argv[3]
    next_server_port = int(sys.argv[4])

    file_server = FileServer(next_server_ip, next_server_port)

    # Start XML-RPC server
    server = SimpleXMLRPCServer((server_ip, server_port))

    server.register_instance(file_server)
    #server.register_instance(server.getFileContent,'getFileContent')
    print(f"server1 started on {server_ip}:{server_port}. Press Ctrl+C to stop.")

    # Run the server
    server.serve_forever()


if __name__ == "__main__":
    main()
