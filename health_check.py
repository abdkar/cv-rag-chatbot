#!/usr/bin/env python3
"""
CV RAG Health Check Script
Comprehensive system verification based on README.md requirements
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

def print_status(message, status="INFO"):
    """Print formatted status message"""
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def check_python_version():
    """Check Python version requirement"""
    print_status("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} ✓", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+", "ERROR")
        return False

def check_dependencies():
    """Check required dependencies"""
    print_status("Checking dependencies...")
    dependencies = [
        "streamlit",
        "langchain",
        "sentence_transformers", 
        "faiss",
        "google.generativeai",
        "pypdf",
        "dotenv"
    ]
    
    failed = []
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print_status(f"  {dep} ✓", "SUCCESS")
        except ImportError:
            print_status(f"  {dep} ✗", "ERROR")
            failed.append(dep)
    
    return len(failed) == 0

def check_environment():
    """Check environment setup"""
    print_status("Checking environment setup...")
    
    # Load .env file
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print_status("Google API key configured ✓", "SUCCESS")
        return True
    else:
        print_status("Google API key missing in .env file", "ERROR")
        return False

def check_files():
    """Check required files"""
    print_status("Checking required files...")
    
    required_files = [
        "app.py",
        "knowledge_base.txt",
        "requirements.txt",
        ".env"
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print_status(f"  {file} ({size} bytes) ✓", "SUCCESS")
        else:
            print_status(f"  {file} ✗", "ERROR")
            missing.append(file)
    
    return len(missing) == 0

def check_knowledge_base():
    """Check knowledge base content"""
    print_status("Checking knowledge base content...")
    
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            content = f.read()
            
        if "Abdolamir Karbalaie" in content:
            print_status("Knowledge base contains required name ✓", "SUCCESS")
            print_status(f"Knowledge base size: {len(content)} characters", "INFO")
            return True
        else:
            print_status("Knowledge base missing required name", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Error reading knowledge base: {e}", "ERROR")
        return False

def check_app_server():
    """Check if Streamlit app is running"""
    print_status("Checking app server...")
    
    ports_to_check = [8501, 57965]
    
    for port in ports_to_check:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                print_status(f"App running on port {port} ✓", "SUCCESS")
                return True
        except requests.exceptions.RequestException:
            continue
    
    print_status("App server not responding", "WARNING")
    return False

def check_vector_store():
    """Check vector store"""
    print_status("Checking vector store...")
    
    vector_path = Path("vector_store")
    if vector_path.exists():
        files = list(vector_path.glob("*"))
        print_status(f"Vector store exists with {len(files)} files ✓", "SUCCESS")
        return True
    else:
        print_status("Vector store not found (will be created on first run)", "WARNING")
        return True  # This is OK, it gets created automatically

def test_imports():
    """Test critical app imports"""
    print_status("Testing critical imports...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        import streamlit as st
        
        print_status("All critical imports successful ✓", "SUCCESS")
        return True
        
    except Exception as e:
        print_status(f"Import error: {e}", "ERROR")
        return False

def main():
    """Run comprehensive health check"""
    print("🏥 CV RAG Health Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_environment),
        ("Required Files", check_files),
        ("Knowledge Base", check_knowledge_base),
        ("Critical Imports", test_imports),
        ("Vector Store", check_vector_store),
        ("App Server", check_app_server),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 {name}")
        print("-" * 30)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score: {passed}/{total} checks passed")
    
    if passed == total:
        print_status("🎉 All systems operational!", "SUCCESS")
        return True
    else:
        print_status(f"⚠️ {total - passed} issues found", "WARNING")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
