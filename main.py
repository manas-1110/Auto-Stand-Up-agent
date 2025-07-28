import os
import sys
import google.generativeai as genai
from github import get_user_activity_report
import dotenv

# Load environment variables
dotenv.load_dotenv()

class AIConfig:
    """Configuration for AI/LLM settings"""
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.model_name = 'gemini-1.5-flash'
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

class StandupAnalyzer:
    """Main class for analyzing GitHub activity and generating standup reports"""
    
    def __init__(self, ai_config: AIConfig):
        self.ai_config = ai_config
        genai.configure(api_key=self.ai_config.google_api_key)
        self.model = genai.GenerativeModel(self.ai_config.model_name)
    
    def get_system_prompt(self) -> str:
        """Enhanced system prompt for better analysis"""
        return """You are an expert software development analyst and standup report generator. 

Your task is to analyze GitHub activity data and create a concise, professional standup report.

**Analysis Guidelines:**
1. Focus on meaningful contributions and progress
2. Categorize work into logical groups (features, bugs, refactoring, etc.)
3. Highlight impact and business value
4. Note collaboration patterns (PRs, reviews)
5. Identify productivity trends

**Output Format:**
Generate a structured report with these sections:

**WORK COMPLETED:**
- List key accomplishments with brief descriptions
- Group similar tasks together
- Mention notable commits or PRs

**IMPACT & VALUE:**
- Highlight business/technical value delivered
- Note any performance improvements or bug fixes

**COLLABORATION:**
- Mention PRs created/reviewed
- Note team interactions

**PRODUCTIVITY INSIGHTS:**
- Overall activity level
- Code quality indicators
- Development patterns

Keep the tone professional but conversational, suitable for team standups.
Limit the response to 100-200 words maximum."""
    
    def analyze_github_activity(self, github_data: str) -> str:
        """Analyze GitHub activity data using LLM"""
        try:
            system_prompt = self.get_system_prompt()
            
            user_prompt = f"""
Please analyze the following GitHub activity data and generate a standup report:

{github_data}

Focus on the work done, impact created, and any notable patterns or insights.
"""
            
            chat = self.model.start_chat(history=[
                {"role": "model", "parts": [{"text": system_prompt}]}
            ])
            
            response = chat.send_message(user_prompt)
            return response.text
            
        except Exception as e:
            return f"Error analyzing GitHub activity: {str(e)}"
    
    def generate_standup_report(self, repo_owner: str, repo_name: str, username: str, days: int = 7) -> str:
        """Generate complete standup report for a user"""
        print(f"Generating standup report for {username} in {repo_owner}/{repo_name} (last {days} days)...")
        
        # Get GitHub activity data
        github_data = get_user_activity_report(repo_owner, repo_name, username, days)
        
        if github_data.startswith("Error"):
            return github_data
        
        # Analyze with AI
        analysis = self.analyze_github_activity(github_data)
        
        return analysis

def main():
    """Main function to run the standup analyzer"""
    # Configuration - you can modify these or make them command line arguments
    REPO_OWNER = 'Owner of the Repo'
    REPO_NAME = 'Name of the Repo'
    TARGET_USER = 'manas-1110'
    ANALYSIS_DAYS = 7
    
    try:
        # Initialize components
        ai_config = AIConfig()
        analyzer = StandupAnalyzer(ai_config)
        
        # Generate report
        report = analyzer.generate_standup_report(
            REPO_OWNER, REPO_NAME, TARGET_USER, ANALYSIS_DAYS
        )
        
        print("\n" + "="*60)
        print("STANDUP REPORT")
        print("="*60)
        print(report)
        print("="*60)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()