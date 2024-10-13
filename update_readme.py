import datetime
import requests
import os
from collections import defaultdict

# GitHub username and token for authentication
GITHUB_USERNAME = "Kaden"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("GH_PAT")  # Get the token from environment variables

# Headers for authentication
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Fetch repositories information
repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
response = requests.get(repos_url, headers=headers)
repos_data = response.json()

# Initialize language data storage
language_data = defaultdict(int)

if response.status_code == 200:
    for repo in repos_data:
        repo_name = repo['name']
        languages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
        lang_response = requests.get(languages_url, headers=headers)
        
        if lang_response.status_code == 200:
            lang_data = lang_response.json()
            for language, size in lang_data.items():
                language_data[language] += size
else:
    print("Failed to fetch repository data")

# Calculate total code size and language percentages
total_size = sum(language_data.values())
language_percentages = {}

for language, size in language_data.items():
    language_percentages[language] = (size / total_size) * 100 if total_size > 0 else 0

# Create language summary string
language_summary = "\n".join([f"{language}: {percentage:.2f}%" for language, percentage in language_percentages.items()])

# Update README.md file
readme_content = f"""
```bash
Kaden Fetch
------------
Location: Bay Area, CA

GitHub Stats
------------
Repositories: {len(repos_data)}
Stars Received: {sum(repo['stargazers_count'] for repo in repos_data)}

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
