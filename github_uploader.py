import os
import sys
import requests
import json
from datetime import datetime
from getpass import getpass

class GitHubUploader:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = None
        self.username = None
        
    def authenticate(self):
        """Authenticate with GitHub using personal access token"""
        print("=== GitHub Authentication ===")
        self.username = input("Enter your GitHub username: ")
        self.token = getpass("Enter your GitHub personal access token: ")
        
        # Test authentication
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(f"{self.base_url}/user", headers=headers)
            if response.status_code == 200:
                print("✓ Authentication successful!")
                return True
            else:
                print("⨯ Authentication failed. Please check your credentials.")
                return False
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            return False

    def create_repository(self, repo_name, description="", private=False):
        """Create a new repository on GitHub"""
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": True
        }
        
        try:
            response = requests.post(f"{self.base_url}/user/repos", headers=headers, json=data)
            if response.status_code == 201:
                print(f"✓ Repository '{repo_name}' created successfully!")
                return response.json()['clone_url']
            else:
                print(f"⨯ Failed to create repository. Status code: {response.status_code}")
                print(response.json())
                return None
        except Exception as e:
            print(f"Error creating repository: {str(e)}")
            return None

    def initialize_git_and_push(self, local_path, repo_url):
        """Initialize git repository and push to GitHub"""
        try:
            # Change to project directory
            os.chdir(local_path)
            
            # Initialize git repository if not already initialized
            if not os.path.exists('.git'):
                os.system('git init')
            
            # Configure git credentials
            os.system(f'git config user.name "{self.username}"')
            
            # Add all files
            os.system('git add .')
            
            # Create initial commit
            commit_message = f"Initial commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            os.system(f'git commit -m "{commit_message}"')
            
            # Add remote and push
            os.system(f'git remote add origin {repo_url}')
            os.system('git push -u origin master')
            
            print("✓ Project successfully uploaded to GitHub!")
            return True
        except Exception as e:
            print(f"Error during git operations: {str(e)}")
            return False

def main():
    print("=== GitHub Project Uploader ===")
    print("This script will help you upload your project to GitHub")
    
    # Initialize uploader
    uploader = GitHubUploader()
    
    # Authenticate
    if not uploader.authenticate():
        sys.exit(1)
    
    # Get project details
    project_path = input("Enter the full path to your project: ")
    repo_name = input("Enter the desired repository name: ")
    description = input("Enter repository description (optional): ")
    is_private = input("Make repository private? (y/n): ").lower() == 'y'
    
    # Create repository
    repo_url = uploader.create_repository(repo_name, description, is_private)
    if not repo_url:
        sys.exit(1)
    
    # Upload project
    if uploader.initialize_git_and_push(project_path, repo_url):
        print("\nProject Upload Summary:")
        print(f"Repository Name: {repo_name}")
        print(f"Repository URL: {repo_url}")
        print(f"Access: {'Private' if is_private else 'Public'}")
        print("\nDone! Your project is now on GitHub!")
    else:
        print("Failed to upload project. Please check the errors above.")

if __name__ == "__main__":
    main()