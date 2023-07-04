import os
import sys

CURRENT_DIR = os.path.dirname(__file__).replace('\\','/')
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
