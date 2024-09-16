import requests

# Thay đổi các biến này theo nhu cầu của bạn
GITHUB_TOKEN = ''
REPO_OWNER = 'en-japan'
REPO_NAME = 'engage-user'
USERS = ['datdangtuan-vti', 'hoang-duongduc', 'huongtrinhthi', 'NguyenDucDuyVti', 'quanphamanhd5', 'thangtranxuan-vti',
         'tungnguyenthanh1-vti', 'VTIDungnguyenquoc', 'VTINguyenHaTrang', 'thanhlexuand5', 'tiennguyenvtid5', 'VTI-Tuanphamvan']
OUTPUT_FILE = 'xxx.txt'

def get_pull_requests(owner, repo, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {token}'}
    all_prs = []
    page = 1
    start_page = page
    per_page = 100

    try:
        while True and page <= start_page + 29:
            print(page)
            params = {
                'page': page,
                'per_page': per_page,
                'state': 'all',
                'sort': 'created'
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Nếu có lỗi trong yêu cầu, nó sẽ ném ngoại lệ
            prs = response.json()

            if not prs:
                break

            all_prs.extend(prs)
            page += 1
    except Exception as err:
        print(err)

    return all_prs


def get_comments(owner, repo, pr_number, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def filter_prs(prs, users, token):
    filtered_prs = []
    for pr in prs:
        if pr['user']['login'] in users:
            pr_number = pr['number']
            comments = get_comments(REPO_OWNER, REPO_NAME, pr_number, token)
            if comments:
                filtered_prs.append(pr)
    return filtered_prs

def write_prs_to_txt(prs, filename):
    with open(filename, 'w') as file:
        file.write("List Pull Request Links\n")
        file.write("="*80 + "\n")
        for pr in prs:
            file.write(f"{pr['html_url']}\n\n")


def main():
    prs = get_pull_requests(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    filtered_prs = filter_prs(prs, USERS, GITHUB_TOKEN)

    print(f"Found {len(filtered_prs)} PRs created by users {USERS} with comments.")
    write_prs_to_txt(filtered_prs, OUTPUT_FILE)
    for pr in filtered_prs:
        print(f"PR #{pr['number']}: {pr['title']} by {pr['user']['login']}")


if __name__ == '__main__':
    main()
