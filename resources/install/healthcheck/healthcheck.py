#!/usr/bin/python3 -u

import signal
import socketserver
import subprocess
import sys
import threading

# opens the configuration file and stores the healthcheck commands to be executed
with open("/etc/healthcheck.conf") as file:
    commands = file.read().splitlines()


# overrides default ForkingTCPServer class to avoid "Address already in use" error
class ReuseAddressForkingTCPServer(socketserver.ForkingTCPServer):
    allow_reuse_address = True


# self-explanatory : this class defines how to handle an incoming request
class HealthCheckRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("> incoming", self.client_address[0])

        for command in commands:
            print("#", command)

            # executes each healthcheck command in a subshell
            sp = subprocess.Popen(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
            sp.wait()

            # if a command fails, returns an error string and exits
            if sp.returncode != 0:
                self.request.sendall("failed".encode("ascii"))
                print("< failed")
                return

        # if none of the commands failed, returns a success string and exits
        self.request.sendall("ok".encode("ascii"))
        print("< ok")


# entrypoint
if __name__ == "__main__":
    # creates a forking server : each request spawns a new process
    server = ReuseAddressForkingTCPServer(("0.0.0.0", 2501), HealthCheckRequestHandler)

    # handles signals properly
    def shutdown(signum, frame): server.shutdown()
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, shutdown)

    # starts the server thread
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    print("healthcheck started")
