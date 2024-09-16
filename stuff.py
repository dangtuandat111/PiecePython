import os
import subprocess
import requests
import re
import logging


def monitor_branches(request):
    """Cloud Function entry point."""
    try:
        # Fetch environment variables
        REPO_URL = os.getenv('REPO_URL')
        BRANCH_PATTERN = r'^ma*'
        NOTIFICATION_URL = os.getenv('NOTIFICATION_URL')
        TMP_DIR = '/tmp/repo'

        # Setup SSH key
        ssh_key = os.getenv('SSH_PRIVATE_KEY')
        if not ssh_key:
            raise ValueError("SSH_PRIVATE_KEY environment variable is not set.")

        ssh_dir = '/root/.ssh'
        os.makedirs(ssh_dir, exist_ok=True)

        key_path = f'{ssh_dir}/id_rsa'
        with open(key_path, 'w') as key_file:
            key_file.write(ssh_key)

        os.chmod(key_path, 0o600)

        config_path = f'{ssh_dir}/config'
        with open(config_path, 'w') as config_file:
            config_file.write("Host github.com\n  StrictHostKeyChecking no\n")

        # Clone the repository
        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)

        if not os.path.exists(os.path.join(TMP_DIR, '.git')):
            subprocess.run(['git', 'clone', REPO_URL, TMP_DIR])

        # Run a Git command
        def run_git_command(command):
            result = subprocess.run(command, cwd=TMP_DIR, capture_output=True, text=True)
            return result.stdout.strip()

        # Get branches matching the pattern
        def get_branches_matching_pattern(pattern):
            output = run_git_command(['git', 'branch', '--list'])
            branches = output.splitlines()
            matching_branches = [branch.strip() for branch in branches if re.match(pattern, branch.strip())]
            return matching_branches

        # Get the SHA of the last commit on the branch
        def get_last_commit_sha(branch):
            return run_git_command(['git', 'rev-parse', branch])

        # Send a notification to a webhook
        def notify_commit(branch, commit_message):
            message = {"text": f"New commits on branch {branch}:\n{commit_message}"}
            response = requests.post(NOTIFICATION_URL, json=message)
            if response.status_code != 200:
                logging.error(f"Failed to send notification: {response.status_code} {response.text}")

        # Read the last commit SHA from a file
        def read_last_commit_sha(branch):
            filename = f'/tmp/last_commit_{branch}.txt'
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    return file.read().strip()
            else:
                # Create the file with an empty SHA if it doesn't exist
                with open(filename, 'w') as file:
                    file.write('')
                return ''

        # Write the last commit SHA to a file
        def write_last_commit_sha(branch, commit_sha):
            filename = f'/tmp/last_commit_{branch}.txt'
            with open(filename, 'w') as file:
                file.write(commit_sha)

        # Main checking logic
        branches = get_branches_matching_pattern(BRANCH_PATTERN)
        for branch in branches:
            logging.info(f"1")
            logging.info(f"Checking branch: {branch}\n")
            logging.info(f"2")

            last_commit_sha = read_last_commit_sha(branch)
            logging.info(f"Checking last_commit_sha: {last_commit_sha}\n")
            current_commit_sha = get_last_commit_sha(branch)
            logging.info(f"Checking current_commit_sha: {current_commit_sha}\n")

            if last_commit_sha != current_commit_sha:
                output = run_git_command(['git', 'log', '--oneline', f'{last_commit_sha}..{current_commit_sha}'])
                commit_message = output.strip()
                if commit_message:
                    notify_commit(branch, commit_message)
                else:
                    notify_commit(branch, 'NONE CHANGES')

                write_last_commit_sha(branch, current_commit_sha)
            else:
                notify_commit(branch, 'NONE CHANGES')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 'Failed to check branches', 500

    response = branches
    return response, 200, {'Content-Type': 'text/plain'}
