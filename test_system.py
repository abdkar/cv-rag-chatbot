#!/usr/bin/env python3
"""
🧪 CV RAG Chatbot System Tester
Complete testing and troubleshooting script for the CV RAG application.

Usage:
    python test_system.py

This script will:
1. Test all system dependencies
2. Validate configuration
3. Check API connectivity  
4. Test RAG pipeline
5. Verify UI components
6. Provide troubleshooting guidance
"""

import os
import sys
import traceback
from pathlib import Path
import importlib
import subprocess

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print(f"🧪 {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_fix(text):
    print(f"{Colors.PURPLE}🔧 FIX: {text}{Colors.END}")

class SystemTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
    def test_dependencies(self):
        """Test all required Python packages."""
        print_header("Testing Dependencies")
        
        required_packages = [
            'streamlit',
            'langchain',
            'langchain_community', 
            'langchain_core',
            'langchain_text_splitters',
            'langchain_google_genai',
            'faiss',
            'dotenv',
            'google.generativeai'
        ]
        
        for package in required_packages:
            try:
                if package == 'faiss':
                    import faiss
                elif package == 'dotenv':
                    from dotenv import load_dotenv
                elif package == 'google.generativeai':
                    import google.generativeai as genai
                else:
                    importlib.import_module(package)
                print_success(f"{package} imported successfully")
            except ImportError as e:
                self.errors.append(f"Missing package: {package}")
                print_error(f"Failed to import {package}: {e}")
                print_fix(f"Install with: pip install {package}")
        
        return len(self.errors) == 0

    def test_project_structure(self):
        """Test if all required files and directories exist."""
        print_header("Testing Project Structure")
        
        required_files = [
            'app_smart.py',
            'app.py', 
            'knowledge_base.txt',
            'requirements.txt',
            '.env.template',
            'configs/app_config.py',
            'src/core/rag_pipeline.py',
            'src/ui/components.py'
        ]
        
        required_dirs = [
            'configs',
            'src',
            'src/core', 
            'src/ui',
            'vector_store',
            'assets'
        ]
        
        # Check files
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print_success(f"Found: {file_path}")
            else:
                self.errors.append(f"Missing file: {file_path}")
                print_error(f"Missing: {file_path}")
        
        # Check directories
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                print_success(f"Found directory: {dir_path}")
            else:
                self.errors.append(f"Missing directory: {dir_path}")
                print_error(f"Missing directory: {dir_path}")

    def test_environment_config(self):
        """Test environment configuration."""
        print_header("Testing Environment Configuration")
        
        # Check .env file
        env_file = self.project_root / '.env'
        env_template = self.project_root / '.env.template'
        
        if not env_file.exists():
            if env_template.exists():
                print_warning(".env file not found, but .env.template exists")
                print_fix("Copy .env.template to .env and add your API key")
                print_fix("Command: cp .env.template .env")
            else:
                self.errors.append("Neither .env nor .env.template found")
                print_error("No environment files found")
            return False
        
        # Load and test environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                print_success("GOOGLE_API_KEY found in environment")
                if len(api_key) > 20:  # Basic validation
                    print_success("API key appears to be valid format")
                else:
                    print_warning("API key seems too short")
            else:
                self.errors.append("GOOGLE_API_KEY not found in .env")
                print_error("GOOGLE_API_KEY not set")
                print_fix("Add GOOGLE_API_KEY=your_api_key_here to .env file")
                
        except Exception as e:
            self.errors.append(f"Environment loading error: {e}")
            print_error(f"Error loading environment: {e}")
            
        return len(self.errors) == 0

    def test_api_connectivity(self):
        """Test Google Gemini API connectivity."""
        print_header("Testing API Connectivity")
        
        try:
            # Import configuration
            sys.path.append(str(self.project_root))
            from configs.app_config import get_google_api_key, ModelConfig
            import google.generativeai as genai
            
            api_key = get_google_api_key()
            if not api_key:
                self.errors.append("No API key available")
                print_error("Cannot test API - no key found")
                return False
            
            genai.configure(api_key=api_key)
            
            # Test primary model
            print_info(f"Testing primary model: {ModelConfig.PRIMARY_MODEL}")
            model = genai.GenerativeModel(ModelConfig.PRIMARY_MODEL)
            response = model.generate_content(
                "Hello, this is a test message", 
                generation_config={'max_output_tokens': 10}
            )
            print_success(f"Primary model working: {response.text[:50]}...")
            
            # Test fallback models
            for fallback_model in ModelConfig.FALLBACK_MODELS[:1]:  # Test first fallback
                try:
                    print_info(f"Testing fallback model: {fallback_model}")
                    model = genai.GenerativeModel(fallback_model)
                    response = model.generate_content(
                        "Test", 
                        generation_config={'max_output_tokens': 5}
                    )
                    print_success(f"Fallback model {fallback_model} working")
                    break
                except Exception as e:
                    print_warning(f"Fallback model {fallback_model} failed: {str(e)[:100]}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"API connectivity error: {e}")
            print_error(f"API test failed: {e}")
            print_fix("Check your API key and internet connection")
            print_fix("Verify API key at: https://makersuite.google.com/app/apikey")
            return False

    def test_rag_pipeline(self):
        """Test RAG pipeline components."""
        print_header("Testing RAG Pipeline")
        
        try:
            sys.path.append(str(self.project_root))
            
            # Test knowledge base
            kb_file = self.project_root / 'knowledge_base.txt'
            if kb_file.exists():
                content = kb_file.read_text(encoding='utf-8')
                if len(content) > 100:
                    print_success(f"Knowledge base loaded: {len(content)} characters")
                else:
                    print_warning("Knowledge base seems very small")
            else:
                self.errors.append("knowledge_base.txt not found")
                print_error("Knowledge base file missing")
                return False
            
            # Test embeddings
            try:
                from src.core.embeddings import get_embeddings
                embeddings = get_embeddings()
                print_success(f"Embeddings initialized with dimension: {embeddings.dimension}")
            except Exception as e:
                print_warning(f"Embeddings test failed: {e}")
            
            # Test vector store
            vector_store_path = self.project_root / 'vector_store'
            if vector_store_path.exists():
                print_success("Vector store directory found")
                
                # Check for index files
                index_files = list(vector_store_path.rglob('*.faiss'))
                if index_files:
                    print_success(f"Found {len(index_files)} FAISS index files")
                else:
                    print_warning("No FAISS index files found - will be created on first run")
            else:
                print_warning("Vector store directory not found - will be created")
            
            # Test RAG pipeline initialization
            try:
                from src.core.rag_pipeline import RAGPipeline
                pipeline = RAGPipeline()
                print_success("RAG pipeline initialized successfully")
                
                # Test simple query
                test_query = "What is this CV about?"
                response = pipeline.query(test_query)
                if response and len(response) > 10:
                    print_success(f"RAG query test successful: {response[:100]}...")
                else:
                    print_warning("RAG query returned short response")
                    
            except Exception as e:
                print_warning(f"RAG pipeline test failed: {e}")
                print_info("This might work once the app starts and initializes properly")
            
            return True
            
        except Exception as e:
            self.errors.append(f"RAG pipeline error: {e}")
            print_error(f"RAG pipeline test failed: {e}")
            traceback.print_exc()
            return False

    def test_streamlit_app(self):
        """Test if Streamlit app can be imported and basic components work."""
        print_header("Testing Streamlit Application")
        
        try:
            # Test app import
            sys.path.append(str(self.project_root))
            
            # Check if app_smart.py can be imported (basic syntax check)
            app_file = self.project_root / 'app_smart.py'
            if app_file.exists():
                print_success("app_smart.py found")
                
                # Basic syntax check by compiling
                with open(app_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    compile(code, 'app_smart.py', 'exec')
                    print_success("app_smart.py syntax is valid")
            else:
                self.errors.append("app_smart.py not found")
                print_error("Main application file missing")
                return False
            
            # Test UI components
            try:
                from src.ui.components import render_header, render_sidebar
                print_success("UI components can be imported")
            except Exception as e:
                print_warning(f"UI components import failed: {e}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Streamlit app error: {e}")
            print_error(f"Streamlit app test failed: {e}")
            return False

    def test_ports(self):
        """Test if the default port is available."""
        print_header("Testing Port Availability")
        
        import socket
        
        ports_to_test = [8511, 8501, 8502]  # Default and common alternatives
        
        for port in ports_to_test:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', port))
                sock.close()
                print_success(f"Port {port} is available")
                return True
            except OSError:
                print_warning(f"Port {port} is in use")
        
        print_warning("All common ports are in use")
        print_fix("You can use a different port with: streamlit run app_smart.py --server.port=8512")
        return True  # Not a critical error

    def provide_troubleshooting_guide(self):
        """Provide comprehensive troubleshooting guidance."""
        print_header("Troubleshooting Guide")
        
        if self.errors:
            print_error("Issues found that need to be fixed:")
            for i, error in enumerate(self.errors, 1):
                print(f"{Colors.RED}   {i}. {error}{Colors.END}")
        
        if self.warnings:
            print_warning("Warnings (not critical but should be addressed):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"{Colors.YELLOW}   {i}. {warning}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.WHITE}🔧 Common Issues and Solutions:{Colors.END}")
        
        solutions = [
            ("Missing dependencies", "pip install -r requirements.txt"),
            ("No API key", "1. Get key from https://makersuite.google.com/app/apikey\n        2. Copy .env.template to .env\n        3. Add GOOGLE_API_KEY=your_key_here"),
            ("API quota exceeded", "1. Wait for quota reset\n        2. Try different model in configs/app_config.py\n        3. Use app's built-in quota management"),
            ("Port already in use", "streamlit run app_smart.py --server.port=8512"),
            ("Import errors", "1. Activate virtual environment\n        2. Reinstall requirements\n        3. Check Python version (3.8+)"),
            ("Vector store issues", "Delete vector_store/ directory - will rebuild automatically"),
            ("Knowledge base empty", "Check knowledge_base.txt file exists and has content"),
        ]
        
        for issue, solution in solutions:
            print(f"\n{Colors.CYAN}🔍 {issue}:{Colors.END}")
            print(f"   {Colors.GREEN}{solution}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.WHITE}🚀 Starting the Application:{Colors.END}")
        print(f"{Colors.GREEN}streamlit run app_smart.py --server.port=8511 --server.address=0.0.0.0{Colors.END}")
        print(f"{Colors.BLUE}Then open: http://localhost:8511{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.WHITE}📞 Need Help?{Colors.END}")
        print(f"{Colors.CYAN}1. Check the logs/ directory for error details")
        print(f"2. Review docs/ directory for documentation")
        print(f"3. Run this test script again after making fixes")
        print(f"4. Check GitHub issues or create a new one{Colors.END}")

    def run_all_tests(self):
        """Run all tests and provide comprehensive report."""
        print(f"{Colors.BOLD}{Colors.PURPLE}")
        print("🧪 CV RAG Chatbot System Tester")
        print("=" * 50)
        print(f"Testing project at: {self.project_root}")
        print(f"{'=' * 50}{Colors.END}")
        
        tests = [
            ("Dependencies", self.test_dependencies),
            ("Project Structure", self.test_project_structure),
            ("Environment Config", self.test_environment_config),
            ("API Connectivity", self.test_api_connectivity),
            ("RAG Pipeline", self.test_rag_pipeline),
            ("Streamlit App", self.test_streamlit_app),
            ("Port Availability", self.test_ports),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                    print_success(f"{test_name} test passed")
                else:
                    print_error(f"{test_name} test failed")
            except Exception as e:
                print_error(f"{test_name} test crashed: {e}")
                self.errors.append(f"{test_name} test exception: {e}")
        
        # Final report
        print_header("Test Results Summary")
        
        if passed == total and not self.errors:
            print(f"{Colors.BOLD}{Colors.GREEN}")
            print("🎉 ALL TESTS PASSED!")
            print("Your CV RAG Chatbot is ready to run!")
            print(f"Start with: streamlit run app_smart.py --server.port=8511{Colors.END}")
        elif passed >= total * 0.7:  # 70% pass rate
            print(f"{Colors.BOLD}{Colors.YELLOW}")
            print(f"⚠️  MOSTLY WORKING ({passed}/{total} tests passed)")
            print("Minor issues found but app should work")
            print(f"Check warnings below{Colors.END}")
        else:
            print(f"{Colors.BOLD}{Colors.RED}")
            print(f"❌ CRITICAL ISSUES FOUND ({passed}/{total} tests passed)")
            print("Please fix the errors before running the app")
            print(f"See troubleshooting guide below{Colors.END}")
        
        # Always show troubleshooting guide
        self.provide_troubleshooting_guide()

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()
