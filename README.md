# Auto Stand-Up Agent

A Python tool that automatically generates stand-up reports by analyzing GitHub activity using AI.

## Features

- 📊 **GitHub Activity Analysis**: Fetches commits, pull requests, and other activity data
- 🤖 **AI-Powered Insights**: Uses LLM AI to analyze and summarize work
- 📝 **Structured Reports**: Generates professional stand-up reports
- 🔐 **Private Repository Support**: Works with private repos using GitHub tokens
- ⚙️ **Configurable**: Easily customize analysis periods and target repositories

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

- **GITHUB_TOKEN**: Get from [GitHub Settings &gt; Developer settings &gt; Personal access tokens](https://github.com/settings/tokens)
- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://ai.google.dev/)

### 3. Configuration

Edit the configuration variables in `main.py`:

```python
REPO_OWNER = 'your-username'     # GitHub username or organization
REPO_NAME = 'your-repository'    # Repository name
TARGET_USER = 'username'         # User to analyze
ANALYSIS_DAYS = 7               # Days to analyze (default: 7)
```

## Usage

### Basic Usage

```bash
python main.py
```

### Programmatic Usage

```python
from main import StandupAnalyzer, AIConfig
from github import get_user_activity_report

# Initialize
ai_config = AIConfig()
analyzer = StandupAnalyzer(ai_config)

# Generate report
report = analyzer.generate_standup_report(
    repo_owner="owner",
    repo_name="repo",
    username="user",
    days=7
)
print(report)
```

## GitHub Token Permissions

For **public repositories**:

- `public_repo` scope

For **private repositories**:

- `repo` scope (full access)

## Output Format

The tool generates structured reports with:

- **Work Completed**: Key accomplishments and tasks
- **Impact & Value**: Business/technical value delivered
- **Collaboration**: PRs, reviews, team interactions
- **Productivity Insights**: Activity patterns and trends


## Error Handling

The tool includes comprehensive error handling for:

- Missing environment variables
- GitHub API rate limits
- Network connectivity issues
- Invalid repository/user names

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
