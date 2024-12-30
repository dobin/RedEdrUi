from proxmoxer import ProxmoxAPI, ResourceException
import socket
import time

node_name = "proxmox"
template_id = 201  # win10hckc

new_vm_id = 202
new_vm_ip = "192.168.88.105"
new_vm_name = "win10hckct"


def connect_to_port(host, port, max_retries=30):
    retries = 0
    while retries < max_retries:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, port))
            print(f"Connection after {retries}s")
            return True
        except (socket.error, ConnectionRefusedError) as e:
            retries += 1
            print(f"Connection attempt {retries} failed: {e}")
            if retries < max_retries:
                continue
            else:
                return False
        finally:
            sock.close()


class ProxmoxApi:
    def __init__(self):
        self.prox = None


    def IsPortOpen(self, max_retries):
        return connect_to_port(new_vm_ip, 3389, max_retries=max_retries)
    

    def WaitForVmStatus(self, status, timeout=5):
        n = 0
        while self.StatusVm() != status:
            if n == timeout:
                print("Wait Failed")
                return False
            time.sleep(1)
            n += 1


    def Connect(self, ip, user, password):
        self.prox = ProxmoxAPI(ip, user=user, password=password, verify_ssl=False)


    def CloneVm(self): 
        self.prox.nodes(node_name).qemu(template_id).clone.create(
            newid=new_vm_id,
            name=new_vm_name,
        )


    def StatusVm(self):
        try:
            vmStatus = self.prox.nodes(node_name).qemu(new_vm_id).status.current.get()
        except ResourceException as e:
            return "doesnotexist"
        return vmStatus["status"]
    

    def StartVm(self):
        self.prox.nodes(node_name).qemu(new_vm_id).status.start.post()
    

    def StopVm(self):
        self.prox.nodes(node_name).qemu(new_vm_id).status.stop.post()


    def DeleteVm(self):
        self.prox.nodes(node_name).qemu(new_vm_id).delete()


    def PrintStatus(self):
        print("Status: " + self.StatusVm())


    def Print(self):
        print("Nodes:")
        print(self.prox.nodes.get())

        print("VMs:")
        print(self.prox.nodes('proxmox').qemu.get())

        print("VM:")
        vmStatus = self.prox.nodes('proxmox').qemu(201).status.current.get()
        print("Status: " + vmStatus["status"])

