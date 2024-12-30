from flask import Flask, jsonify, request, render_template
from threading import Thread
import queue
import time
import random
import os
import shutil
import yaml
import string

import proxmox
import rededr
import filesystem

app = Flask(__name__)

# REST:
# curl.exe -X POST http://127.0.0.1:5000/create_job
#   curl.exe -X POST http://localhost:5000/create_job -F "file=@C:\tools\procexp64.exe"
# curl.exe http://127.0.0.1:5000/job_status/123
# curl.exe http://127.0.0.1:5000/jobs
# 

UPLOAD_FOLDER = 'uploads'

proxmoxApi = None
rededrApi = None
filesystemApi = filesystem.FilesystemApi(UPLOAD_FOLDER)

execution_time = 10  # seconds


class Job:
    def __init__(self, job_id, filename):
        self.job_id = job_id
        self.status = "Created"
        self.filename = filename


# Queue to hold jobs
job_queue = queue.Queue()

# In-memory dictionary to store jobs by ID
jobs = {}

config = {}


def load_config(file_path):
    global config
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/create_job', methods=['POST'])
def create_job():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        fname = filesystemApi.WriteBinary(file.filename, file.read())

        job_id = random.randint(1, 100000)  # Generate a random job ID for simplicity
        new_job = Job(job_id, fname)
        jobs[job_id] = new_job

        # Add job to queue for processing
        job_queue.put(new_job)

        return jsonify({'message': 'Job created', 'job_id': job_id, 'file': file.filename}), 201


@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    all_jobs = [{'job_id': job.job_id, 'status': job.status } for job in jobs.values()]
    return jsonify(all_jobs)


@app.route('/job_status/<int:job_id>', methods=['GET'])
def get_job_status(job_id):
    job = jobs.get(job_id)
    if job:
        return jsonify({'job_id': job.job_id, 'status': job.status })
    else:
        return jsonify({'message': 'Job not found'}), 404
    

@app.route('/result', methods=['GET'])
def get_results():
    files = filesystemApi.ListResult()
    return jsonify(files)


@app.route('/result/<fname>', methods=['GET'])
def get_result(fname):
    data = filesystemApi.ReadResult(fname)
    return data


def DoJob(job):
    job.status = "In Progress"
    print(f"Proxmox: Processing job {job.job_id}")

    do_start = True
    do_rededr = False
    do_revert = True

    if do_start:
        print("InstanceVM: Initial Status: " + proxmoxApi.StatusVm())

        # VM & Snapshot exists?
        if proxmoxApi.StatusVm() == "doesnotexist":
            print("InstanceVM: Does not exist? Pls create :-(")
            return
        if not proxmoxApi.SnapshotExists():
            print("InstanceVM: Snapshot does not exist? Pls create :-(")
            return

        # Start VM
        proxmoxApi.StartVm()
        proxmoxApi.WaitForVmStatus("started")
        print("InstanceVM: Started: " + proxmoxApi.StatusVm())

        # Wait for booted
        #   17s on LAN proxmox
        isPortOpen = proxmoxApi.IsPortOpen(max_retries=60)  # will block
        if isPortOpen:
            print("InstanceVM: Port is reachable")

    if do_rededr:
        rededrApi.StartTrace(job.filename)
        file_data = filesystemApi.ReadBinary(job.filename)
        rededrApi.ExecFile(job.filename, file_data)
        time.sleep(execution_time)  # give it 10s time to execute
        rededrApi.StopTrace()
        jsonResult = rededrApi.GetJsonResult()
        filesystemApi.WriteResult(job.filename, jsonResult)

    if do_revert:
        # Stop VM
        proxmoxApi.StopVm()
        proxmoxApi.WaitForVmStatus("stopped")
        print("InstanceVM: Shutdown: " + proxmoxApi.StatusVm())

        # Revert VM
        proxmoxApi.RevertVm()
        print("InstanceVM: Reverted: " + proxmoxApi.StatusVm())

    
    job.status = "Completed"

    print(f"Job {job.job_id} completed")


def process_jobs():
    while True:
        # Wait and take a job from the queue
        job = job_queue.get()
        if job:
            DoJob(job)


if __name__ == '__main__':
    # Prepare upload folder
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Prepare config
    if not os.path.exists("config.yaml"):
        shutil.copy("config.yaml.init", "config.yaml")
    load_config('config.yaml')

    rededrApi = rededr.RedEdrApi(config['proxmox_ip'])
    proxmoxApi = proxmox.ProxmoxApi(
        config['proxmox_ip'],
        config['proxmox_node_name'],
        config['vm_id'],
        config['vm_ip'],
    )
    proxmoxApi.Connect(config['proxmox_ip'], config['user'], config['password'])

    if False:
        # Prepare worker thread
        worker_thread = Thread(target=process_jobs, daemon=True)
        worker_thread.start()
        app.run(debug=True, threaded=True)  # Flask runs in multi-threaded mode
    else:
        job  = Job(1, "test")
        DoJob(job)