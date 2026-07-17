import msvcrt

from .config import LOCK_FILE

_lock_handle = None


def acquire() -> bool:
    """Try to become the only running instance. Returns False if another instance holds the lock.

    Uses an OS-level file lock (msvcrt.locking) instead of just checking whether the
    lock file exists, so the lock is automatically released by Windows if the process
    crashes instead of leaving a stale file behind.
    """
    global _lock_handle

    _lock_handle = open(LOCK_FILE, 'w')
    try:
        msvcrt.locking(_lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        _lock_handle.close()
        _lock_handle = None
        return False

    return True
