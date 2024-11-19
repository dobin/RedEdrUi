import requests

def query_lm_studio(prompt, url="http://localhost:55444/v1/chat/completions"):
    try:
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "qwen2.5-32b-instruct",
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def read_recording_file(name) -> str:
    try:
        with open("data/" + name + ".events.json", "r") as f:
            data = f.read()

            # Remove the hooking message from the recording as it confused LLM's
            data = data.replace("hooking", "")

            return data
    except FileNotFoundError:
        return b""
    except PermissionError:
        return b""


if __name__ == "__main__":
    user_prompt = """You are a SOC analyst reviewing a JSON recording of malware events
recorded by an EDR, which was gathered by injecting a trusted RedEdrDll.dll DLL into the process and hooking ntdll.dll, plus ETW and kernel events.
In that event JSON data appended below, are there any indications of shellcode execution, process injection or similar techniques?"""
    recording_data = read_recording_file("examplemalware-1")
    answer = query_lm_studio(user_prompt + "\n\n" + recording_data) 
    print("Model response:", answer)