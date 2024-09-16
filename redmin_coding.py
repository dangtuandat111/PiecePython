import requests
import json
from datetime import datetime, timedelta

# Cấu hình cơ bản
REDMINE_URL = 'https://redmine.vti.com.vn'
API_KEY = ''
API_ENDPOINT = f'{REDMINE_URL}/time_entries.json'

# Thông tin cập nhật
issue_id = 272407
hours = 7.5

# Ngày bắt đầu và ngày kết thúc
start_date = datetime.strptime('2024-09-21', '%Y-%m-%d')
end_date = datetime.strptime('2024-09-30', '%Y-%m-%d')

# Ngày cần loại trừ
excluded_start = datetime.strptime('2024-09-01', '%Y-%m-%d')
excluded_end = datetime.strptime('2024-09-03', '%Y-%m-%d')

# Danh sách thông tin comments và activity_id
info_list = [
    {"comments": "Coding", "activity_id": 9},
    {"comments": "Fix bug", "activity_id": 39},
    {"comments": "UT + Fix bug", "activity_id": 22},
    {"comments": "Review + Merge code", "activity_id": 38}
]


# Hàm gửi yêu cầu API để cập nhật thời gian
def update_time_entry(date, comments, activity_id):
    data = {
        "time_entry": {
            "issue_id": issue_id,
            "hours": hours,
            "activity_id": activity_id,
            "comments": comments,
            "spent_on": date.strftime('%Y-%m-%d')  # Ngày tiêu tốn
        }
    }

    response = requests.post(
        API_ENDPOINT,
        headers={
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': API_KEY
        },
        data=json.dumps(data)
    )

    if response.status_code == 201:
        print(f"Updated {date.strftime('%Y-%m-%d')} successfully.")
    else:
        print(f"Failed to update {date.strftime('%Y-%m-%d')}. Response: {response.text}")


# Lặp qua từng ngày trong khoảng thời gian
current_date = start_date
index = 0  # Chỉ số cho danh sách thông tin

while current_date <= end_date:
    # Kiểm tra nếu ngày không phải là thứ 7 hoặc chủ nhật và không nằm trong khoảng loại trừ
    if current_date.weekday() < 5 and not (excluded_start <= current_date <= excluded_end):
        info = info_list[index]
        update_time_entry(current_date, info["comments"], info["activity_id"])

        # Cập nhật chỉ số cho thông tin
        index = (index + 1) % len(info_list)

    current_date += timedelta(days=1)
