#!/usr/bin/python3 -u

import argparse
import subprocess
import sys

# command line template
template = "lxc {} ubuntu:xenial {}-{}-{} -p default -p {}"

# authorized lxd commands
commands = ["init", "launch"]

# servers associated with each project
projects = {
    "torii": ["postgresql", "wildfly", "deploy"]
}

# entrypoint
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="docker-compose-like tool to deploy projects on lxd")
    parser.add_argument("command", choices=commands, help="lxd command to run behind the scenes")
    parser.add_argument("project", choices=projects, help="project to deploy (requires a matching profile in lxd)")
    parser.add_argument("stage", nargs="?", default="master", help="deploy stage (default: master)")
    args = parser.parse_args()

    # for each server associated with the given project...
    for server in projects[args.project]:
        # creates a lxd container named {server}-{project}-{stage}
        commandline = template.format(args.command, server, args.project, args.stage, args.project)
        sp = subprocess.Popen(commandline, shell=True, stdout=sys.stdout, stderr=sys.stderr)
        sp.wait()
