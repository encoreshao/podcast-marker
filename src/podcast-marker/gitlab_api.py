from dotenv import load_dotenv
import requests
import urllib.parse
import os
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_URL = os.getenv('GITLAB_URL')
PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')

def get_project_id(project_path):
    """
    Retrieve the numeric project ID for a given GitLab project path.

    Args:
        project_path (str): The GitLab project path (e.g., 'namespace/project').

    Returns:
        int or None: The project ID if found, otherwise None.
    """
    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f'{GITLAB_URL}/api/v4/projects/{encoded_path}'
    headers = {'Authorization': f'Bearer {GITLAB_TOKEN}'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        project_data = response.json()
        return project_data['id']
    except requests.exceptions.RequestException as e:
        print(f"Error finding project ID: {e}")
        return None


def fetch_gitlab_issues(days_to_backtrack=1):
    """
    Fetch issues from the configured GitLab project, including recent comments within the specified backtrack window.

    Args:
        days_to_backtrack (int): Number of days to look back for recent comments (default: 1).

    Returns:
        list: List of issue dicts, each with recent comments and label names, or None on error.
    """
    if not GITLAB_TOKEN or not PROJECT_ID:
        raise ValueError("GITLAB_TOKEN and GITLAB_PROJECT_ID must be set in .env file")

    updated_after = datetime.now() - timedelta(days=days_to_backtrack)
    url = f'{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues'
    params = {
        'scope': 'all',
        'order_by': 'updated_at',
        'sort': 'desc',
        'per_page': 100
    }
    headers = {'Authorization': f'Bearer {GITLAB_TOKEN}'}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        all_issues = response.json()
        recent_issues = []
        for issue in all_issues:
            comments_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues/{issue['iid']}/notes"
            comments_response = requests.get(comments_url, headers=headers)
            if comments_response.status_code == 200:
                comments = comments_response.json()
                recent_comments = [
                    comment for comment in comments
                    if datetime.strptime(comment['created_at'][:19], '%Y-%m-%dT%H:%M:%S') > updated_after
                ]
                if recent_comments:
                    issue['recent_comments'] = recent_comments
                    labels = issue.get('labels', [])
                    if labels and isinstance(labels[0], dict):
                        issue['label_names'] = [label['name'] for label in labels]
                    else:
                        issue['label_names'] = labels
                    recent_issues.append(issue)
        return recent_issues
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues: {e}")
        return None