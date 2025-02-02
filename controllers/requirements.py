import os
import subprocess

import docker
from rich.console import Console

console = Console()


class Requirements:
    def __init__(self) -> None:
        pass

    def checkAll(self):
        console.print("[bold green]Checking Requirements[/]")
        self.checkCurl()
        self.checkJq()
        self.checkDocker()
        self.checkHLFBinaries()
        self.checkDomainFolder()

    def checkCurl(self):
        console.print("[bold white]# Checking cURL[/]")
        rc = subprocess.call(
            ["which", "curl"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        if rc != 0:
            console.print("[bold red]> cURL isn't installed. Please install it.[/]")
            exit(0)

    def checkJq(self):
        console.print("[bold white]# Checking jq[/]")
        rc = subprocess.call(
            ["which", "jq"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        if rc != 0:
            console.print("[bold red]> jq isn't installed. Please install it.[/]")
            exit(0)

    def checkDocker(self):
        console.print("[bold white]# Checking Docker[/]")
        try:
            client = docker.DockerClient(base_url="unix://var/run/docker.sock")
            client.ping()
        except:
            console.print(
                "[bold red]> Docker isn't installed or running. Please install and run it.[/]"
            )
            exit(0)

    def checkHLFBinaries(self):
        console.print("[bold white]# Checking HLF binaries[/]")

        pathbin = "bin"
        isFolderBinExist = os.path.exists(pathbin)

        pathbuilder = "builders"
        isFolderBuilderExist = os.path.exists(pathbuilder)

        pathconfig = "config"
        isFolderConfigExist = os.path.exists(pathconfig)

        if (
            (isFolderBinExist == False)
            or (isFolderBuilderExist == False)
            or (isFolderConfigExist == False)
        ):
            console.print(
                "[bold yellow]> Please wait for HLF binaries downloading and installing.[/]"
            )

            os.system(
                "curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && chmod +x install-fabric.sh"
            )
            os.system("./install-fabric.sh binary")

        console.print("[bold green]All requirements gathered.[/]")
        console.print("")

    def checkDomainFolder(self):
        pathdomains = "domains"
        isFolderDomainsExist = os.path.exists(pathdomains)

        if not isFolderDomainsExist:
            os.mkdir(pathdomains)
