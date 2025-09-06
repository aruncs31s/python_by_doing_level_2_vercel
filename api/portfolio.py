from http.server import BaseHTTPRequestHandler
import json
import requests
import subprocess
from urllib.parse import urlparse
import os

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            # Parse the URL
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/is_complete':
                self.send_json_response({"result": True})
                return
            
            # Default to homepage
            portfolio = self.get_portfolio_data()
            html_content = self.render_html_template(portfolio)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, error_msg):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Server Error</h1>
            <p>{error_msg}</p>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode())
    
    def get_portfolio_data(self):
        # Load data from files
        data = self.load_data()
        username = data.get("username", "aruncs31s")
        
        # Get GitHub data
        name = self.get_git_name()
        email = self.get_git_email(username)
        bio = self.get_github_bio(username)
        repos = self.get_github_repos(username)
        
        return {
            "name": name,
            "title": "Python Developer",
            "bio": bio,
            "about": data.get("about", "Just a developer with laptop"),
            "avatar": f"https://github.com/{username}.png",
            "github_username": username,
            "skills": ["Python", "Flask", "JavaScript", "HTML", "CSS"],
            "projects": repos,
            "experience": data.get("experience", []),
            "email": email,
            "github": f"https://github.com/{username}",
            "linkedin": f"https://linkedin.com/in/{username}",
            "website": f"https://{username}.github.io"
        }
    
    def load_data(self):
        try:
            # Try to find data.json in various locations
            possible_paths = ['data.json', '../data.json', './data.json']
            for path in possible_paths:
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
    
    def get_git_name(self):
        try:
            result = subprocess.run(["git", "config", "--get", "user.name"], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() or "Developer"
        except:
            return "Developer"
    
    def get_git_email(self, username):
        try:
            result = subprocess.run(["git", "config", "--get", "user.email"], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() or f"{username}@github.com"
        except:
            return f"{username}@github.com"
    
    def get_github_bio(self, username):
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            response = requests.get(f"https://api.github.com/users/{username}", 
                                  headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get('bio', 'Python Developer')
        except:
            pass
        return "Python Developer"
    
    def get_github_repos(self, username):
        try:
            # Try to load from repos.json first
            possible_paths = ['repos.json', '../repos.json', './repos.json']
            for path in possible_paths:
                try:
                    with open(path, 'r') as f:
                        return json.load(f)
                except FileNotFoundError:
                    continue
            
            # Fallback to API call
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            response = requests.get(f"https://api.github.com/users/{username}/repos", 
                                  headers=headers, timeout=10)
            if response.status_code == 200:
                repos = response.json()
                return [{"name": repo["name"], 
                        "description": repo.get("description", ""),
                        "tech": []} for repo in repos[:6]]
        except:
            pass
        
        return [{"name": "Sample Project", 
                "description": "A sample project", 
                "tech": ["Python", "Flask"]}]
    
    def render_html_template(self, portfolio):
        # Simple HTML template with GitHub Dark theme
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{portfolio['name']} - Portfolio</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #f0f6fc;
                    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .header {{
                    text-align: center;
                    color: #f0f6fc;
                    padding: 60px 0;
                }}
                
                .profile-photo {{
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    border: 5px solid #58a6ff;
                    box-shadow: 0 10px 30px rgba(13,17,23,0.5);
                    margin: 0 auto 30px;
                    display: block;
                    object-fit: cover;
                    transition: transform 0.3s ease;
                }}
                
                .profile-photo:hover {{
                    transform: scale(1.05);
                }}
                
                .header h1 {{
                    font-size: 3.5rem;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(13,17,23,0.5);
                    color: #58a6ff;
                }}
                
                .header h2 {{
                    font-size: 1.8rem;
                    font-weight: 300;
                    margin-bottom: 20px;
                    opacity: 0.9;
                    color: #79c0ff;
                }}
                
                .header p {{
                    font-size: 1.2rem;
                    max-width: 600px;
                    margin: 0 auto;
                    opacity: 0.8;
                    color: #8b949e;
                }}
                
                .content {{
                    background: #21262d;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(13,17,23,0.3);
                    padding: 40px;
                    margin-top: 40px;
                }}
                
                .section {{
                    margin-bottom: 40px;
                }}
                
                .section h3 {{
                    color: #58a6ff;
                    font-size: 2rem;
                    margin-bottom: 20px;
                    border-bottom: 3px solid #58a6ff;
                    padding-bottom: 10px;
                }}
                
                .projects-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 25px;
                    margin-top: 20px;
                }}
                
                .project-card {{
                    background: #30363d;
                    border-radius: 10px;
                    padding: 25px;
                    border-left: 5px solid #f78166;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                
                .project-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(13,17,23,0.4);
                    background: #282e33;
                }}
                
                .project-card h4 {{
                    color: #f0f6fc;
                    font-size: 1.3rem;
                    margin-bottom: 10px;
                }}
                
                .project-card p {{
                    color: #c9d1d9;
                    line-height: 1.5;
                }}
                
                .skills {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-top: 20px;
                }}
                
                .skill-tag {{
                    background: #388bfd;
                    color: #ffffff;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    font-weight: 500;
                }}
                
                .contact {{
                    background: #238636;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 30px;
                    text-align: center;
                }}
                
                .contact h3 {{
                    color: #ffffff;
                    border-bottom: 3px solid #ffffff;
                }}
                
                .contact-links {{
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 20px;
                    flex-wrap: wrap;
                }}
                
                .contact-link {{
                    background: rgba(255,255,255,0.15);
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 25px;
                    text-decoration: none;
                    transition: background 0.3s ease;
                    border: 2px solid rgba(255,255,255,0.3);
                }}
                
                .contact-link:hover {{
                    background: rgba(255,255,255,0.25);
                }}
                
                @media (max-width: 768px) {{
                    .header h1 {{
                        font-size: 2.5rem;
                    }}
                    
                    .header h2 {{
                        font-size: 1.4rem;
                    }}
                    
                    .profile-photo {{
                        width: 120px;
                        height: 120px;
                        margin-bottom: 20px;
                    }}
                    
                    .content {{
                        padding: 20px;
                        margin-top: 20px;
                    }}
                    
                    .projects-grid {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .contact-links {{
                        flex-direction: column;
                        align-items: center;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header Section -->
                <header class="header">
                    <img src="{portfolio['avatar']}" alt="{portfolio['name']}" class="profile-photo">
                    <h1>{portfolio['name']}</h1>
                    <h2>{portfolio['title']}</h2>
                    <p>{portfolio['bio']}</p>
                </header>
                
                <!-- Main Content -->
                <main class="content">
                    <!-- About Section -->
                    <section class="section">
                        <h3>About Me</h3>
                        <p>{portfolio['about']}</p>
                    </section>
                    
                    <!-- Skills Section -->
                    <section class="section">
                        <h3>Skills</h3>
                        <div class="skills">
                            {''.join([f'<span class="skill-tag">{skill}</span>' for skill in portfolio['skills']])}
                        </div>
                    </section>
                    
                    <!-- Projects Section -->
                    <section class="section">
                        <h3>Projects</h3>
                        <div class="projects-grid">
                            {''.join([f'''
                            <div class="project-card">
                                <h4>{project['name']}</h4>
                                <p>{project['description']}</p>
                                <div class="skills" style="margin-top: 15px;">
                                    {''.join([f'<span class="skill-tag" style="background: #a5f3fc; color: #0f172a;">{tech}</span>' for tech in project.get('tech', [])])}
                                </div>
                            </div>
                            ''' for project in portfolio['projects']])}
                        </div>
                    </section>
                    
                    <!-- Experience Section -->
                    {'<section class="section"><h3>Experience</h3>' + ''.join([f'''<div class="project-card" style="margin-bottom: 20px;"><h4>{exp['position']} at {exp['company']}</h4><p style="color: #58a6ff; font-weight: bold;">{exp['duration']}</p><p>{exp['description']}</p></div>''' for exp in portfolio['experience']]) + '</section>' if portfolio['experience'] else ''}
                    
                    <!-- Contact Section -->
                    <section class="section">
                        <div class="contact">
                            <h3>Get In Touch</h3>
                            <p>I'm always open to discussing new opportunities and interesting projects.</p>
                            <div class="contact-links">
                                <a href="mailto:{portfolio['email']}" class="contact-link">Email</a>
                                <a href="{portfolio['github']}" class="contact-link" target="_blank">GitHub</a>
                                <a href="{portfolio['linkedin']}" class="contact-link" target="_blank">LinkedIn</a>
                                <a href="{portfolio['website']}" class="contact-link" target="_blank">Website</a>
                            </div>
                        </div>
                    </section>
                </main>
            </div>
        </body>
        </html>
        """
