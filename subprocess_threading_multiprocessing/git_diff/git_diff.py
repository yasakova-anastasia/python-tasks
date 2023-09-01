import subprocess
import typing as tp
from pathlib import Path


def get_changed_dirs(git_path: Path, from_commit_hash: str, to_commit_hash: str) -> tp.Set[Path]:
    """
    Get directories which content was changed between two specified commits
    :param git_path: path to git repo directory
    :param from_commit_hash: hash of commit to do diff from
    :param to_commit_hash: hash of commit to do diff to
    :return: sequence of changed directories between specified commits
    """
    diff = subprocess.check_output(['git', 'diff', '--name-only',
                                   from_commit_hash + '..' + to_commit_hash], cwd=git_path)
    diff_str = diff.decode('utf-8').split("\n")[:-1]
    res = []
    for path in diff_str:
        res.append(Path(git_path, path).parent)

    return set(res)
