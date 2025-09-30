#!/usr/bin/env python3
"""
SableAI GitHub Repository Initialization Script
Automated GitHub repository creation and setup
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    print("🔍 Checking if git is installed...")
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install git first.")
        return False

def init_git_repo():
    """Initialize git repository"""
    print("📦 Initializing git repository...")
    
    # Initialize git repository
    if not run_command("git init", "Initializing git repository"):
        return False
    
    # Add all files
    if not run_command("git add .", "Adding all files to git"):
        return False
    
    # Create initial commit
    if not run_command('git commit -m "Initial commit: ScypherAI Pine Script to Python Backtesting Framework"', "Creating initial commit"):
        return False
    
    return True

def create_github_repo():
    """Create GitHub repository (requires GitHub CLI)"""
    print("🐙 Creating GitHub repository...")
    
    # Check if GitHub CLI is installed
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        print("✅ GitHub CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI is not installed. Please install it from https://cli.github.com/")
        print("📝 You can also create the repository manually on GitHub.com")
        return False
    
    # Create repository
    if not run_command("gh repo create SableAI --public --description 'Pine Script to Python Backtesting Framework with Domain-Driven Design'", "Creating GitHub repository"):
        return False
    
    # Add remote origin
    if not run_command("git remote add origin https://github.com/$(gh api user --jq .login)/SableAI.git", "Adding remote origin"):
        return False
    
    # Push to GitHub
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        return False
    
    return True

def create_github_workflows():
    """Create GitHub Actions workflows"""
    print("⚙️ Creating GitHub Actions workflows...")
    
    # Create .github/workflows directory
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Create CI/CD workflow
    ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libta-lib-dev
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_system.py
    
    - name: Run linting
      run: |
        pip install black flake8 mypy
        black --check .
        flake8 .
        mypy .
"""
    
    with open(".github/workflows/ci.yml", "w") as f:
        f.write(ci_workflow)
    
    # Create release workflow
    release_workflow = """name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m twine upload dist/*
"""
    
    with open(".github/workflows/release.yml", "w") as f:
        f.write(release_workflow)
    
    print("✅ Created GitHub Actions workflows")
    return True

def create_contributing_guide():
    """Create contributing guide"""
    print("📝 Creating contributing guide...")
    
    contributing_content = """# Contributing to ScypherAI

Thank you for your interest in contributing to ScypherAI! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ScypherAI.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `python test_system.py`

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused

### Testing
- Write tests for new features
- Ensure all tests pass before submitting
- Use descriptive test names

### Documentation
- Update README.md for significant changes
- Add docstrings to new functions
- Update type hints as needed

## 🔄 Pull Request Process

1. Ensure your code follows the style guidelines
2. Run all tests and ensure they pass
3. Update documentation if needed
4. Submit a pull request with a clear description
5. Respond to feedback and make necessary changes

## 🐛 Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## 💡 Feature Requests

For feature requests, please:
- Describe the feature clearly
- Explain the use case
- Consider the impact on existing functionality
- Provide examples if possible

## 📄 License

By contributing to ScypherAI, you agree that your contributions will be licensed under the MIT License.

## 🎉 Thank You

Thank you for contributing to ScypherAI! Your contributions help make this project better for everyone.
"""
    
    with open("CONTRIBUTING.md", "w") as f:
        f.write(contributing_content)
    
    print("✅ Created contributing guide")
    return True

def create_issue_templates():
    """Create GitHub issue templates"""
    print("📋 Creating issue templates...")
    
    # Create .github/ISSUE_TEMPLATE directory
    os.makedirs(".github/ISSUE_TEMPLATE", exist_ok=True)
    
    # Bug report template
    bug_report = """---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the Bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows, macOS, Linux]
 - Python Version: [e.g. 3.8, 3.9, 3.10]
 - ScypherAI Version: [e.g. 1.0.0]

**Additional Context**
Add any other context about the problem here.
"""
    
    with open(".github/ISSUE_TEMPLATE/bug_report.md", "w") as f:
        f.write(bug_report)
    
    # Feature request template
    feature_request = """---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
"""
    
    with open(".github/ISSUE_TEMPLATE/feature_request.md", "w") as f:
        f.write(feature_request)
    
    print("✅ Created issue templates")
    return True

def main():
    """Main function"""
    print("🚀 SableAI GitHub Repository Initialization")
    print("=" * 60)
    
    # Check if git is installed
    if not check_git_installed():
        sys.exit(1)
    
    # Initialize git repository
    if not init_git_repo():
        print("❌ Failed to initialize git repository")
        sys.exit(1)
    
    # Create GitHub repository
    if not create_github_repo():
        print("⚠️  Failed to create GitHub repository automatically")
        print("📝 Please create the repository manually on GitHub.com")
        print("🔗 Repository URL: https://github.com/yourusername/ScypherAI")
    
    # Create GitHub workflows
    if not create_github_workflows():
        print("⚠️  Failed to create GitHub workflows")
    
    # Create contributing guide
    if not create_contributing_guide():
        print("⚠️  Failed to create contributing guide")
    
    # Create issue templates
    if not create_issue_templates():
        print("⚠️  Failed to create issue templates")
    
    print("\n🎉 SableAI GitHub repository setup completed!")
    print("=" * 60)
    print("📚 Next steps:")
    print("1. Push your changes: git push -u origin main")
    print("2. Set up GitHub Actions secrets if needed")
    print("3. Configure branch protection rules")
    print("4. Add collaborators if needed")
    print("\n🚀 Happy coding!")

if __name__ == "__main__":
    main()
