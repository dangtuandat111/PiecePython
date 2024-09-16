import subprocess
import requests
import time

# Thay đổi các giá trị sau đây cho phù hợp
WATCHED_BRANCH = 'TEST_NOTIFY, vti_dev2'  # Thay đổi nhánh mà bạn muốn theo dõi
NOTIFICATION_URL = 'https://chat.googleapis.com/v1/spaces/AAAAUhcjgN0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=9eWqxSACARUu7MZb8gIt8mqQILctO7FdcfwyJbIfHHY'  # URL của webhook nơi bạn muốn gửi thông báo

def get_last_commit_sha(branch):
    result = subprocess.run(['git', 'rev-parse', branch], capture_output=True, text=True)
    return result.stdout.strip()

def notify_commit(commit_message):
    message = {"text": f"New commit on branch {WATCHED_BRANCH}: {commit_message}"}
    response = requests.post(NOTIFICATION_URL, json=message)
    if response.status_code != 200:
        print(f"Failed to send notification: {response.status_code} {response.text}")

def main():
    last_commit_sha = get_last_commit_sha(WATCHED_BRANCH)

    while True:
        time.sleep(60)  # Thay đổi thời gian nếu cần
        subprocess.run(['git', 'fetch'])
        new_commit_sha = get_last_commit_sha(WATCHED_BRANCH)

        if new_commit_sha != last_commit_sha:
            # Có commit mới, gửi thông báo
            result = subprocess.run(['git', 'log', '--oneline', f'{last_commit_sha}..{new_commit_sha}'], capture_output=True, text=True)
            commit_message = result.stdout.strip()
            notify_commit(commit_message)
            last_commit_sha = new_commit_sha

if __name__ == '__main__':
    main()
