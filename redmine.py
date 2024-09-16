import requests
import json
from datetime import datetime, timedelta

# Cấu hình cơ bản
REDMINE_URL = 'https://redmine.vti.com.vn'
API_KEY = ''
API_ENDPOINT = f'{REDMINE_URL}/time_entries.json'

# Thông tin cập nhật
issue_id = 272415
hours = 0.5
activity_id = 30
comments = 'Daily meeting'

# Ngày bắt đầu và ngày kết thúc
start_date = datetime.strptime('2024-09-04', '%Y-%m-%d')
end_date = datetime.strptime('2024-09-30', '%Y-%m-%d')


# Hàm gửi yêu cầu API để cập nhật thời gian
def update_time_entry(date):
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
while current_date <= end_date:
    # Kiểm tra nếu ngày không phải là thứ 7 hoặc chủ nhật
    if current_date.weekday() < 5:
        update_time_entry(current_date)
    current_date += timedelta(days=1)
