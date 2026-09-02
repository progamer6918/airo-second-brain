"""
Controlled LLM worker placeholder.

Phase 1 boundary:
- receives approved package
- prepares handoff point
- does not invoke model directly
"""

from .queue_reader import QueueReader


class ControlledLLMWorker:
    def __init__(self, queue_path):
        self.reader = QueueReader(queue_path)

    def inspect(self):
        return self.reader.list_packages()
