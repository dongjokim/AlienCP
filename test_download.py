#!/usr/bin/env python3
"""
Test script to demonstrate the download functionality
"""

import os
import tempfile
from pathlib import Path

def test_download_script():
    """Test the download script with a mock scenario"""
    
    print("Testing AlienCP download script...")
    print("=" * 50)
    
    # Test help command
    print("1. Testing help command:")
    os.system("python3 download_file.py --help")
    print()
    
    # Test invalid alien path
    print("2. Testing invalid alien path:")
    os.system("python3 download_file.py invalid_path")
    print()
    
    # Test with a real alien path (this will fail if alien_cp is not available)
    print("3. Testing with real alien path (will fail if alien_cp not available):")
    test_path = "alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root"
    os.system(f"python3 download_file.py {test_path} -v")
    print()
    
    print("Test completed!")

if __name__ == "__main__":
    test_download_script()
