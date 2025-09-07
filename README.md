# AlienCP - Smart File Download Scripts

Python scripts to download files from ALICE's Alien file system using the `alien_cp` command with intelligent duplicate detection and size comparison.

## Scripts Overview

- **`download_file.py`**: Download individual files from Alien
- **`download_from_list.py`**: Batch download AnalysisResults.root files from a downloadlist.txt file

## Prerequisites

Before using this script, ensure you have:

1. **ALICE software environment** properly installed
2. **alien_cp command** available in your PATH
3. **Valid ALICE credentials** configured (usually done via `alien-token-init`)

## Installation

1. Clone or download this repository
2. Make the scripts executable:
   ```bash
   chmod +x download_file.py
   chmod +x download_from_list.py
   ```

## Features

### Both Scripts Include:
- **Smart duplicate detection**: Automatically checks if a file already exists locally
- **Size comparison**: Compares local and Alien file sizes to avoid unnecessary re-downloads
- **Download directory specification**: Organize downloads in a specific directory
- **Force download option**: Override duplicate detection when needed
- **Verbose output**: Detailed information about download process and file sizes

### download_from_list.py Additional Features:
- **Batch processing**: Download multiple files from a downloadlist.txt file
- **Custom filename generation**: Creates descriptive filenames based on directory paths
- **Progress tracking**: Shows progress for multiple downloads
- **Full command display**: Shows the exact alien_cp commands being executed

## Usage

## download_file.py - Individual File Downloads

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

### Command Line Options for download_file.py

- `alien_path`: Path to the file in Alien (required)
- `-d, --download-dir`: Directory to download files to (optional, defaults to current directory)
- `-o, --output`: Local filename to save the file (optional, defaults to filename from alien_path)
- `-v, --verbose`: Enable verbose output (optional)
- `--force`: Force download even if file already exists (optional)

## download_from_list.py - Batch Downloads

### Setup

Create a `downloadlist.txt` file with entries in the format:
```
first_argument second_argument /alice/path/to/directory
```

Example:
```
CF_JetShape_NeNe_default_with_outliers LHC25af_pass1 /alice/cern.ch/user/a/alihyperloop/outputs/0049/494220/145539
CF_JetShape_NeNe_xxx LHC25af_pass1 /alice/cern.ch/user/a/alihyperloop/outputs/0049/493316/145211
```

### Basic Usage

Download all AnalysisResults.root files from downloadlist.txt to the default `hyperloopOutputs` directory:

```bash
python download_from_list.py
```

### Download to Custom Directory

```bash
python download_from_list.py -d ./my_downloads
```

### Verbose Output

```bash
python download_from_list.py -v
```

### Custom Downloadlist File

```bash
python download_from_list.py -f my_custom_list.txt -d ./downloads -v
```

### Command Line Options for download_from_list.py

- `-f, --file`: Path to the downloadlist file (default: downloadlist.txt)
- `-d, --download-dir`: Directory to download files to (default: hyperloopOutputs)
- `-v, --verbose`: Enable verbose output (optional)

### Filename Generation

The script automatically generates descriptive filenames in the format:
```
AnalysisResults_[first_arg]_[second_arg]_[last_two_numbers_from_directory].root
```

Example output filenames:
- `AnalysisResults_CF_JetShape_NeNe_default_with_outliers_LHC25af_pass1_494220_145539.root`
- `AnalysisResults_CF_JetShape_NeNe_xxx_LHC25af_pass1_493316_145211.root`

## Examples

### download_file.py Examples

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

### download_from_list.py Examples

```bash
# Download all files from downloadlist.txt to hyperloopOutputs directory
python download_from_list.py

# Download with verbose output to see full commands
python download_from_list.py -v

# Download to custom directory
python download_from_list.py -d ./my_analysis_data

# Use custom downloadlist file
python download_from_list.py -f my_experiments.txt -d ./results -v
```

## Smart Download Behavior

Both scripts intelligently handle file downloads:

1. **File exists with matching size**: Skips download and reports success
2. **File exists with different size**: Re-downloads the file
3. **File doesn't exist**: Downloads the file normally
4. **Cannot determine Alien size**: Re-downloads to be safe

### download_from_list.py Additional Behavior:
- **Progress tracking**: Shows `[1/2]`, `[2/2]` etc. for multiple downloads
- **Full command display**: Shows the exact `alien_cp` commands being executed
- **Automatic directory creation**: Creates the output directory if it doesn't exist
- **Batch processing**: Processes all entries in the downloadlist.txt file

## Error Handling

Both scripts include error handling for:

- Missing `alien_cp` command
- Invalid Alien paths (must start with `alien://`)
- Download failures
- File system errors
- Size comparison failures

### download_from_list.py Additional Error Handling:
- Invalid downloadlist.txt format
- Missing downloadlist.txt file
- Empty or malformed entries in downloadlist.txt
- Directory creation failures

## Notes

- Both scripts automatically create output directories if they don't exist
- Exit codes: 0 for success, 1 for failure
- Uses Python standard library only (no external dependencies required)
- Compatible with Python 3.6+
- `download_from_list.py` defaults to downloading to `hyperloopOutputs/` directory
- Filenames are automatically generated based on directory paths for better organization

## Troubleshooting

If you encounter issues:

1. **"alien_cp command not found"**: Ensure ALICE software is properly installed and sourced
2. **Authentication errors**: Run `alien-token-init` to set up your credentials
3. **Permission denied**: Check that you have access to the requested Alien file
4. **File not found**: Verify the Alien path is correct and the file exists

### download_from_list.py Specific Issues:

5. **"No valid entries found"**: Check your downloadlist.txt format - each line should have 3 columns
6. **"File not found"**: Ensure downloadlist.txt exists in the current directory or specify with `-f`
7. **"Less than 3 columns"**: Each line in downloadlist.txt must have: `first_arg second_arg /alice/path/to/directory`
8. **Download failures**: Use `-v` flag to see the exact alien_cp commands being executed
