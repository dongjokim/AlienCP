# AlienCP - ALICE File Download Scripts

Simple Python scripts to download files from ALICE's Alien file system.

## What You Need

1. **ALICE software** installed and sourced
2. **alien_cp command** available
3. **Valid credentials** (run `alien-token-init`)

## Quick Start

### For Batch Downloads (Most Common)

1. **Add entries to `downloadlist.txt`**:
   ```
   CF_JetShape_NeNe_default_with_outliers LHC25af_pass1 /alice/cern.ch/user/a/alihyperloop/outputs/0049/494220/145539
   CF_JetShape_NeNe_xxx LHC25af_pass1 /alice/cern.ch/user/a/alihyperloop/outputs/0049/493316/145211
   ```

2. **Run the script**:
   ```bash
   # Default: downloads to hyperloopOutputs/
   python3 download_from_list.py -v
   
   # EOS directory: syncs to CERNBox automatically
   python3 download_from_list.py -d /eos/user/your_username/analysis_data -v
   ```

3. **Files get organized** with descriptive names:
   - `AnalysisResults_CF_JetShape_NeNe_default_with_outliers_LHC25af_pass1_494220_145539.root`
   - `AnalysisResults_CF_JetShape_NeNe_xxx_LHC25af_pass1_493316_145211.root`

### For Single File Downloads

```bash
python3 download_file.py alien:///alice/path/to/file.root -d ./downloads -v
```

## Commands

### download_from_list.py (Batch Downloads)
```bash
python3 download_from_list.py [options]

Options:
  -v, --verbose          Show detailed output and commands
  -d, --download-dir     Directory to save files (default: hyperloopOutputs)
  -f, --file            Custom downloadlist file (default: downloadlist.txt)
```

### download_file.py (Single Files)
```bash
python3 download_file.py alien_path [options]

Options:
  -d, --download-dir     Directory to save file
  -o, --output          Custom filename
  -v, --verbose         Show detailed output
  --force               Re-download even if file exists
```

## How It Works

- **Smart downloads**: Skips files that already exist with correct size
- **Progress tracking**: Shows `[1/2]`, `[2/2]` for multiple downloads
- **Command display**: Shows exact `alien_cp` commands being run
- **Auto-organization**: Creates directories and descriptive filenames

## Common Issues

| Problem | Solution |
|---------|----------|
| `alien_cp command not found` | Source ALICE software environment |
| Authentication errors | Run `alien-token-init` |
| `No valid entries found` | Check downloadlist.txt has 3 columns per line |
| Permission denied | Verify you have access to the Alien file |

## Examples

```bash
# Basic batch download
python3 download_from_list.py -v

# EOS/CERNBox sync
python3 download_from_list.py -d /eos/user/your_username/data -v

# Single file download
python3 download_file.py alien:///alice/path/file.root -d ./data -v

# Force re-download
python3 download_file.py alien:///alice/path/file.root --force -v
```

## File Format

**downloadlist.txt** format:
```
first_argument second_argument /alice/path/to/directory
```

Each line downloads `AnalysisResults.root` from the specified directory with a filename like:
`AnalysisResults_[first]_[second]_[numbers].root`