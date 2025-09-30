#!/usr/bin/env python3
"""
SableAI Installation Script
Automated installation and setup for the Pine Script to Python Backtesting Framework
"""

import os
import sys
import subprocess
import platform
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

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    
    # Install core requirements
    if not run_command("pip install -r requirements.txt", "Installing core requirements"):
        return False
    
    # Install TA-Lib (platform specific)
    system = platform.system().lower()
    if system == "windows":
        print("🪟 Installing TA-Lib for Windows...")
        run_command("pip install TA-Lib", "Installing TA-Lib")
    elif system == "darwin":  # macOS
        print("🍎 Installing TA-Lib for macOS...")
        run_command("brew install ta-lib", "Installing TA-Lib via Homebrew")
        run_command("pip install TA-Lib", "Installing TA-Lib Python package")
    elif system == "linux":
        print("🐧 Installing TA-Lib for Linux...")
        run_command("sudo apt-get update", "Updating package list")
        run_command("sudo apt-get install -y libta-lib-dev", "Installing TA-Lib development files")
        run_command("pip install TA-Lib", "Installing TA-Lib Python package")
    
    return True

def setup_optional_integrations():
    """Setup optional integrations"""
    print("🔧 Setting up optional integrations...")
    
    # OpenBB integration
    print("📊 Setting up OpenBB integration...")
    run_command("pip install openbb", "Installing OpenBB")
    
    # Cipher-BT integration
    print("🔄 Setting up Cipher-BT integration...")
    run_command("pip install cipher-bt", "Installing Cipher-BT")
    
    # BTA-Lib integration
    print("📈 Setting up BTA-Lib integration...")
    run_command("pip install bta-lib", "Installing BTA-Lib")
    
    # AI integration (OpenAI)
    print("🤖 Setting up AI integration...")
    run_command("pip install openai", "Installing OpenAI")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = [
        "data",
        "results",
        "strategies",
        "logs",
        "backtest_results",
        "strategy_results",
        "generated_strategies"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create environment file template"""
    print("🔐 Creating environment file template...")
    
    env_content = """# SableAI Environment Configuration

# OpenAI API Key (for AI strategy generation)
OPENAI_API_KEY=your-openai-api-key-here

# OpenBB API Key (optional)
OPENBB_API_KEY=your-openbb-api-key-here

# Trading API Keys (optional)
BINANCE_API_KEY=your-binance-api-key-here
BINANCE_SECRET_KEY=your-binance-secret-key-here

# Database Configuration (optional)
DATABASE_URL=sqlite:///scypherai.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/scypherai.log

# Backtesting Configuration
DEFAULT_INITIAL_CAPITAL=10000
DEFAULT_COMMISSION=0.001
DEFAULT_SLIPPAGE=0.0005

# Risk Management
MAX_POSITION_SIZE=0.1
MAX_DAILY_LOSS=0.05
MAX_DRAWDOWN=0.2
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env.example file")
    print("📝 Please copy .env.example to .env and configure your API keys")
    
    return True

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    
    if not run_command("python test_system.py", "Running system tests"):
        print("⚠️  Some tests failed, but installation may still be successful")
        return False
    
    return True

def main():
    """Main installation function"""
    print("🚀 SableAI Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Setup optional integrations
    if not setup_optional_integrations():
        print("⚠️  Some optional integrations failed, but core functionality should work")
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Failed to create environment file")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but installation may still be successful")
    
    print("\n🎉 SableAI installation completed!")
    print("=" * 50)
    print("📚 Next steps:")
    print("1. Copy .env.example to .env and configure your API keys")
    print("2. Run: python example_usage.py")
    print("3. Run: python strategy_launcher.py --mode demo")
    print("4. Check the documentation in README.md")
    print("\n🚀 Happy trading!")

if __name__ == "__main__":
    main()
