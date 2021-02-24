import psutil


def waitIfNotInWindowsTerminal():
    """如果父进程不是WindowsTerminal，则等待一个输入"""
    process = psutil.Process()
    skip_process_names = ['py.exe', 'python.exe', 'python3.exe', 'pwsh.exe']
    while (process.name() in skip_process_names):
        process = process.parent()
    if (process.name() != 'WindowsTerminal.exe'):
        input('Press any key to continue.')