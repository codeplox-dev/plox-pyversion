# -*- coding: utf-8 -*-
import shutil
import subprocess
from pathlib import Path
from typing import List


class GitTestProject:

    def __init__(self, proj_dir: Path):
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
        with Path(self.proj_dir, filename).open(mode="w", encoding="utf-8") as outf:
            outf.write(content)

        self("add", str(filename))

        if commit:
            self("commit", "-m", f"added {filename}")

    def __call__(self, *args: str) -> List[str]:
        return self._run_git_command(*args)

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4
