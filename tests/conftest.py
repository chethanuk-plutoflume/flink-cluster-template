import filecmp
import json
import os
import sys
import textwrap
from enum import Enum
from hashlib import sha1
from pathlib import Path
from typing import Dict

import copier
from copier.types import StrOrPath

PROJECT_TEMPLATE = Path(__file__).parent.parent

DATA = {
    "flink_version": "1.12.5",
    "python_version": "3.7.9",
    "enable_flink_sql": True,
    "enable_flink_operator": True
}



