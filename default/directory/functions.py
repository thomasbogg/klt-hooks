import os

from settings import DIR
from libraries.directory.directory import Directory


def get_KLT_directory(localPath: str = '') -> Directory:
    """
    Get the KLT directory with an optional subdirectory path.
    
    Parameters:
        localPath: Optional subdirectory path to append to the KLT directory.
        
    Returns:
        Directory: A Directory object pointing to the KLT directory or subdirectory.
    """
    name: str = 'klt' if not localPath else os.path.basename(localPath)
    directory: Directory = Directory(path=os.path.join(DIR, localPath), name=name)
    return directory


def get_local_storage_directory(localPath: str = '') -> Directory:
    """
    Get the local storage cache directory with an optional subdirectory path.
    
    Parameters:
        localPath: Optional subdirectory path to append to the cache directory.
        
    Returns:
        Directory: A Directory object pointing to the local storage cache directory.
    """
    directory = get_KLT_directory(os.path.join('cache', localPath))
    return directory