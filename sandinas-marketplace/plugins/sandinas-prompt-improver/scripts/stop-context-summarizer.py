#!/usr/bin/env python3
"""
Stop hook context summarizer for Sandinas Prompt Improver.
Always outputs valid JSON with continue: false to prevent hook errors.
"""

import os
import re
import sys
import json


# Redirect stderr to avoid non-JSON output that breaks hook parsing
class NullWriter:
    def write(self, text): pass
    def flush(self): pass


sys.stderr = NullWriter()


def main():
    """Main entry point with robust error handling."""
    try:
        transcript = os.environ.get('ARGUMENTS', '')

        # ALWAYS return continue: false to allow session to close normally
        result = {"continue": False}

        if transcript:
            # Simple local analysis for Sandinas 4-point context
            has_project = bool(re.search(r'(proyecto|project|sandbox)', transcript, re.IGNORECASE))
            has_feature = bool(re.search(r'(feature|regla|business)', transcript, re.IGNORECASE))
            has_arch = bool(re.search(r'(arquitectura|architecture)', transcript, re.IGNORECASE))
            has_data = bool(re.search(r'(modelo|data|entity)', transcript, re.IGNORECASE))

            if all([has_project, has_feature, has_arch, has_data]):
                result["hookSpecificOutput"] = {
                    "additionalContext": "Sandinas context detected"
                }

        # CRITICAL: ensure_ascii=True prevents encoding issues
        # This print MUST execute for the hook to work
        print(json.dumps(result, ensure_ascii=True))
        return 0

    except Exception:
        # LAST RESORT: if everything fails, output minimal JSON
        # This ensures the hook never prevents session closure
        print(json.dumps({"continue": False}, ensure_ascii=True))
        return 0


if __name__ == '__main__':
    sys.exit(main())
