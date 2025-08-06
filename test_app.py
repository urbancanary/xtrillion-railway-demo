#!/usr/bin/env python3
"""
Testing Framework for Guinness App
Run periodic tests to ensure app functionality
"""

import os
import sys
import importlib
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class AppTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test_imports(self) -> Tuple[bool, str]:
        """Test that all required imports work"""
        print("Testing imports...")
        required_imports = [
            'streamlit',
            'pandas',
            'plotly',
            'requests',
            'numpy',
            'report_utils',
            'credit_reports',
            'portfolio_valuation',
            'user_guide',
            'debug_deployment'
        ]
        
        failed_imports = []
        for module in required_imports:
            try:
                importlib.import_module(module)
            except ImportError as e:
                failed_imports.append(f"{module}: {str(e)}")
        
        if failed_imports:
            return False, f"Failed imports: {', '.join(failed_imports)}"
        return True, "All imports successful"
    
    def test_file_structure(self) -> Tuple[bool, str]:
        """Test that required files exist"""
        print("Testing file structure...")
        required_files = [
            'guinness_app.py',
            'requirements.txt',
            'report_utils.py',
            'credit_reports.py',
            'portfolio_valuation.py',
            'user_guide.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        return True, "All required files present"
    
    def test_data_files(self) -> Tuple[bool, str]:
        """Test that data files are accessible"""
        print("Testing data files...")
        data_files = [
            'data.csv',  # If used
            '.streamlit/config.toml'
        ]
        
        issues = []
        for file in data_files:
            if os.path.exists(file):
                try:
                    size = os.path.getsize(file)
                    if size == 0:
                        issues.append(f"{file} is empty")
                except:
                    issues.append(f"Cannot read {file}")
        
        if issues:
            return False, f"Data file issues: {', '.join(issues)}"
        return True, "Data files OK"
    
    def test_navigation_structure(self) -> Tuple[bool, str]:
        """Test that navigation structure is valid"""
        print("Testing navigation structure...")
        try:
            # Import the main app to check navigation
            import guinness_app
            return True, "Navigation structure valid"
        except Exception as e:
            return False, f"Navigation error: {str(e)}"
    
    def test_api_connectivity(self) -> Tuple[bool, str]:
        """Test API connectivity (if applicable)"""
        print("Testing API connectivity...")
        try:
            import requests
            # Test a simple endpoint
            response = requests.get("https://api.github.com", timeout=5)
            if response.status_code == 200:
                return True, "API connectivity OK"
            else:
                return False, f"API returned status {response.status_code}"
        except Exception as e:
            return False, f"API connection failed: {str(e)}"
    
    def run_all_tests(self) -> Dict:
        """Run all tests and generate report"""
        print(f"\n{'='*60}")
        print(f"Guinness App Test Suite - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        tests = [
            ("Import Test", self.test_imports),
            ("File Structure Test", self.test_file_structure),
            ("Data Files Test", self.test_data_files),
            ("Navigation Test", self.test_navigation_structure),
            ("API Connectivity Test", self.test_api_connectivity)
        ]
        
        for test_name, test_func in tests:
            try:
                passed, message = test_func()
                self.results.append({
                    'test': test_name,
                    'passed': passed,
                    'message': message
                })
                if passed:
                    self.passed += 1
                    print(f"✅ {test_name}: PASSED - {message}")
                else:
                    self.failed += 1
                    print(f"❌ {test_name}: FAILED - {message}")
            except Exception as e:
                self.failed += 1
                self.results.append({
                    'test': test_name,
                    'passed': False,
                    'message': f"Exception: {str(e)}"
                })
                print(f"❌ {test_name}: ERROR - {str(e)}")
        
        # Generate summary
        print(f"\n{'='*60}")
        print(f"Test Summary: {self.passed} passed, {self.failed} failed")
        print(f"{'='*60}\n")
        
        # Save results
        self.save_results()
        
        return {
            'total': len(tests),
            'passed': self.passed,
            'failed': self.failed,
            'results': self.results
        }
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"test_results_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Guinness App Test Results\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"{'='*60}\n\n")
            
            for result in self.results:
                status = "PASS" if result['passed'] else "FAIL"
                f.write(f"{status}: {result['test']}\n")
                f.write(f"      {result['message']}\n\n")
            
            f.write(f"\nSummary: {self.passed}/{len(self.results)} tests passed\n")
        
        print(f"Results saved to {filename}")

def main():
    """Run tests with command line options"""
    tester = AppTester()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        # Continuous testing mode
        import time
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            tester = AppTester()  # Reset for fresh results
            tester.run_all_tests()
            print("\nWatching for changes... (Ctrl+C to stop)")
            time.sleep(300)  # Run every 5 minutes
    else:
        # Single run
        results = tester.run_all_tests()
        sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()