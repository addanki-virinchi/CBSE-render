#!/usr/bin/env python3
"""
Test script to verify imports work correctly (without webdriver-manager)
"""

import sys
import traceback

def test_basic_imports():
    """Test basic imports that should work locally"""
    try:
        print("🧪 Testing basic imports...")
        
        # Test pandas
        import pandas as pd
        print("✅ pandas imported successfully")
        
        # Test selenium
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        print("✅ selenium imports successful")
        
        # Test other dependencies
        import json
        import re
        import time
        import logging
        print("✅ standard library imports successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        traceback.print_exc()
        return False

def test_config_imports():
    """Test config imports"""
    try:
        print("\n🧪 Testing config imports...")
        
        # Test config import with fallback
        try:
            import config
            print("✅ config.py imported successfully")
        except ImportError:
            print("⚠️ config.py not available (using fallback)")
        
        # Test render_config
        try:
            from render_config import render_config
            print("✅ render_config imported successfully")
        except ImportError as e:
            print(f"❌ render_config import failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config imports failed: {e}")
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that all required files exist"""
    try:
        print("\n🧪 Testing file structure...")
        
        import os
        required_files = [
            'app.py',
            'sequential_process_state.py',
            'phase1_statewise_scraper.py',
            'phase2_automated_processor.py',
            'render_config.py',
            'requirements.txt',
            'render.yaml'
        ]
        
        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file} exists")
            else:
                print(f"❌ {file} missing")
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ File structure test failed: {e}")
        traceback.print_exc()
        return False

def test_requirements():
    """Test requirements.txt content"""
    try:
        print("\n🧪 Testing requirements.txt...")
        
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'pandas',
            'selenium',
            'webdriver-manager',
            'setuptools',
            'gspread',
            'google-auth',
            'flask'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package in content:
                print(f"✅ {package} in requirements.txt")
            else:
                print(f"❌ {package} missing from requirements.txt")
                missing_packages.append(package)
        
        # Check that undetected-chromedriver is NOT in requirements
        if 'undetected-chromedriver' not in content:
            print("✅ undetected-chromedriver removed from requirements.txt")
        else:
            print("❌ undetected-chromedriver still in requirements.txt")
            missing_packages.append("undetected-chromedriver should be removed")
        
        if missing_packages:
            print(f"❌ Requirements issues: {missing_packages}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 CHROME DRIVER MIGRATION TEST")
    print("="*50)
    
    results = []
    
    # Run all tests
    results.append(("Basic Imports", test_basic_imports()))
    results.append(("Config Imports", test_config_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Requirements", test_requirements()))
    
    # Summary
    print("\n" + "="*50)
    print("🎯 TEST SUMMARY")
    print("="*50)
    
    all_tests_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_tests_passed = False
    
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Chrome driver migration completed successfully")
        print("Ready for deployment to Render.com")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Fix the issues before deploying")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
