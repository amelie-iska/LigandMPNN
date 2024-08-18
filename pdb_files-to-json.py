import os
import json
import argparse
import re
from pathlib import Path
import sys

def find_pdb_files(input_folder):
    pdb_files = {}
    input_folder = Path(input_folder).resolve()
    
    print(f"Input folder: {input_folder}")

    file_pattern = re.compile(r'output_\d{8}_\d{6}_\d+\.pdb$')

    for root, dirs, files in os.walk(input_folder):
        if 'traj' in dirs:
            dirs.remove('traj')
        for file in files:
            if file.endswith('.pdb') and file_pattern.match(file):
                full_path = Path(root) / file
                rel_path_str = str(full_path)
                pdb_files[rel_path_str] = ""
                print(f"Found PDB file: {rel_path_str}")
    
    print(f"Total PDB files found: {len(pdb_files)}")
    return pdb_files

def main():
    parser = argparse.ArgumentParser(description="Find PDB files and create a JSON file")
    parser.add_argument('--input_folder', required=True, help="Path to the input folder")
    parser.add_argument('--output_file', required=True, help="Path to the output JSON file")
    args = parser.parse_args()

    input_folder = Path(args.input_folder).resolve()
    if not input_folder.exists():
        print(f"Error: Input folder does not exist: {input_folder}")
        sys.exit(1)  # Exit with an error code

    pdb_files = find_pdb_files(args.input_folder)

    if not pdb_files:
        print(f"No PDB files found in {args.input_folder}")
        sys.exit(1)  # Exit with an error code

    with open(args.output_file, 'w') as f:
        json.dump(pdb_files, f, indent=4)

    print(f"JSON file created: {args.output_file}")
    print(f"Contents of JSON file:")
    with open(args.output_file, 'r') as f:
        print(json.dumps(json.load(f), indent=2))

if __name__ == "__main__":
    main()

# Example usage:
# python pdb_files2json.py --input_folder ../RFdiffusion/example_outputs/design_ppi/5era-chainDI --output_file ./runs/5era-DI_1100.json