#!/usr/bin/env python3
"""
Simple script to download files from Alien using alien_cp
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def get_alien_file_size(alien_path):
    """
    Get the size of a file in Alien using alien_ls command
    
    Args:
        alien_path (str): Path to the file in Alien
        
    Returns:
        int: File size in bytes, or None if unable to determine
    """
    try:
        cmd = f"alien_ls -l {alien_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            # Parse the output to get file size
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if alien_path.split('/')[-1] in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        return int(parts[4])  # File size is typically the 5th column
        return None
    except Exception as e:
        return None


def download_file(alien_path, local_path=None, download_dir=None, verbose=False, skip_existing=True):
    """
    Download a file from Alien using alien_cp command
    
    Args:
        alien_path (str): Path to the file in Alien (e.g., alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root)
        local_path (str, optional): Local path to save the file. If None, uses the filename from alien_path
        download_dir (str, optional): Directory to download files to. If specified, local_path will be relative to this directory
        verbose (bool): Enable verbose output
        skip_existing (bool): Skip download if file already exists and sizes match
    """
    
    # Check if alien_cp is available
    if not check_alien_cp():
        print("Error: alien_cp command not found. Please ensure ALICE software is properly installed.")
        return False
    
    # Set default local path if not provided
    if local_path is None:
        local_path = Path(alien_path).name
    
    # Apply download directory if specified
    if download_dir:
        download_dir = Path(download_dir)
        download_dir.mkdir(parents=True, exist_ok=True)
        local_path = download_dir / Path(local_path).name
    
    # Convert to absolute path
    local_path = Path(local_path).resolve()
    
    # Ensure the local directory exists
    local_dir = local_path.parent
    local_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if file already exists and compare sizes
    if skip_existing and local_path.exists():
        local_size = local_path.stat().st_size
        alien_size = get_alien_file_size(alien_path)
        
        if verbose:
            print(f"Local file exists: {local_path}")
            print(f"Local size: {local_size} bytes")
            if alien_size is not None:
                print(f"Alien size: {alien_size} bytes")
        
        if alien_size is not None and local_size == alien_size:
            print(f"✓ File already exists with matching size: {local_path}")
            return True
        elif alien_size is not None and local_size != alien_size:
            print(f"⚠ File exists but size differs (local: {local_size}, alien: {alien_size}). Re-downloading...")
        else:
            print(f"⚠ File exists but cannot determine Alien size. Re-downloading...")
    
    # Build the alien_cp command
    cmd = f"alien_cp {alien_path} file://{os.path.abspath(local_path)}"
    
    if verbose:
        print(f"Downloading: {alien_path}")
        print(f"To: {os.path.abspath(local_path)}")
        print(f"Command: {cmd}")
    
    # Execute the download
    try:
        result = os.system(cmd)
        if result == 0:
            print(f"✓ Successfully downloaded: {local_path}")
            return True
        else:
            print(f"✗ Failed to download file. Exit code: {result}")
            return False
    except Exception as e:
        print(f"✗ Error during download: {e}")
        return False


def check_alien_cp():
    """Check if alien_cp command is available"""
    try:
        result = os.system("which alien_cp > /dev/null 2>&1")
        return result == 0
    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download files from Alien using alien_cp with smart duplicate detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic download to current directory
  python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root
  
  # Download to specific directory
  python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data
  
  # Download with custom filename in specific directory
  python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -o my_file.root
  
  # Force re-download even if file exists
  python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data --force
  
  # Verbose output
  python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -v
        """
    )
    
    parser.add_argument("alien_path", 
                       help="Path to the file in Alien (e.g., alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root)")
    parser.add_argument("-d", "--download-dir", 
                       help="Directory to download files to (default: current directory)")
    parser.add_argument("-o", "--output", 
                       help="Local filename to save the file (default: filename from alien_path)")
    parser.add_argument("-v", "--verbose", 
                       action="store_true", 
                       help="Enable verbose output")
    parser.add_argument("--force", 
                       action="store_true", 
                       help="Force download even if file already exists")
    
    args = parser.parse_args()
    
    # Validate alien path
    if not args.alien_path.startswith("alien://"):
        print("Error: alien_path must start with 'alien://'")
        sys.exit(1)
    
    # Download the file
    success = download_file(
        alien_path=args.alien_path, 
        local_path=args.output, 
        download_dir=args.download_dir,
        verbose=args.verbose, 
        skip_existing=not args.force
    )
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
