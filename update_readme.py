import datetime
import requests
import os
from collections import defaultdict

# GitHub username and token for authentication
GITHUB_USERNAME = "Kaden-G"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("PAT_TOKEN")  # Get the PAT from environment variables

# Check if GITHUB_TOKEN is available
if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN environment variable is not set.")
    exit(1)

# Headers for authentication
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_all_repos(username, headers):
    repos = []
    page = 1
    per_page = 100
    while True:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        print(f"Fetching repositories from {repos_url}")
        response = requests.get(repos_url, headers=headers)
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            print(f"Fetched {len(page_repos)} repositories from page {page}.")
            page += 1
        else:
            print(f"Failed to fetch repository data. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            break
    return repos

def fetch_languages(repo_name, headers):
    languages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
    print(f"Fetching languages for repository: {repo_name}")
    lang_response = requests.get(languages_url, headers=headers)
    if lang_response.status_code == 200:
        lang_data = lang_response.json()
        print(f"Languages for {repo_name}: {lang_data}")
        return lang_data
    else:
        print(f"Failed to fetch languages for repository {repo_name}. Status code: {lang_response.status_code}")
        print(f"Response content: {lang_response.text}")
        return {}

def main():
    # Check API rate limits
    rate_limit_url = "https://api.github.com/rate_limit"
    rate_response = requests.get(rate_limit_url, headers=headers)
    if rate_response.status_code == 200:
        rate_data = rate_response.json()
        remaining = rate_data['resources']['core']['remaining']
        reset_time = datetime.datetime.fromtimestamp(rate_data['resources']['core']['reset'])
        print(f"API Rate Limit: {remaining} requests remaining. Resets at {reset_time}.")
        if remaining < 10:
            print("Warning: Approaching API rate limit.")
    else:
        print(f"Failed to fetch rate limit status. Status code: {rate_response.status_code}")
        print(f"Response content: {rate_response.text}")

    # Fetch repositories
    repos_data = fetch_all_repos(GITHUB_USERNAME, headers)
    print(f"Total repositories fetched: {len(repos_data)}")

    # Initialize language data storage
    language_data = defaultdict(int)

    # Fetch languages in parallel to optimize API calls
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_repo = {executor.submit(fetch_languages, repo['name'], headers): repo for repo in repos_data}
        for future in concurrent.futures.as_completed(future_to_repo):
            repo = future_to_repo[future]
            lang_data = future.result()
            for language, size in lang_data.items():
                language_data[language] += size

    # Calculate total code size and language percentages
    total_size = sum(language_data.values())
    print(f"Total code size: {total_size} bytes")
    language_percentages = {}

    for language, size in language_data.items():
        language_percentages[language] = (size / total_size) * 100 if total_size > 0 else 0
        print(f"Language: {language}, Percentage: {language_percentages[language]:.2f}%")

    # Create language summary table
    language_summary = "| Language | Percentage |\n| --- | ---: |\n"
    for language, percentage in language_percentages.items():
        language_summary += f"| {language} | {percentage:.2f}% |\n"

    # Update README.md file with a timestamp to ensure changes
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
```bash
Kaden Fetch
------------
Location: Bay Area, CA

Last Updated: {current_time}

GitHub Stats
------------
Repositories: {len(repos_data)}
Stars Received: {sum(repo.get('stargazers_count', 0) for repo in repos_data)}

Languages Used
--------------
{language_summary}

Programming Languages
----------------------
- Python
- Java
- HTML
- CSS

Favorite Technologies
----------------------
- AWS
- Django
- GitHub Actions
- Linux
- Flask (for lightweight web applications)
- Docker (for containerization)
- PostgreSQL (as a relational database)
- VS Code (as a preferred IDE)

Contact Information
--------------------
Email: kaden@example.com
LinkedIn: https://linkedin.com/in/kaden
"""
