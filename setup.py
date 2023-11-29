"""
SETUP WORKING VENV FOR PYTHON PROJECT
* Require: Git and Python installed
1: Create and active vitural environment
2: Install packages from requirements.txt
3: Run the main code file eventually
"""

import os
import sys
import subprocess

def is_git_installed():
    try:
        # Attempt to run the git command
        subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_installation_directory():
    try:
        # Run the git command to get the path
        result = subprocess.run(['git', '--exec-path'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


# Check if Git is installed
if is_git_installed():
    # Get Git installation directory
    git_folder_name = "Git"
    sh_exe_folder_name = "bin" # parent folder of sh.exe

    git_exec_path = get_git_installation_directory()
    git_path = git_exec_path[:git_exec_path.find(git_folder_name) + len(git_folder_name)]
    git_bin_path = os.path.join(git_path, sh_exe_folder_name)

    # Get the current PATH variable
    current_path = os.environ.get('PATH', '')

    # Append the bin folder to the PATH variable to enable execution of shell script in sh file
    new_path_variable = f'{current_path};{git_bin_path}'

    # Update the PATH variable
    os.environ['PATH'] = new_path_variable

    script_path = os.path.join(os.path.dirname(__file__), 'setup.sh')
    python_exe_path = sys.executable
    main_src_path = os.path.join("src", "main.py")
    subprocess.run(['sh', script_path, python_exe_path, main_src_path])
else:
    print('Git is not installed on this system.')
