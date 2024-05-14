import subprocess
import shlex

def get_disk_usage(parameters: str):

    # Use shlex.quote to safely create a string that can be used as one token in a shell command
    safe_user_input = shlex.quote(parameters)

    command = f'df -h {safe_user_input}'
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        usage = result.stdout.strip().decode()
    except:
        raise Exception("An unexpected error was observed")

    return usage
