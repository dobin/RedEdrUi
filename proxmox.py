from proxmoxer import ProxmoxAPI, ResourceException
import socket
import time


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
    def __init__(self, proxmox_ip, proxmox_node_name, template_id, new_vm_id, new_vm_name, rededr_ip):
        self.proxmox_ip = proxmox_ip
        self.proxmox_node_name = proxmox_node_name
        self.template_id = template_id
        self.new_vm_id = new_vm_id
        self.new_vm_name = new_vm_name
        self.rededr_ip = rededr_ip
        self.prox = None


    def IsPortOpen(self, max_retries):
        return connect_to_port(self.rededr_ip, 8080, max_retries=max_retries)
    

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
        self.prox.nodes(self.proxmox_node_name).qemu(self.template_id).clone.create(
            newid=self.new_vm_id,
            name=self.new_vm_name,
        )


    def StatusVm(self):
        try:
            vmStatus = self.prox.nodes(self.proxmox_node_name).qemu(self.new_vm_id).status.current.get()
        except ResourceException as e:
            return "doesnotexist"
        return vmStatus["status"]
    

    def StartVm(self):
        self.prox.nodes(self.proxmox_node_name).qemu(self.new_vm_id).status.start.post()
    

    def StopVm(self):
        self.prox.nodes(self.proxmox_node_name).qemu(self.new_vm_id).status.stop.post()


    def DeleteVm(self):
        self.prox.nodes(self.proxmox_node_name).qemu(self.new_vm_id).delete()


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

