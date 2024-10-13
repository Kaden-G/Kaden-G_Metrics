import datetime
import requests

# Example user information
GITHUB_USERNAME = "Kaden"  # Replace with your actual GitHub username

# Get age
birth_date = datetime.datetime(1987, 6, 15)  # Replace with your birth date
today = datetime.datetime.now()
age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Fetch GitHub statistics
repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
response = requests.get(repos_url)
repos_data = response.json()

num_repos = len(repos_data)
total_commits = 0  # This would require more in-depth API calls (GitHub API has limitations for commits)
total_stars = sum(repo['stargazers_count'] for repo in repos_data)

# Update README.md file
with open("README.md", "w") as readme_file:
    readme_file.write(f"""
    ```
    Kaden Fetch
    ------------
    Name: Kaden
    Age: {age}
    Repos: {num_repos}
    Stars: {total_stars}
    Commits: Approx. {total_commits}
    ```
    """)
