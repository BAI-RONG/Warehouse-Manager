#!/usr/bin/env python3
"""
Setup script for SFT Data Synthesis System
Helps users configure the environment and dependencies
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠️  Not running in virtual environment")
        print("Recommendation: Create and activate a virtual environment")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Linux/Mac")
        print("  # or")
        print("  venv\\Scripts\\activate  # On Windows")
        return False
    print("✅ Running in virtual environment")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example template found")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print("✅ Created output directory")

def verify_input_files():
    """Verify required input files exist"""
    print("\n📁 Verifying input files...")
    
    required_files = {
        "PRD_context/live_streaming_prd.md": "PRD document",
        "rd_suggestions/technical_optimization.md": "RD suggestions", 
        "evaluation_data/script_evaluation_data.csv": "Evaluation data",
        "prompts/gaming_script_template.txt": "Prompt template",
        "base_dataset.jsonl": "Base dataset",
        "config/config.yaml": "Configuration file"
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (missing)")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test that all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    test_modules = [
        "langchain",
        "langgraph", 
        "pandas",
        "yaml",
        "agents.requirement_decomposition_agent",
        "tools.llm_tools"
    ]
    
    all_imported = True
    for module in test_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_imported = False
    
    return all_imported

def show_usage_instructions():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    
    print("""
📖 Next Steps:

1️⃣ Configure API Keys:
   • Edit .env file and add your OpenAI API key
   • Or set OPENAI_API_KEY environment variable
   • Or edit config/config.yaml directly

2️⃣ Run Demonstrations:
   • Simple overview: python simple_demo.py
   • Full demo: python demo.py
   • Complete workflow: python -m workflow.main_workflow

3️⃣ Customize Configuration:
   • Edit config/config.yaml for system parameters
   • Modify prompt templates in prompts/ directory
   • Add your own PRD documents and RD suggestions

4️⃣ View Results:
   • Check output/ directory for generated data
   • Review workflow reports and analysis

🔗 Documentation:
   • README.md - Detailed documentation
   • 架构图.jpg - System architecture diagram

⚠️  Remember to keep your API keys secure!
""")

def main():
    """Main setup function"""
    print("="*60)
    print("🚀 SFT Data Synthesis System Setup")
    print("="*60)
    
    # Check requirements
    if not check_python_version():
        return False
    
    # Check virtual environment (warning only)
    check_virtual_environment()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup environment
    setup_environment()
    
    # Verify files
    files_ok = verify_input_files()
    
    # Test imports
    imports_ok = test_imports()
    
    # Show instructions
    show_usage_instructions()
    
    if files_ok and imports_ok:
        print("✅ Setup completed successfully!")
        return True
    else:
        print("⚠️  Setup completed with warnings. Check messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)