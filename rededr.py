import requests
import json


class RedEdrApi:
    def __init__(self, rededr_ip):
        self.rededr_url = "http://" + rededr_ip + ":8080"


    def StartTrace(self, target_name):
        url = self.rededr_url + "/api/trace"
        headers = {"Content-Type": "application/json"}
        payload = {"trace": target_name}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("Response:", response.json())
                return True
            else:
                print("Error:", response.status_code, response.json())
                return False
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False
        
    
    def StopTrace(self):
        pass


    def ExecFile(self, filename, file_data):
        url = self.rededr_url + "/api/exec"
        files = {
            "file": (filename, file_data)
        }
        # multipart form-data
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("Response:", response.json())
            return True
        else:
            print("Error:", response.status_code, response.text)
            return False
        

    def GetJsonResult(self):
        url = self.rededr_url + "/api/events"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print("Error:", response.status_code, response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
