from default.directory.functions import get_KLT_directory
from libraries.directory.directory import Directory
from default.settings import LOCAL

def clear_cache() -> None:
    """
    Clear cache files and resolve conflicts across the KLT directory.
    
    Removes selenium leftovers, pycache conflicted files, and cached update files.
    
    Returns:
        None
    """
    if not LOCAL:
        return None
    directory: Directory = get_KLT_directory()
    _delete_all_pycache_files(directory)


def _delete_all_pycache_files(directory: Directory) -> None:
    """
    Recursively delete conflicted files in all __pycache__ folders.
    
    Args:
        directory: The directory to search within.
        
    Returns:
        None
    """
    for subdirectory in directory.subdirectories:
        if subdirectory.name == '__pycache__': 
            subdirectory.delete()
        else:
            _delete_all_pycache_files(subdirectory)
    return None