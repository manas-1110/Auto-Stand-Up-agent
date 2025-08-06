# Auto Stand-Up Report Generator

A modern, industry-level Python tool and web interface that automatically generates stand-up reports by analyzing GitHub activity using AI.

## Features

-   📊 **GitHub Activity Analysis**: Fetches commits, pull requests, and other activity data
-   🤖 **AI-Powered Insights**: Uses LLM AI to analyze and summarize work
-   📝 **Structured Reports**: Generates professional stand-up reports
-   🔐 **Private Repository Support**: Works with private repos using GitHub tokens
-   ⚙️ **Configurable**: Easily customize analysis periods and target repositories
-   🎨 **Modern Web UI**: Clean, responsive design with professional styling
-   ⏱️ **Real-time Validation**: Validate GitHub repositories before analysis
-   📈 **Progress Tracking**: Visual progress indicators during report generation
-   📤 **Export Options**: Copy to clipboard or download as text file
-   🩺 **Health Monitoring**: System status indicator for configuration health
-   💾 **Auto-save**: Automatically saves form inputs to localStorage

## Quick Start

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Set Environment Variables**:
   Create a `.env` file with:

    ```
    GITHUB_TOKEN=your_github_token_here
    GOOGLE_API_KEY=your_google_api_key_here
    ```

3. **Run the Web Application**:

    ```bash
    python app.py
    ```

4. **Open Browser**:
   Navigate to `http://localhost:5000`

## Usage

### Web Interface

1. **Configure Repository**: Enter the GitHub repository owner and name
2. **Validate Repository**: Click "Validate Repository" to verify access
3. **Set Analysis Parameters**: Choose username and time period
4. **Generate Report**: Click "Generate Report" to create the stand-up report
5. **Export Results**: Copy to clipboard or download as a file

### Command Line

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

## File Structure

```
├── app.py                 # Flask web application
├── main.py                # Core analysis logic
├── github.py              # GitHub API integration
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   │   └── style.css      # Modern styling
│   └── js/
│       └── app.js         # Frontend JavaScript
└── requirements.txt       # Python dependencies
```

## API Endpoints (Web UI)

-   `GET /` - Main dashboard
-   `POST /api/generate-report` - Generate stand-up report
-   `POST /api/validate-repo` - Validate GitHub repository
-   `GET /api/health` - System health check

## Configuration

-   **Host/Port**: Modify in `app.py` (default: localhost:5000)
-   **Debug Mode**: Enable/disable in `WebConfig` class
-   **Analysis Period**: 1-30 days supported
-   **Form Auto-save**: Automatically enabled

## GitHub Token Permissions

For **public repositories**:

-   `public_repo` scope

For **private repositories**:

-   `repo` scope (full access)

## Output Format

The tool generates structured reports with:

-   **Work Completed**: Key accomplishments and tasks
-   **Impact & Value**: Business/technical value delivered
-   **Collaboration**: PRs, reviews, team interactions
-   **Productivity Insights**: Activity patterns and trends

## Error Handling

The tool includes comprehensive error handling for:

-   Missing environment variables
-   GitHub API rate limits
-   Network connectivity issues
-   Invalid repository/user names

## Technologies Used

-   **Backend**: Flask (Python web framework)
-   **Frontend**: Vanilla JavaScript, CSS3, HTML5
-   **Icons**: Font Awesome
-   **Fonts**: Inter (Google Fonts)
-   **AI Integration**: Google Generative AI
-   **GitHub API**: REST API v3

## Browser Support

-   Chrome 80+
-   Firefox 75+
-   Safari 13+
-   Edge 80+

## Development

For development with auto-reload:

```bash
export FLASK_ENV=development
python app.py
```

## Production Deployment

For production deployment, consider:

1. Use a production WSGI server (e.g., Gunicorn)
2. Set up proper environment variable management
3. Configure reverse proxy (e.g., Nginx)
4. Enable HTTPS
5. Set up monitoring and logging

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
