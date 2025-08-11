import subprocess
import json

def check_cpu_usage_and_temperature():
    try:
        cpu_usage_result = subprocess.run(
            ["top", "-l", "1", "-s", "0"],
            capture_output=True, text=True, timeout=30
        )
        temperature_result = subprocess.run(
            ["sudo", "powermetrics", "--samplers", "smc", "-n", "1", "--hide-cpu-duty-cycle"],
            capture_output=True, text=True, timeout=30
        )

        if cpu_usage_result.returncode == 0 and temperature_result.returncode == 0:
            return {
                "status": "success",
                "message": "CPU usage and temperature retrieved successfully",
                "data": {
                    "cpu_usage": cpu_usage_result.stdout.strip(),
                    "temperature": temperature_result.stdout.strip()
                }
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve CPU usage or temperature",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def check_memory_usage():
    try:
        memory_result = subprocess.run(
            ["vm_stat"],
            capture_output=True, text=True, timeout=30
        )

        if memory_result.returncode == 0:
            return {
                "status": "success",
                "message": "Memory usage retrieved successfully",
                "data": memory_result.stdout.strip()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve memory usage",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def check_disk_space():
    try:
        disk_result = subprocess.run(
            ["df", "-h"],
            capture_output=True, text=True, timeout=30
        )

        if disk_result.returncode == 0:
            return {
                "status": "success",
                "message": "Disk space retrieved successfully",
                "data": disk_result.stdout.strip()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve disk space",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def check_battery_status():
    try:
        battery_result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True, text=True, timeout=30
        )

        if battery_result.returncode == 0:
            return {
                "status": "success",
                "message": "Battery status retrieved successfully",
                "data": battery_result.stdout.strip()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve battery status",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def list_running_processes():
    try:
        processes_result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True, timeout=30
        )

        if processes_result.returncode == 0:
            return {
                "status": "success",
                "message": "Running processes retrieved successfully",
                "data": processes_result.stdout.strip()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve running processes",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def get_system_uptime_and_load():
    try:
        uptime_result = subprocess.run(
            ["uptime"],
            capture_output=True, text=True, timeout=30
        )

        if uptime_result.returncode == 0:
            return {
                "status": "success",
                "message": "System uptime and load averages retrieved successfully",
                "data": uptime_result.stdout.strip()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to retrieve system uptime and load averages",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "data": None
        }

def main():
    return {
        "cpu": check_cpu_usage_and_temperature(),
        "memory": check_memory_usage(),
        "disk": check_disk_space(),
        "battery": check_battery_status(),
        "processes": list_running_processes(),
        "uptime": get_system_uptime_and_load()
    }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
