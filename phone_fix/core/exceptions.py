"""
Domain exceptions for PhoneFix.
"""

class PhoneFixError(Exception):
    """Base exception for PhoneFix errors."""
    pass

class AdbNotFoundError(PhoneFixError):
    """Raised when ADB is not installed or cannot be found."""
    pass

class DeviceNotFoundError(PhoneFixError):
    """Raised when no Android device is connected."""
    pass

class DeviceUnauthorizedError(PhoneFixError):
    """Raised when connected device is in 'unauthorized' ADB state."""
    pass

class MultipleDevicesError(PhoneFixError):
    """Raised when multiple devices are detected and no specific serial was provided."""
    pass

class CommandExecutionError(PhoneFixError):
    """Raised when an ADB command fails unexpectedly."""
    def __init__(self, command: str, return_code: int, stderr: str):
        self.command = command
        self.return_code = return_code
        self.stderr = stderr
        super().__init__(f"Command '{command}' failed with exit code {return_code}: {stderr}")

class OptimizationError(PhoneFixError):
    """Raised when an optimization action fails."""
    pass
