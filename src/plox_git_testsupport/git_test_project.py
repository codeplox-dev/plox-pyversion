"""A dummy class to represent a sample git project."""

import shutil
import subprocess
from pathlib import Path
from typing import List


class GitTestProject:
    def __init__(self, proj_dir: Path):
        """Create a new ``GitTestProject`` instance.

        Args:
            proj_dir (Path): Local path to project.
        """
        self.proj_dir = proj_dir

        ge = shutil.which("git")
        if ge is None:
            raise RuntimeError("Could not find required executable: git")
        self._ge = ge

        self._run_git_command("init")

    def _run_git_command(self, *args: str) -> List[str]:
        p = subprocess.run([self._ge, *args], cwd=self.proj_dir, stdout=subprocess.PIPE)

        if p.returncode != 0:
            raise RuntimeError(f"Failed to run git command: {args}")

        return p.stdout.decode("utf-8").splitlines()

    def add_content_as_file(self, filename: str, content: str, commit: bool = False) -> None:
        """Add a local file's contents via commit.

        Args:
            filename (str): Name of local file on disk to add.
            content (str): String content to write.
            commit (bool): Whether or not the change should be comitted.
        """
        with Path(self.proj_dir, filename).open(mode="w", encoding="utf-8") as outf:
            outf.write(content)

        self("add", str(filename))

        if commit:
            self("commit", "-m", f"added {filename}")

    def __call__(self, *args: str) -> List[str]:
        """Run a git command with a list of given args.

        Args:
            args (str): Set of CLI args to pass to git command.

        Returns:
            List[str]: STDOUT of the executed git command.
        """
        return self._run_git_command(*args)
