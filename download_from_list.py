#!/usr/bin/env python3
"""
Script to download AnalysisResults.root files from directories listed in downloadlist.txt
"""

import os
import sys
from pathlib import Path
from download_file import download_file

# Output directory for downloads
OutDir = "hyperloopOutputs"

def read_downloadlist(file_path):
    """
    Read the downloadlist.txt file and extract all columns for filename generation
    
    Args:
        file_path (str): Path to the downloadlist.txt file
        
    Returns:
        list: List of tuples containing (first_arg, second_arg, directory_path)
    """
    entries = []
    
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                # Split by whitespace
                columns = line.split()
                if len(columns) < 3:
                    print(f"Warning: Line {line_num} has less than 3 columns, skipping")
                    continue
                
                # Extract the three parts: first_arg, second_arg, directory_path
                first_arg = columns[0]
                second_arg = columns[1]
                directory = columns[-1]  # Last column is the directory path
                
                entries.append((first_arg, second_arg, directory))
                print(f"Found entry: {first_arg} | {second_arg} | {directory}")
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    return entries

def generate_filename(first_arg, second_arg, directory_path):
    """
    Generate filename in format: AnalysisResults_[first_arg]_[second_arg]_[last_two_numbers_from_directory]
    
    Args:
        first_arg (str): First argument from downloadlist
        second_arg (str): Second argument from downloadlist
        directory_path (str): Directory path from downloadlist (last column)
        
    Returns:
        str: Generated filename
    """
    import re
    
    # Extract all numbers from the directory path
    numbers = re.findall(r'\d+', directory_path)
    
    if len(numbers) >= 2:
        # Take the last two numbers from the directory path
        last_two_numbers = f"{numbers[-2]}_{numbers[-1]}"
    elif len(numbers) == 1:
        # If only one number, use it twice
        last_two_numbers = f"{numbers[0]}_{numbers[0]}"
    else:
        # Default if no numbers found
        last_two_numbers = "00_00"
    
    # Create filename
    filename = f"AnalysisResults_{first_arg}_{second_arg}_{last_two_numbers}.root"
    
    # Clean up filename by replacing problematic characters
    filename = filename.replace("/", "_").replace("\\", "_")
    
    return filename

def download_analysis_results(entries, download_dir=None, verbose=False):
    """
    Download AnalysisResults.root files from the given entries
    
    Args:
        entries (list): List of tuples containing (first_arg, second_arg, directory_path)
        download_dir (str, optional): Local directory to save files
        verbose (bool): Enable verbose output
    """
    if not entries:
        print("No entries found to download from")
        return
    
    # Create download directory if specified
    if download_dir:
        download_dir = Path(download_dir)
        download_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading files to: {download_dir}")
    
    success_count = 0
    total_count = len(entries)
    
    for i, (first_arg, second_arg, directory) in enumerate(entries, 1):
        print(f"\n[{i}/{total_count}] Processing entry:")
        print(f"  First arg: {first_arg}")
        print(f"  Second arg: {second_arg}")
        print(f"  Directory: {directory}")
        
        # Construct the full Alien path for AnalysisResults.root
        alien_path = f"alien://{directory}/AnalysisResults.root"
        
        # Generate custom filename
        filename = generate_filename(first_arg, second_arg, directory)
        print(f"  Generated filename: {filename}")
        
        # Determine local path
        if download_dir:
            local_path = download_dir / filename
        else:
            local_path = filename
        
        print(f"Downloading: {alien_path}")
        print(f"To: {local_path}")
        
        # Print the full alien_cp command
        full_command = f"alien_cp {alien_path} file://{os.path.abspath(local_path)}"
        print(f"Full command: {full_command}")
        
        # Download the file
        success = download_file(
            alien_path=alien_path,
            local_path=str(local_path),
            verbose=verbose,
            skip_existing=True
        )
        
        if success:
            success_count += 1
            print(f"✓ Successfully downloaded {filename}")
        else:
            print(f"✗ Failed to download {filename}")
    
    print(f"\n=== Download Summary ===")
    print(f"Total entries processed: {total_count}")
    print(f"Successful downloads: {success_count}")
    print(f"Failed downloads: {total_count - success_count}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download AnalysisResults.root files from directories listed in downloadlist.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download to current directory
  python download_from_list.py
  
  # Download to specific directory
  python download_from_list.py -d ./downloads
  
  # Verbose output
  python download_from_list.py -d ./downloads -v
  
  # Use custom downloadlist file
  python download_from_list.py -f my_list.txt -d ./downloads
        """
    )
    
    parser.add_argument("-f", "--file", 
                       default="downloadlist.txt",
                       help="Path to the downloadlist file (default: downloadlist.txt)")
    parser.add_argument("-d", "--download-dir", 
                       default=OutDir,
                       help=f"Directory to download files to (default: {OutDir})")
    parser.add_argument("-v", "--verbose", 
                       action="store_true", 
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Check if downloadlist file exists
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found")
        sys.exit(1)
    
    # Read entries from downloadlist
    print(f"Reading entries from: {args.file}")
    entries = read_downloadlist(args.file)
    
    if not entries:
        print("No valid entries found in the downloadlist file")
        sys.exit(1)
    
    # Download AnalysisResults.root files
    download_analysis_results(entries, args.download_dir, args.verbose)

if __name__ == "__main__":
    main()
