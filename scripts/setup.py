#!/usr/bin/env python3
"""
CV RAG Chatbot Setup Script
Helps users set up the application for the first time
"""

import os
import sys
import subprocess
from pathlib import Path

def print_step(step, message):
    """Print formatted step message"""
    print(f"\n🔸 Step {step}: {message}")
    print("-" * 50)

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.10+")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("🔑 Setting up environment file...")
    api_key = input("Enter your Google Gemini API key: ").strip()
    
    if not api_key:
        print("❌ API key is required")
        return False
    
    try:
        with open(".env", "w") as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def setup_knowledge_base():
    """Set up knowledge base file"""
    kb_file = Path("knowledge_base.txt")
    
    if kb_file.exists():
        print("✅ knowledge_base.txt already exists")
        return True
    
    print("📝 Setting up knowledge base...")
    print("You need to create a knowledge_base.txt file with your CV content.")
    print("You can:")
    print("1. Copy knowledge_base_template.txt to knowledge_base.txt and edit it")
    print("2. Create your own knowledge_base.txt file")
    
    choice = input("Would you like to copy the template? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        try:
            template_file = Path("knowledge_base_template.txt")
            if template_file.exists():
                import shutil
                shutil.copy("knowledge_base_template.txt", "knowledge_base.txt")
                print("✅ Template copied to knowledge_base.txt")
                print("📝 Please edit knowledge_base.txt with your actual CV content")
                return True
            else:
                print("❌ Template file not found")
                return False
        except Exception as e:
            print(f"❌ Failed to copy template: {e}")
            return False
    else:
        print("📝 Please create knowledge_base.txt manually with your CV content")
        return False

def setup_profile_photo():
    """Check for profile photo"""
    photo_file = Path("phto.jpg")
    
    if photo_file.exists():
        print("✅ Profile photo (phto.jpg) found")
        return True
    
    print("📸 Profile photo setup...")
    print("Please add your profile photo as 'phto.jpg' in the project directory")
    print("Recommended: Square image, at least 300x300 pixels")
    return True

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    try:
        # Test basic imports
        import streamlit
        import langchain
        from dotenv import load_dotenv
        
        # Test API key
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            print("⚠️ API key not found in .env file")
            return False
        
        print("✅ All imports successful")
        print("✅ API key configured")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 CV RAG Chatbot Setup")
    print("=" * 50)
    
    steps = [
        ("1", "Checking Python version", check_python_version),
        ("2", "Installing dependencies", install_dependencies),
        ("3", "Setting up environment", setup_environment),
        ("4", "Setting up knowledge base", setup_knowledge_base),
        ("5", "Checking profile photo", setup_profile_photo),
        ("6", "Testing installation", test_installation),
    ]
    
    failed_steps = []
    
    for step, description, function in steps:
        print_step(step, description)
        if not function():
            failed_steps.append(description)
    
    print("\n" + "=" * 50)
    print("📊 SETUP SUMMARY")
    print("=" * 50)
    
    if not failed_steps:
        print("🎉 Setup completed successfully!")
        print("\n🚀 Next steps:")
        print("1. Edit knowledge_base.txt with your actual CV content")
        print("2. Add your profile photo as phto.jpg")
        print("3. Run the application: streamlit run app.py")
        print("4. Open http://localhost:8501 in your browser")
    else:
        print("⚠️ Setup completed with issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease resolve these issues and run setup again.")

if __name__ == "__main__":
    main()
