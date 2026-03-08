import os
import subprocess
import sys
import tempfile


def _lock_filepath(prefix: str) -> str:
    return os.path.join(tempfile.gettempdir(), f"blender_{prefix}.lock")


def _pid_exists(pid: int) -> bool:
    if pid <= 0:
        return False

    if sys.platform == "win32":
        # Windows
        try:
            r = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True,
                timeout=5,
            )

            return str(pid).encode("ascii") in r.stdout
        except subprocess.SubprocessError:
            return False
    else:
        # Other OS
        try:
            os.kill(pid, 0)

            return True
        except OSError:
            return False


def list_pids(prefix: str) -> list[str]:
    filepath = _lock_filepath(prefix)

    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.read().splitlines()

    return []


def register_pid(prefix: str):
    pids = list_pids(prefix)
    filepath = _lock_filepath(prefix)
    this_pid = os.getpid()

    if str(this_pid) not in pids:
        pids.append(str(this_pid))

        with open(filepath, "w") as f:
            f.write("\n".join(pids))


def unregister_pid(prefix: str):
    pids = list_pids(prefix)
    filepath = _lock_filepath(prefix)
    this_pid = os.getpid()

    alive_pids = []

    for pid in pids:
        if pid != str(this_pid) and _pid_exists(int(pid)):
            alive_pids.append(pid)

    if alive_pids:
        with open(filepath, "w") as f:
            f.write("\n".join(alive_pids))
    else:
        os.remove(filepath)
