"""
EARESMES Hermes CLI Provider Adapter — V1
=========================================
Controlled wrapper for official Hermes CLI execution.

Governance limits enforced:
  - Does NOT evaluate policy or approvals
  - Does NOT modify system or Hermes configuration
  - Wraps CLI invocation under explicit command request only
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Optional


class HermesProviderAdapter:
    """Controlled wrapper for official Hermes CLI execution."""

    def __init__(self, executable_path: Optional[str] = None) -> None:
        if executable_path:
            self.executable_path = Path(executable_path)
        else:
            local_bin = Path.home() / ".local" / "bin" / "hermes"
            which_bin = shutil.which("hermes")
            if which_bin:
                self.executable_path = Path(which_bin)
            elif local_bin.exists():
                self.executable_path = local_bin
            else:
                self.executable_path = Path("hermes")

    def check_availability(self) -> Tuple[bool, str]:
        """Check if Hermes executable is accessible."""
        if not self.executable_path.exists() and not shutil.which(str(self.executable_path)):
            return False, f"Hermes executable not found at {self.executable_path}"
        try:
            env = os.environ.copy()
            env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"
            res = subprocess.run(
                [str(self.executable_path), "--version"],
                capture_output=True,
                text=True,
                env=env,
                timeout=10,
            )
            if res.returncode == 0:
                return True, res.stdout.strip()
            return False, f"Hermes --version returned exit code {res.returncode}: {res.stderr.strip()}"
        except Exception as exc:
            return False, f"Hermes availability check failed: {exc}"

    def invoke_quiet(self, prompt: str, timeout: int = 120) -> Tuple[bool, str, str]:
        """
        Controlled non-interactive invocation of Hermes.
        Returns: (success: bool, stdout_output: str, error_msg: str)
        """
        avail, reason = self.check_availability()
        if not avail:
            return False, "", reason

        try:
            env = os.environ.copy()
            env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"
            res = subprocess.run(
                [str(self.executable_path), "chat", "-q", prompt],
                capture_output=True,
                text=True,
                env=env,
                timeout=timeout,
            )
            if res.returncode == 0:
                return True, res.stdout.strip(), ""
            return False, res.stdout.strip(), f"Hermes exit code {res.returncode}: {res.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return False, "", f"Hermes execution timed out after {timeout} seconds"
        except Exception as exc:
            return False, "", f"Hermes invocation error: {exc}"
