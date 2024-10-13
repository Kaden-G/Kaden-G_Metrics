import datetime
import requests
import os

# GitHub username and token for authentication
GITHUB_USERNAME = "Kaden"  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv("GH_PAT")  # Get the token from environment variables

# Get age calculation
birth_date = datetime.datetime(1987, 6, 15)  # Replace with your birth date
today = datetime.datetime.now()
age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Fetch GitHub statistics
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Get repositories information
repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
response = requests.get(repos_url, headers=headers)
repos_data = response.json()

if response.status_code == 200:
    num_repos = len(repos_data)
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
else:
    num_repos = 0
    total_stars = 0

# TODO: Get commit data (requires more sophisticated API use due to rate limits and authentication requirements)
total_commits = "N/A"  # Leave as "N/A" for now since commit counting involves a more complex approach

# Update README.md file
with open("README.md", "w") as readme_file:
    readme_content = f"""
