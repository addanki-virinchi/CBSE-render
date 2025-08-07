#!/usr/bin/env python3
"""
Deployment verification script for Render.com
This script can be run on the deployed server to verify all components work correctly
"""

import sys
import traceback
import json

def verify_sequential_processor():
    """Verify SequentialStateProcessor works correctly"""
    try:
        print("🔍 Verifying SequentialStateProcessor...")
        from sequential_process_state import SequentialStateProcessor
        
        processor = SequentialStateProcessor()
        
        # Check states_list
        if hasattr(processor, 'states_list') and len(processor.states_list) > 0:
            print(f"✅ states_list: {len(processor.states_list)} states available")
        else:
            print("❌ states_list: Missing or empty")
            return False
        
        # Check process_complete_state method
        if hasattr(processor, 'process_complete_state'):
            print("✅ process_complete_state: Method exists")
        else:
            print("❌ process_complete_state: Method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ SequentialStateProcessor verification failed: {e}")
        traceback.print_exc()
        return False

def verify_render_config():
    """Verify render configuration works"""
    try:
        print("\n🔍 Verifying render configuration...")
        from render_config import render_config
        
        # Check basic config
        headless = render_config.get_config('HEADLESS')
        render_deployment = render_config.get_config('RENDER_DEPLOYMENT')
        
        print(f"✅ Headless mode: {headless}")
        print(f"✅ Render deployment: {render_deployment}")
        
        # Check credentials
        credentials = render_config.get_credentials()
        if credentials:
            print("✅ Google credentials: Available")
        else:
            print("⚠️ Google credentials: Not available (check GOOGLE_CREDENTIALS_JSON env var)")
        
        return True
        
    except Exception as e:
        print(f"❌ Render config verification failed: {e}")
        traceback.print_exc()
        return False

def verify_flask_endpoints():
    """Verify Flask endpoints would work"""
    try:
        print("\n🔍 Verifying Flask endpoint compatibility...")
        from sequential_process_state import SequentialStateProcessor
        
        processor = SequentialStateProcessor()
        
        # Test /api/states endpoint
        try:
            states = processor.states_list
            states_json = json.dumps({'states': states})
            print(f"✅ /api/states: Would return {len(states)} states")
        except Exception as e:
            print(f"❌ /api/states: Would fail - {e}")
            return False
        
        # Test /api/start endpoint
        try:
            # Just check if method exists and is callable
            method = getattr(processor, 'process_complete_state')
            if callable(method):
                print("✅ /api/start: process_complete_state method is callable")
            else:
                print("❌ /api/start: process_complete_state is not callable")
                return False
        except Exception as e:
            print(f"❌ /api/start: Would fail - {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask endpoints verification failed: {e}")
        traceback.print_exc()
        return False

def verify_dependencies():
    """Verify all required dependencies are available"""
    try:
        print("\n🔍 Verifying dependencies...")
        
        # Core dependencies
        import pandas
        print("✅ pandas: Available")
        
        import selenium
        print("✅ selenium: Available")
        
        import undetected_chromedriver
        print("✅ undetected-chromedriver: Available")
        
        import flask
        print("✅ flask: Available")
        
        # Google Sheets dependencies
        try:
            import gspread
            import google.oauth2.service_account
            print("✅ Google Sheets dependencies: Available")
        except ImportError:
            print("⚠️ Google Sheets dependencies: Not available")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependencies verification failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    print("🚀 RENDER DEPLOYMENT VERIFICATION")
    print("="*60)
    
    results = []
    
    # Run all verifications
    results.append(("Dependencies", verify_dependencies()))
    results.append(("Render Config", verify_render_config()))
    results.append(("SequentialStateProcessor", verify_sequential_processor()))
    results.append(("Flask Endpoints", verify_flask_endpoints()))
    
    # Summary
    print("\n" + "="*60)
    print("🎯 VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL VERIFICATIONS PASSED!")
        print("The Flask application should work correctly on Render.com")
    else:
        print("❌ SOME VERIFICATIONS FAILED!")
        print("The Flask application may have issues on Render.com")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
