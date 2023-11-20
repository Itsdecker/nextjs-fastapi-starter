import subprocess
import sys
import os


def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
        print(f"Successfully ran {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    # Get the directory where this script is located
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # List of scripts to run in order
    scripts = [
        'download_pdfs_from_drive.py',
        'pdf_to_csv.py',
        'write_to_sheet.py'
    ]

    for script in scripts:
        script_path = os.path.join(script_directory, script)
        run_script(script_path)

    print("All scripts completed successfully.")


if __name__ == "__main__":
    main()
