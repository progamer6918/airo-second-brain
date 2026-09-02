"""
Controlled execution package consumer.

Phase 3 boundary:
- consumes validated execution package metadata
- does not execute commands
- does not call LLM
"""

from pathlib import Path


class PackageConsumer:

    REQUIRED_FIELDS = [
        "job_id",
        "session_id",
        "project_id",
        "objective",
        "approval_status",
        "package_path",
    ]

    def validate(self, package):
        missing = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in package
        ]

        if missing:
            return {
                "valid": False,
                "missing": missing,
            }

        return {
            "valid": True,
            "job_id": package["job_id"],
        }

    def inspect_package_path(self, package_path):
        return Path(package_path).exists()
