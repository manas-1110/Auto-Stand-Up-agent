import requests
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import dotenv

# Load environment variables
dotenv.load_dotenv()

class GitHubConfig:
    """Configuration class for GitHub API settings"""
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.api_url = 'https://api.github.com'
        self.per_page = 100
        self.max_commits = 500  # Limit commits to avoid too much data
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
    
    @property
    def headers(self):
        return {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

class GitHubAnalyzer:
    """GitHub repository analyzer for user activity"""
    
    def __init__(self, config: GitHubConfig):
        self.config = config

    
    def get_user_pull_requests(self, owner: str, repo: str, username: str) -> List[Dict]:
        """Get all pull requests by a specific user in a repository"""
        url = f"{self.config.api_url}/repos/{owner}/{repo}/pulls"
        params = {'state': 'all', 'per_page': self.config.per_page}
        
        all_prs = []
        page = 1
        
        while True:
            params['page'] = page
            try:
                resp = requests.get(url, headers=self.config.headers, params=params)
                resp.raise_for_status()
                
                data = resp.json()
                if not data:
                    break
                    
                # Filter PRs by the target user
                user_prs = [pr for pr in data if pr['user']['login'].lower() == username.lower()]
                all_prs.extend(user_prs)
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching pull requests: {e}")
                break
                
        return all_prs
    
    def get_user_commits(self, owner: str, repo: str, username: str, since_days: int = 30) -> List[Dict]:
        """Get commits by a specific user in a repository"""
        url = f"{self.config.api_url}/repos/{owner}/{repo}/commits"
        
        # Calculate date range
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        
        params = {
            'author': username,
            'per_page': self.config.per_page,
            'since': since_date
        }
        
        all_commits = []
        page = 1
        
        while True:
            params['page'] = page
            try:
                resp = requests.get(url, headers=self.config.headers, params=params)
                resp.raise_for_status()
                
                data = resp.json()
                if not data or len(all_commits) >= self.config.max_commits:
                    break
                    
                all_commits.extend(data)
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching commits: {e}")
                break
                
        return all_commits[:self.config.max_commits]
    
    def get_user_activity_summary(self, owner: str, repo: str, username: str, since_days: int = 30) -> Dict:
        """Get comprehensive user activity summary"""
        print(f"Fetching activity for {username} in {owner}/{repo}...")
        
        # Get pull requests
        prs = self.get_user_pull_requests(owner, repo, username)
        
        # Get commits
        commits = self.get_user_commits(owner, repo, username, since_days)
        
        # Organize data
        activity_summary = {
            'user': username,
            'repository': f"{owner}/{repo}",
            'period_days': since_days,
            'pull_requests': {
                'total': len(prs),
                'open': len([pr for pr in prs if pr['state'] == 'open']),
                'closed': len([pr for pr in prs if pr['state'] == 'closed']),
                'merged': len([pr for pr in prs if pr.get('merged_at')]),
                'details': prs
            },
            'commits': {
                'total': len(commits),
                'details': commits
            }
        }
        
        return activity_summary
    
    def format_activity_for_llm(self, activity_summary: Dict) -> str:
        """Format activity summary for LLM analysis"""
        user = activity_summary['user']
        repo = activity_summary['repository']
        period = activity_summary['period_days']
        
        output = []
        output.append(f"GitHub Activity Report for {user} in {repo} (Last {period} days)")
        output.append("=" * 60)
        
        # Pull Requests Summary
        pr_data = activity_summary['pull_requests']
        output.append(f"\nPULL REQUESTS SUMMARY:")
        output.append(f"Total PRs: {pr_data['total']}")
        output.append(f"Open: {pr_data['open']}, Closed: {pr_data['closed']}, Merged: {pr_data['merged']}")
        
        if pr_data['details']:
            output.append(f"\nPULL REQUESTS DETAILS:")
            for pr in pr_data['details'][:10]:  # Limit to 10 most recent
                state_info = f"({pr['state']}"
                if pr.get('merged_at'):
                    state_info += ", merged"
                state_info += ")"
                output.append(f"• PR #{pr['number']}: {pr['title']} {state_info}")
                output.append(f"  Created: {pr['created_at'][:10]}")
        
        # Commits Summary
        commit_data = activity_summary['commits']
        output.append(f"\nCOMMITS SUMMARY:")
        output.append(f"Total Commits: {commit_data['total']}")
        
        if commit_data['details']:
            output.append(f"\nCOMMIT DETAILS:")
            for commit in commit_data['details'][:20]:  # Limit to 20 most recent
                sha = commit['sha'][:7]
                message = commit['commit']['message'].split('\n')[0]  # First line only
                date = commit['commit']['author']['date'][:10]
                output.append(f"• {sha}: {message} ({date})")
        
        return '\n'.join(output)

def get_user_activity_report(owner: str, repo: str, username: str, since_days: int = 30) -> str:
    """
    Main function to get user activity report from GitHub
    """
    try:
        config = GitHubConfig()
        analyzer = GitHubAnalyzer(config)
        
        # Get activity summary
        activity_summary = analyzer.get_user_activity_summary(owner, repo, username, since_days)
        
        # Format for LLM
        formatted_report = analyzer.format_activity_for_llm(activity_summary)
        
        return formatted_report
        
    except Exception as e:
        return f"Error generating activity report: {str(e)}"

if __name__ == "__main__":
    # Demo configuration
    REPO_OWNER = 'manas-1110'
    REPO_NAME = 'fighting_game'
    TARGET_USER = 'manas-1110'
    SINCE_DAYS = 30
    
    report = get_user_activity_report(REPO_OWNER, REPO_NAME, TARGET_USER, SINCE_DAYS)
    print(report)