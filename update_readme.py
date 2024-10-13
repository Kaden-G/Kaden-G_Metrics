import datetime
import requests
import os
from collections import defaultdict

# GitHub username and token for authentication
GITHUB_USERNAME = "Kaden"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Get the token from environment variables

# Headers for authentication
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Fetch repositories information
repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
response = requests.get(repos_url, headers=headers)

# Check the response and handle errors
if response.status_code == 200:
    repos_data = response.json()
else:
    print(f"Failed to fetch repository data. Status code: {response.status_code}")
    print(f"Response content: {response.text}")
    repos_data = []

# Initialize language data storage
language_data = defaultdict(int)

# Fetch languages for each repository if repositories were fetched successfully
if repos_data:
    for repo in repos_data:
        repo_name = repo['name']
        languages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
        lang_response = requests.get(languages_url, headers=headers)

        if lang_response.status_code == 200:
            lang_data = lang_response.json()
            for language, size in lang_data.items():
                language_data[language] += size
        else:
            print(f"Failed to fetch languages for repository {repo_name}. Status code: {lang_response.status_code}")

# Calculate total code size and language percentages
total_size = sum(language_data.values())
language_percentages = {}

for language, size in language_data.items():
    language_percentages[language] = (size / total_size) * 100 if total_size > 0 else 0

# Create language summary string
language_summary = "\n".join([f"{language}: {percentage:.2f}%" for language, percentage in language_percentages.items()])

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
