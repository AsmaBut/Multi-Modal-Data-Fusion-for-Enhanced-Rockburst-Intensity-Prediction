#!/usr/bin/env python3
"""
Simple test script for the Geological Analysis Application
Run this to verify the application is working correctly
"""

import requests
import json
import time
import sys

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_data_endpoint(base_url):
    """Test the main data endpoint"""
    print("🔍 Testing data endpoint...")
    try:
        response = requests.get(f"{base_url}/api/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Data endpoint working:")
            print(f"   - Total records: {data.get('total_records', 'N/A')}")
            print(f"   - Columns: {len(data.get('columns', []))}")
            return True
        else:
            print(f"❌ Data endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Data endpoint error: {e}")
        return False

def test_analysis_endpoints(base_url):
    """Test the analysis endpoints"""
    print("🔍 Testing analysis endpoints...")
    
    analysis_types = ['composition', 'rockburst', 'mechanical']
    success_count = 0
    
    for analysis_type in analysis_types:
        try:
            response = requests.get(f"{base_url}/api/analysis/{analysis_type}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {analysis_type} analysis working")
                success_count += 1
            else:
                print(f"❌ {analysis_type} analysis failed with status {response.status_code}")
        except Exception as e:
            print(f"❌ {analysis_type} analysis error: {e}")
    
    return success_count == len(analysis_types)

def test_search_endpoint(base_url):
    """Test the search endpoint"""
    print("🔍 Testing search endpoint...")
    try:
        response = requests.get(f"{base_url}/api/search", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search endpoint working:")
            print(f"   - Total matches: {data.get('total_matches', 'N/A')}")
            return True
        else:
            print(f"❌ Search endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
        return False

def test_main_page(base_url):
    """Test the main page loads"""
    print("🔍 Testing main page...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if "Geological Analysis Dashboard" in content:
                print("✅ Main page loads correctly")
                return True
            else:
                print("❌ Main page content not as expected")
                return False
        else:
            print(f"❌ Main page failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Geological Analysis Application Test Suite")
    print("=" * 50)
    
    # Test different base URLs
    base_urls = [
        "http://localhost:5000",  # Direct Flask app
        "http://localhost:80"     # Through Nginx
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing {base_url}")
        print("-" * 30)
        
        # Test if the service is reachable
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print(f"✅ Service reachable at {base_url}")
        except:
            print(f"❌ Service not reachable at {base_url}")
            continue
        
        # Run all tests
        tests = [
            test_health_endpoint,
            test_data_endpoint,
            test_analysis_endpoints,
            test_search_endpoint,
            test_main_page
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test(base_url):
                passed += 1
            time.sleep(0.5)  # Small delay between tests
        
        print(f"\n📊 Test Results for {base_url}:")
        print(f"   Passed: {passed}/{total}")
        
        if passed == total:
            print(f"🎉 All tests passed for {base_url}!")
        else:
            print(f"⚠️  Some tests failed for {base_url}")
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")
    
    # Provide helpful information
    print("\n💡 If tests are failing:")
    print("   1. Ensure Docker containers are running: docker-compose ps")
    print("   2. Check container logs: docker-compose logs")
    print("   3. Verify data files exist in task2itsolera/ directory")
    print("   4. Check if ports 5000 and 80 are available")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
