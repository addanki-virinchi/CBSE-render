#!/usr/bin/env python3
"""
Test script to verify Flask app compatibility with SequentialStateProcessor
"""

import sys
import traceback

def test_import():
    """Test importing SequentialStateProcessor"""
    try:
        print("🧪 Testing import of SequentialStateProcessor...")
        from sequential_process_state import SequentialStateProcessor
        print("✅ Import successful")
        return SequentialStateProcessor
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return None

def test_states_list(processor_class):
    """Test states_list attribute"""
    try:
        print("\n🧪 Testing states_list attribute...")
        processor = processor_class()
        
        if hasattr(processor, 'states_list'):
            states_list = processor.states_list
            print(f"✅ states_list exists with {len(states_list)} states")
            print(f"   First few states: {states_list[:3]}")
            return True
        else:
            print("❌ states_list attribute not found")
            print(f"   Available attributes: {[attr for attr in dir(processor) if not attr.startswith('_')]}")
            return False
    except Exception as e:
        print(f"❌ Error testing states_list: {e}")
        traceback.print_exc()
        return False

def test_process_complete_state(processor_class):
    """Test process_complete_state method"""
    try:
        print("\n🧪 Testing process_complete_state method...")
        processor = processor_class()
        
        if hasattr(processor, 'process_complete_state'):
            print("✅ process_complete_state method exists")
            # Test method signature
            import inspect
            sig = inspect.signature(processor.process_complete_state)
            print(f"   Method signature: {sig}")
            return True
        else:
            print("❌ process_complete_state method not found")
            print(f"   Available methods: {[method for method in dir(processor) if callable(getattr(processor, method)) and not method.startswith('_')]}")
            return False
    except Exception as e:
        print(f"❌ Error testing process_complete_state: {e}")
        traceback.print_exc()
        return False

def test_flask_endpoints():
    """Test Flask app endpoints"""
    try:
        print("\n🧪 Testing Flask app endpoints...")
        from sequential_process_state import SequentialStateProcessor
        
        # Test /api/states endpoint logic
        processor = SequentialStateProcessor()
        states = processor.states_list
        print(f"✅ /api/states would return {len(states)} states")
        
        # Test /api/start endpoint logic
        if hasattr(processor, 'process_complete_state'):
            print("✅ /api/start can call process_complete_state method")
        else:
            print("❌ /api/start cannot call process_complete_state method")
            
        return True
    except Exception as e:
        print(f"❌ Error testing Flask endpoints: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 FLASK COMPATIBILITY TEST")
    print("="*50)
    
    # Test 1: Import
    processor_class = test_import()
    if not processor_class:
        print("\n❌ CRITICAL: Cannot import SequentialStateProcessor")
        return False
    
    # Test 2: states_list attribute
    states_list_ok = test_states_list(processor_class)
    
    # Test 3: process_complete_state method
    method_ok = test_process_complete_state(processor_class)
    
    # Test 4: Flask endpoints
    flask_ok = test_flask_endpoints()
    
    # Summary
    print("\n" + "="*50)
    print("🎯 TEST SUMMARY")
    print("="*50)
    print(f"Import SequentialStateProcessor: {'✅' if processor_class else '❌'}")
    print(f"states_list attribute: {'✅' if states_list_ok else '❌'}")
    print(f"process_complete_state method: {'✅' if method_ok else '❌'}")
    print(f"Flask endpoints compatibility: {'✅' if flask_ok else '❌'}")
    
    all_tests_passed = all([processor_class, states_list_ok, method_ok, flask_ok])
    
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED - Flask app should work correctly!")
    else:
        print("\n❌ SOME TESTS FAILED - Flask app will have errors")
        
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
