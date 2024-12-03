import requests
import time

def query_lm_studio(prompt, model, url="http://localhost:55444/v1/chat/completions"):
    try:
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model,
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("  Tokens: ", result.get("usage", {}).get("total_tokens", "n/a"))
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

    models = [
        "mixtral-8x7b-instruct-v0.1"
        "c4ai-command-r-08-2024",
        "meta-llama-3.1-8b-instruct", 
        "qwen2.5-32b-instruct" 
    ]
    names = ["examplemalware-1", 
             "examplemalware-2", 
             "examplemalware-3", 
             "meterpreter-revhttp-staged-noautoload", 
             "meterpreter-revhttp-staged", 
             "meterpreter-revhttp-nonstaged-noautoload", 
             "meterpreter-revhttp-nonstaged-autoload", 
             "notepad"]

    for model in models:
        for name in names:
            print("Handling: {} {}".format(name, model))
            recording_data = read_recording_file(name)
            # measure time 
            
            start_time = time.time()
            answer = query_lm_studio(user_prompt + "\n\n" + recording_data, model)
            end_time = time.time()
            t = int(end_time - start_time)
            print("  Time elapsed: ", t)

            #print("Model response:", answer)

            # write results
            result_filename = "data/" + name + "." + model + ".llm.txt"
            print("  Writing to: " + result_filename)
            with open(result_filename, "w") as f:
                f.write(answer)

