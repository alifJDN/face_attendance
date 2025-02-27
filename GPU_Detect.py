import subprocess
import csv
import io

def get_non_nvidia_gpus():
    try:
        output = subprocess.check_output('wmic path Win32_VideoController get Name,VideoMemory,DriverVersion,Status /format:csv', shell=True)
    except subprocess.CalledProcessError:
        return []
    
    # Decode the output to string
    csv_data = output.strip().decode()
    
    # Use StringIO to treat the string as a file
    csv_file = io.StringIO(csv_data)
    
    # Read the CSV file
    reader = csv.reader(csv_file)
    
    # Skip the first row (headers)
    next(reader)
    
    non_nvidia_gpus = []
    for row in reader:
        name = row[0]
        if "NVIDIA" not in name.upper():
            non_nvidia_gpus.append(row)
    return non_nvidia_gpus

def print_gpu_specs(gpu):
    name = gpu[0]
    try:
        video_memory = int(gpu[1]) / (1024 * 1024 * 1024)
    except (ValueError, IndexError):
        video_memory = "N/A"
    driver_version = gpu[2] if len(gpu) > 2 else "N/A"
    status = gpu[3] if len(gpu) > 3 else "N/A"
    
    print(f"Name: {name}")
    print(f"Video Memory: {video_memory:.2f} GB" if video_memory != "N/A" else "Video Memory: N/A")
    print(f"Driver Version: {driver_version}")
    print(f"Status: {status}")
    print("")

gpus = get_non_nvidia_gpus()
if gpus:
    print("Non-NVIDIA GPUs detected with their specs: ")
    for gpu in gpus:
        print_gpu_specs(gpu)
else:
    print("No non-NVIDIA GPUs detected.")