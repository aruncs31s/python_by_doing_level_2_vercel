import sys
import os
from flask import Flask, render_template
import json
import requests
import subprocess

app = Flask(__name__, template_folder="../src/templates")

class SimpleGit:
    def __init__(self, username="aruncs31s"):
        self.username = username
    
    @property 
    def name(self):
        try:
            result = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True)
            return result.stdout.strip() or "Developer"
        except:
            return "Developer"
    
    @property
    def github_email(self):
        try:
            result = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True)
            return result.stdout.strip() or f"{self.username}@github.com"
        except:
            return f"{self.username}@github.com"
    
    def get_image_url_github(self):
        return f"https://github.com/{self.username}.png"
    
    def get_github_description(self):
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            response = requests.get(f"https://api.github.com/users/{self.username}", headers=headers)
            if response.status_code == 200:
                return response.json().get('bio', 'Python Developer')
        except:
            pass
        return "Python Developer"
    
    def get_github_repositories(self):
        try:
            headers = {
                "Accept": "application/vnd.github+json", 
                "X-GitHub-Api-Version": "2022-11-28",
            }
            response = requests.get(f"https://api.github.com/users/{self.username}/repos", headers=headers)
            if response.status_code == 200:
                repos = response.json()
                return [{"name": repo["name"], "description": repo.get("description", ""), "tech": []} for repo in repos[:6]]
        except:
            pass
        return [{"name": "Sample Project", "description": "A sample project", "tech": ["Python", "Flask"]}]

def load_data():
    try:
        for path in ['../data.json', 'data.json', './data.json']:
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                continue
    except:
        pass
    return {
        "username": "aruncs31s",
        "about": "Just a developer with laptop",
        "experience": []
    }

@app.route('/')
def go_home():
    data = load_data()
    git = SimpleGit(data.get("username", "aruncs31s"))
    try:
        for path in ['../repos.json', 'repos.json', './repos.json']:
            try:
                with open(path, 'r') as f:
                    github_projects = json.load(f)
                    break
            except FileNotFoundError:
                continue
        else:
            github_projects = git.get_github_repositories()
    except:
        github_projects = git.get_github_repositories()
    
    portfolio = {
        "name": git.name,
        "title": "Python Developer", 
        "bio": git.get_github_description(),
        "about": data.get("about", "Python Developer"),
        "avatar": git.get_image_url_github(),
        "github_username": git.username,
        "skills": ["Python", "Flask", "JavaScript", "HTML", "CSS"],
        "projects": github_projects,
        "experience": data.get("experience", []),
        "email": git.github_email,
        "github": f"https://github.com/{git.username}",
        "linkedin": f"https://linkedin.com/in/{git.username}",
        "website": f"https://{git.username}.github.io"
    }
    return render_template("home.html", portfolio=portfolio)

@app.route('/is_complete')
def is_complete():
    return {"result": True}

# For Vercel
def handler(environ, start_response):
    return app(environ, start_response)
