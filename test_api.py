#!/usr/bin/env python3
"""
Simple test script to verify AI Microservices API functionality
"""
import requests
import json
import time
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Available providers: {data.get('available_providers', [])}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_summarization():
    """Test text summarization"""
    print("\n📝 Testing text summarization...")
    try:
        test_text = """
        Artificial Intelligence (AI) is a transformative technology that enables machines to perform tasks typically requiring human intelligence. 
        It encompasses various subfields including machine learning, natural language processing, computer vision, and robotics. 
        AI systems learn from data, recognize patterns, and make decisions with minimal human intervention. 
        The technology has applications across industries, from healthcare and finance to transportation and entertainment. 
        Machine learning, particularly deep learning, has driven recent breakthroughs in AI capabilities. 
        However, AI development also raises important ethical considerations regarding privacy, bias, and job displacement.
        """
        
        payload = {
            "text": test_text.strip(),
            "max_length": 80,
            "provider": "ollama"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/summarize", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Summarization successful")
            print(f"   Original length: {data['original_length']} words")
            print(f"   Summary length: {data['summary_length']} words")
            print(f"   Provider: {data['provider_used']}")
            print(f"   Summary: {data['summary'][:100]}...")
            return True
        else:
            print(f"❌ Summarization failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Summarization error: {e}")
        return False

def test_qa():
    """Test Q&A functionality"""
    print("\n🤔 Testing Q&A...")
    try:
        payload = {
            "question": "What is artificial intelligence?",
            "provider": "ollama"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/qa", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Q&A successful")
            print(f"   Question: {data['question']}")
            print(f"   Answer: {data['answer'][:100]}...")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
            print(f"   Provider: {data['provider_used']}")
            return True
        else:
            print(f"❌ Q&A failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Q&A error: {e}")
        return False

def test_learning_path():
    """Test learning path generation"""
    print("\n📚 Testing learning path generation...")
    try:
        payload = {
            "goals": [
                {
                    "topic": "Python Programming",
                    "proficiency_level": "beginner",
                    "time_commitment": "5 hours/week"
                }
            ],
            "background": "Complete beginner with no programming experience",
            "duration_weeks": 8,
            "provider": "ollama"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/learning-path", json=payload, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Learning path generation successful")
            print(f"   Path title: {data['path_title']}")
            print(f"   Duration: {data['total_duration_weeks']} weeks")
            print(f"   Steps: {len(data['steps'])} weekly steps")
            print(f"   Prerequisites: {len(data['prerequisites'])} items")
            print(f"   Provider: {data['provider_used']}")
            return True
        else:
            print(f"❌ Learning path failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Learning path error: {e}")
        return False

def wait_for_server(max_attempts=12, delay=5):
    """Wait for server to be ready"""
    print(f"⏳ Waiting for server at {BASE_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        
        if attempt < max_attempts - 1:
            print(f"   Attempt {attempt + 1}/{max_attempts} - Retrying in {delay}s...")
            time.sleep(delay)
    
    print("❌ Server is not responding")
    return False

def main():
    """Run all tests"""
    print("🚀 AI Microservices API Test Suite")
    print("=" * 50)
    
    # Wait for server
    if not wait_for_server():
        print("\n❌ Cannot connect to server. Please ensure:")
        print("   1. Backend server is running (python main.py)")
        print("   2. Server is accessible at http://localhost:8000")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Text Summarization", test_summarization),
        ("Q&A", test_qa),
        ("Learning Path", test_learning_path),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error in {test_name}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI Microservices API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\nCommon issues:")
        print("- Ollama not running (start with: ollama serve)")
        print("- Missing environment variables in .env file")
        print("- Required Python packages not installed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)