from subprocess import CompletedProcess
from subprocess import run
import platform


def tee(command: str, log_path: str, **kwargs) -> CompletedProcess:
    if platform.system() == 'Windows':
        return tee_batch(command, log_path, **kwargs)
    else:
        return tee_posix(command, log_path, **kwargs)


def tee_powershell(powershell_command: str, log_path: str, **kwargs) -> CompletedProcess:
    return run(f'PowerShell -Command "{powershell_command} 2>&1 | Tee-Object -FilePath \\"{log_path}\\""', **kwargs)


def tee_batch(batch_command: str, log_path: str, **kwargs) -> CompletedProcess:
    return tee_powershell(f'CMD /C {batch_command}', log_path, **kwargs)


def tee_posix(shell_command: str, log_path: str, **kwargs) -> CompletedProcess:
    """
    TODO(hunhoekim): not tested.
    """
    return run(f'{shell_command} 2>&1 | tee "{log_path}"', **kwargs)


if __name__ == '__main__':
    tee_powershell('Write-Output \\"hello tee powershell by $Env:USERNAME\\"', 'my tee powershell console.log').check_returncode()
    tee_batch('echo hello tee batch by %USERNAME%', 'my tee batch console.log').check_returncode()
    tee('echo hello tee by %USERNAME%', 'my tee console.log').check_returncode()