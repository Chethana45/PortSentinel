"""Safe process inspection and explicitly-confirmed termination."""
import psutil

def inspect_process(pid: int) -> dict:
    try:
        p = psutil.Process(pid)
        with p.oneshot():
            return {
                "pid": p.pid, "name": p.name(), "executable": p.exe(),
                "username": p.username(), "status": p.status(),
                "created": p.create_time(), "cmdline": p.cmdline()
            }
    except psutil.NoSuchProcess:
        raise ValueError(f"Process {pid} no longer exists")
    except psutil.AccessDenied:
        raise PermissionError(f"Access denied while inspecting process {pid}")

def terminate_process(pid: int, expected_name: str, confirmed: bool = False) -> dict:
    """Terminate only after explicit confirmation and PID/name revalidation.

    Refuses PID 0/1, the current process, and processes owned by another user.
    """
    if not confirmed:
        raise PermissionError("Explicit confirmation is required")
    if pid <= 1 or pid == psutil.Process().pid:
        raise PermissionError("Refusing to terminate a protected process")
    try:
        proc = psutil.Process(pid)
        if proc.name() != expected_name:
            raise ValueError("Process identity changed; refresh the scan before retrying")
        if proc.username() != psutil.Process().username():
            raise PermissionError("Refusing to terminate a process owned by another user")
        proc.terminate()
        try:
            proc.wait(timeout=3)
            return {"pid": pid, "terminated": True, "message": "Process terminated"}
        except psutil.TimeoutExpired:
            return {"pid": pid, "terminated": False, "message": "Termination requested; process is still exiting"}
    except psutil.NoSuchProcess:
        raise ValueError(f"Process {pid} no longer exists")
    except psutil.AccessDenied:
        raise PermissionError(f"Access denied while terminating process {pid}")
