#!/usr/bin/env python3
"""
CCPA Guardian - Production Entry Point
Usage:
    python run.py         # Start interactive CLI
    python run.py --api   # Start FastAPI Web Server
"""
import os
import sys
import argparse

# Ensure the package is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ccpa_guardian.main import interactive_mode
from ccpa_guardian.api import run_api

def main():
    parser = argparse.ArgumentParser(description="CCPA Guardian RAG System")
    parser.add_argument("--api", action="store_true", help="Run as FastAPI server")
    args = parser.parse_args()

    try:
        if args.api:
            print("Starting Web API...")
            run_api()
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
