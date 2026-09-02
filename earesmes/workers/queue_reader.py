"""
Controlled queue reader.

Phase 1:
- inspect approved execution packages
- no execution
- no model calls
"""

from pathlib import Path


class QueueReader:
    def __init__(self, queue_path):
        self.queue_path = Path(queue_path)

    def list_packages(self):
        if not self.queue_path.exists():
            return []

        return sorted(
            [
                p for p in self.queue_path.iterdir()
                if p.is_dir()
            ]
        )
