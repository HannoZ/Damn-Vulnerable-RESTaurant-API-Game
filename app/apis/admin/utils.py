import subprocess

def get_disk_usage(parameters: str):

    # Use a list for the command instead of a string
    command = ['df', '-h', parameters]
    
    try:
        result = subprocess.check_output(command, shell=False)
        usage = result.stdout.strip().decode()
    except:
        raise Exception("An unexpected error was observed")

    return usage
