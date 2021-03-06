import subprocess
from typing import List
import logging

logger = logging.getLogger(__name__)


def execute_command(command: List[str]) -> str:
    res = subprocess.run(command, stdout=subprocess.PIPE)
    return res.stdout.decode("utf8")
