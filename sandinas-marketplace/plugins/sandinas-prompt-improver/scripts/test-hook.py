#!/usr/bin/env python3
"""
Test script for the prompt improver hook
"""

import json
import subprocess
import sys
import os

def test_hook():
    """Test the hook with sample input"""
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Test data
    test_input = {
        "prompt": "help me fix this bug"
    }

    # Convert to JSON string
    json_input = json.dumps(test_input)

    # Run the hook script
    if os.name == 'nt':  # Windows
        # Use the batch file wrapper
        result = subprocess.run(
            [os.path.join(script_dir, 'run_python.bat'),
             os.path.join(script_dir, 'improve-prompt.py')],
            input=json_input,
            text=True,
            capture_output=True
        )
    else:  # Linux/macOS
        result = subprocess.run(
            ['python3', os.path.join(script_dir, 'improve-prompt.py')],
            input=json_input,
            text=True,
            capture_output=True
        )

    print("Return code:", result.returncode)
    print("\nOutput:")
    print(result.stdout)

    if result.stderr:
        print("\nStderr:")
        print(result.stderr)

    # Parse the output to verify it's valid JSON
    try:
        output = json.loads(result.stdout)
        print("\n[OK] Valid JSON output")
        if 'hookSpecificOutput' in output:
            print("[OK] Contains hookSpecificOutput")
            print("[OK] Test passed!")
        else:
            print("[ERROR] Missing hookSpecificOutput")
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON output: {e}")

if __name__ == "__main__":
    test_hook()