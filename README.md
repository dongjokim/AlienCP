# AlienCP - Smart File Download Script

A Python script to download files from ALICE's Alien file system using the `alien_cp` command with intelligent duplicate detection and size comparison.

## Prerequisites

Before using this script, ensure you have:

1. **ALICE software environment** properly installed
2. **alien_cp command** available in your PATH
3. **Valid ALICE credentials** configured (usually done via `alien-token-init`)

## Installation

1. Clone or download this repository
2. Make the script executable:
   ```bash
   chmod +x download_file.py
   ```

## Features

- **Smart duplicate detection**: Automatically checks if a file already exists locally
- **Size comparison**: Compares local and Alien file sizes to avoid unnecessary re-downloads
- **Download directory specification**: Organize downloads in a specific directory
- **Force download option**: Override duplicate detection when needed
- **Verbose output**: Detailed information about download process and file sizes

## Usage

### Basic Usage

Download a file to the current directory:

```bash
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root
```

### Download to Specific Directory

Download to a specific directory:

```bash
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data
```

### Advanced Usage

Download with custom filename in specific directory:

```bash
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -o my_data.root
```

Force re-download even if file exists:

```bash
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data --force
```

Enable verbose output:

```bash
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -v
```

### Command Line Options

- `alien_path`: Path to the file in Alien (required)
- `-d, --download-dir`: Directory to download files to (optional, defaults to current directory)
- `-o, --output`: Local filename to save the file (optional, defaults to filename from alien_path)
- `-v, --verbose`: Enable verbose output (optional)
- `--force`: Force download even if file already exists (optional)

## Examples

```bash
# Download a ROOT file to current directory
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root

# Download to specific directory
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data

# Download with custom name in specific directory
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -o experiment_data.root

# Download with verbose output to see size comparison
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data -v

# Force re-download even if file exists
python download_file.py alien:///alice/data/2022/LHC22c/000123456/raw/run123456_0001.root -d ./data --force
```

## Smart Download Behavior

The script intelligently handles file downloads:

1. **File exists with matching size**: Skips download and reports success
2. **File exists with different size**: Re-downloads the file
3. **File doesn't exist**: Downloads the file normally
4. **Cannot determine Alien size**: Re-downloads to be safe

## Error Handling

The script includes error handling for:

- Missing `alien_cp` command
- Invalid Alien paths (must start with `alien://`)
- Download failures
- File system errors
- Size comparison failures

## Notes

- The script automatically creates output directories if they don't exist
- Exit codes: 0 for success, 1 for failure
- Uses Python standard library only (no external dependencies required)
- Compatible with Python 3.6+

## Troubleshooting

If you encounter issues:

1. **"alien_cp command not found"**: Ensure ALICE software is properly installed and sourced
2. **Authentication errors**: Run `alien-token-init` to set up your credentials
3. **Permission denied**: Check that you have access to the requested Alien file
4. **File not found**: Verify the Alien path is correct and the file exists
