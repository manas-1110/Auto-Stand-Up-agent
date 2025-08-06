from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import sys
import json
from datetime import datetime
from main import AIConfig, StandupAnalyzer
from github import get_user_activity_report

app = Flask(__name__)
app.secret_key = os.urandom(24)

class WebConfig:
    """Configuration for web application"""
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5000
        self.debug = True

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """API endpoint to generate standup report"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['repo_owner', 'repo_name', 'username', 'days']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        repo_owner = data['repo_owner']
        repo_name = data['repo_name']
        username = data['username']
        days = int(data['days'])
        
        # Validate days range
        if days < 1 or days > 30:
            return jsonify({
                'success': False,
                'error': 'Days must be between 1 and 30'
            }), 400
        
        # Initialize analyzer
        ai_config = AIConfig()
        analyzer = StandupAnalyzer(ai_config)
        
        # Generate report
        report = analyzer.generate_standup_report(repo_owner, repo_name, username, days)
        
        if report.startswith("Error"):
            return jsonify({
                'success': False,
                'error': report
            }), 500
        
        return jsonify({
            'success': True,
            'report': report,
            'metadata': {
                'repo_owner': repo_owner,
                'repo_name': repo_name,
                'username': username,
                'days': days,
                'generated_at': datetime.now().isoformat()
            }
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Configuration error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/api/validate-repo', methods=['POST'])
def validate_repo():
    """API endpoint to validate if repository exists"""
    try:
        data = request.get_json()
        repo_owner = data.get('repo_owner')
        repo_name = data.get('repo_name')
        
        if not repo_owner or not repo_name:
            return jsonify({
                'success': False,
                'error': 'Repository owner and name are required'
            }), 400
        
        # Simple validation by trying to fetch basic repo info
        import requests
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return jsonify({
                'success': False,
                'error': 'GitHub token not configured'
            }), 500
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            return jsonify({
                'success': True,
                'repo_info': {
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description', ''),
                    'language': repo_data.get('language', 'Unknown'),
                    'stars': repo_data['stargazers_count'],
                    'forks': repo_data['forks_count']
                }
            })
        elif response.status_code == 404:
            return jsonify({
                'success': False,
                'error': 'Repository not found or not accessible'
            }), 404
        else:
            return jsonify({
                'success': False,
                'error': f'GitHub API error: {response.status_code}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error validating repository: {str(e)}'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if required environment variables are set
        github_token = os.getenv('GITHUB_TOKEN')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        return jsonify({
            'status': 'healthy',
            'github_configured': bool(github_token),
            'ai_configured': bool(google_api_key),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    config = WebConfig()
    print(f"Starting Auto Stand-Up Report Generator...")
    print(f"Access the application at: http://{config.host}:{config.port}")
    
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )
