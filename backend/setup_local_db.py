#!/usr/bin/env python3
"""
Setup script for local PostgreSQL database development.
This script helps create the database and initial setup for local development.
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
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_postgresql_installed():
    """Check if PostgreSQL is installed and running"""
    print("🔍 Checking PostgreSQL installation...")
    
    # Check if psql command exists
    if not run_command("which psql", "Checking psql command"):
        print("❌ PostgreSQL is not installed or not in PATH")
        print("Please install PostgreSQL first:")
        print("  macOS: brew install postgresql")
        print("  Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        return False
    
    # Check if PostgreSQL is running
    if not run_command("pg_isready", "Checking PostgreSQL service"):
        print("❌ PostgreSQL service is not running")
        print("Please start PostgreSQL:")
        print("  macOS: brew services start postgresql")
        print("  Ubuntu: sudo systemctl start postgresql")
        return False
    
    print("✅ PostgreSQL is installed and running")
    return True

def create_database():
    """Create the database and user"""
    print("🗄️ Setting up database...")
    
    # Create database
    create_db_cmd = "createdb stock_rec"
    if not run_command(create_db_cmd, "Creating database 'stock_rec'"):
        print("Database might already exist, continuing...")
    
    print("✅ Database setup completed")
    return True

def get_postgres_user():
    """Get the current PostgreSQL user"""
    try:
        result = subprocess.run(["whoami"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return "postgres"

def create_env_file():
    """Create .env file for local development"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️ .env file already exists, skipping creation")
        return True
    
    # Get the current user for PostgreSQL
    postgres_user = get_postgres_user()
    
    env_content = f"""# Database Configuration for Local Development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_rec
DB_USER={postgres_user}
DB_PASSWORD=

# Application Configuration
ENVIRONMENT=development
PORT=8000
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"✅ Created .env file for local development (using user: {postgres_user})")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    print("✅ Dependencies installed")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up local PostgreSQL database for stock-rec application...")
    print()
    
    # Check PostgreSQL installation
    if not check_postgresql_installed():
        sys.exit(1)
    
    print()
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    print()
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print()
    print("🎉 Local setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Run the migration script: python migrate_json_to_db.py")
    print("2. Start the application: python main.py")
    print("3. Test the API: curl http://localhost:8000/stocks")
    print()
    print("Note: Make sure to set up your PostgreSQL user password if needed.")

if __name__ == "__main__":
    main()
