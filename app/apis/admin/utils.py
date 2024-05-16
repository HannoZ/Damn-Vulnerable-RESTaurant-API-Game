import subprocess

def get_disk_usage(parameters: str):

    # Use a list for the command instead of a string
    command = ["df", "-h"]
    
    if parameters:
        command.append(parameters.split())

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        usage = result.stdout.strip().decode()
    except:
        raise Exception("An unexpected error was observed")

    return usage
