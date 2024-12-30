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
    def __init__(self, proxmox_ip, proxmox_node_name, vm_id, vm_ip):
        self.proxmox_ip = proxmox_ip
        self.proxmox_node_name = proxmox_node_name
        self.vm_id = vm_id
        self.vm_ip = vm_ip
        self.prox = None


    def IsPortOpen(self, max_retries):
        return connect_to_port(self.vm_ip, 8080, max_retries=max_retries)
    

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


    def StatusVm(self):
        try:
            vmStatus = self.prox.nodes(self.proxmox_node_name).qemu(self.vm_id).status.current.get()
        except ResourceException as e:
            return "doesnotexist"
        return vmStatus["status"]
    

    def StartVm(self):
        task = self.prox.nodes(self.proxmox_node_name).qemu(self.vm_id).status.start.post()
        if not self._waitForTask(task):
            print(f"Start failed")    


    def StopVm(self):
        task = self.prox.nodes(self.proxmox_node_name).qemu(self.vm_id).status.stop.post()
        if not self._waitForTask(task):
            print(f"Stop failed")


    def RevertVm(self):
        task = self.prox.nodes(self.proxmox_node_name).qemu(self.vm_id).snapshot("base").rollback.post()
        if not self._waitForTask(task):
            print(f"Rollback to snapshot failed")
            

    def SnapshotExists(self):
        snapshots = self.prox.nodes(self.proxmox_node_name).qemu(self.vm_id).snapshot.get()
        snapshot_exists = any(snapshot['name'] == 'base' for snapshot in snapshots)
        return snapshot_exists


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


    def _waitForTask(self, rollback_task, max_tries=10):
        if not rollback_task:
            return True
        if 'taskid' not in rollback_task:
            return True
        
        task_id = rollback_task['taskid']
        tries = 0
        while True:
            if tries == max_tries:
                print(f"Rollback to snapshot failed")
                return False
            
            task_status = self.prox.nodes(self.proxmox_node_name).tasks(task_id).status.get()
            
            if task_status['status'] == 'stopped':
                if task_status['exitstatus'] == 'OK':
                    return True
                else:
                    return False
            tries += 1
            time.sleep(1)