import os
import regex as re
from ssl import SSLEOFError
import time

from libraries.google.drives.directory import GoogleDriveDirectory
from libraries.google.drives.file import GoogleDriveFile
from libraries.google.drives.permissions import GoogleDrivePermissions
from libraries.google.drives.utils import (
    GoogleAPIService,
    get_google_drives,
    get_google_drives_connection,
    get_refreshed_google_drives_connection
)
from libraries.dates import dates
from default.directory.functions import get_local_storage_directory
from settings import DEFAULT_ACCOUNT, LOCAL
from libraries.utils import log, logerror, logwarning


# Global variables
_DRIVES_CONNECTION = None
_DRIVE_DIRECTORY = None


def exception_handlers(func):
    """
    Decorator to handle SSL errors in a function.
    
    Parameters:
        func: The function to wrap with SSL error handling.
        
    Returns:
        The wrapped function that handles SSL exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SSLEOFError:
            logwarning('SSL Error occurred, reconnecting to Google Drive...')
           
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, (GoogleDriveFile, GoogleDriveDirectory)):
           
                    if (
                        arg.connection.connectionTime >= 
                        _DRIVES_CONNECTION.connectionTime
                    ):
                        reconnect()
                    arg.connection = _DRIVES_CONNECTION

            return func(*args, **kwargs)
        except TimeoutError:
            logwarning(
                'Timeout occurred, waiting 5 seconds and reconnecting '
                'to Google Drive...')
            time.sleep(5)
            reconnect()
            return func(*args, **kwargs)
        except BrokenPipeError:
            logwarning(
                'Broken pipe occurred during Google Drive transfer, '
                'reconnecting and retrying...')

            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, (GoogleDriveFile, GoogleDriveDirectory)):
                    reconnect()
                    arg.connection = _DRIVES_CONNECTION

            return func(*args, **kwargs)
    return wrapper


def connect() -> None:
    """
    Connect to Google Drive API.
    
    Establishes a connection to the Google Drive API using the default account
    and stores it in the global _DRIVES_CONNECTION variable.
    """
    global _DRIVES_CONNECTION
    _DRIVES_CONNECTION = get_google_drives_connection(DEFAULT_ACCOUNT)


def reconnect() -> GoogleAPIService:
    """
    Refresh the Google Drive connection.
    
    Calls the Google Drive API to refresh the connection for the default account
    and updates the global _DRIVES_CONNECTION variable.
    """
    global _DRIVES_CONNECTION
    _DRIVES_CONNECTION = get_refreshed_google_drives_connection(DEFAULT_ACCOUNT)
    return _DRIVES_CONNECTION


def get_klt_management_drive() -> GoogleDriveDirectory:
    """
    Get the KLT Management Drive.
    
    Connects to Google Drive if not already connected and retrieves the
    KLT Management Drive.
    
    Returns:
        GoogleDriveDirectory: The KLT Management Drive directory.
    """
    if not _DRIVES_CONNECTION:
        connect()
    global _DRIVE_DIRECTORY
    _DRIVE_DIRECTORY = get_google_drives(
        name='KLT Management Drive', 
        connection=_DRIVES_CONNECTION, 
        LOCAL=LOCAL
    )
    return _DRIVE_DIRECTORY


def get_file_by_id(id=None) -> GoogleDriveFile:
    """
    Get a file from Google Drive by its ID.
    
    Parameters:
        id: The ID of the file to retrieve.
        
    Returns:
        GoogleDriveFile: The file object retrieved from Google Drive.
    """
    if id is None:
        return logwarning(
            'ID not provided to get_file_id in '
            'default.google.drive.functions'
        )
    
    if not _DRIVES_CONNECTION:
        connect()

    return GoogleDriveFile(connection=_DRIVES_CONNECTION, id=id).get()


@exception_handlers
def get_klt_management_directory_on_drive(
        drivePath: str = '', 
        giveError: bool = True) -> GoogleDriveDirectory | None:
    """
    Get a directory on the KLT Management Drive.
    
    Parameters:
        drivePath: The path to the directory on the KLT Management Drive.
        giveError: Whether to raise an error if the directory is not found.
        
    Returns:
        GoogleDriveDirectory: The directory on the KLT Management Drive,
                             or None if not found and giveError is False.
        
    Raises:
        ValueError: If the directory is not found and giveError is True.
    """
    driveDirectory = (
        _DRIVE_DIRECTORY if _DRIVE_DIRECTORY else get_klt_management_drive()
    )

    for name in drivePath.split('/'):
        driveDirectory: GoogleDriveDirectory = driveDirectory.subdirectory(name=name)
    
        if not driveDirectory.exists:
            if giveError:
                raise ValueError(
                    f'Drive Directory not found: "{name}" in given path: {drivePath}')
            return None
    return driveDirectory


@exception_handlers
def get_todays_backup_directory_on_drive() -> GoogleDriveDirectory:
    """
    Get the backup directory for today on Google Drive.
    
    Creates a new directory with today's date if it doesn't exist.
    
    Returns:
        GoogleDriveDirectory: The backup directory for today.
    """
    backups: GoogleDriveDirectory = get_klt_management_directory_on_drive('Backups')
    todays: GoogleDriveDirectory = backups.subdirectory(name=dates.prettyDate())
    if not todays.exists:
        todays.create()
    return todays


@exception_handlers
def download_drive_file_to_local_storage(**kwargs) -> GoogleDriveFile | None:
    """
    Download a file from Google Drive to local storage.
    
    Parameters:
        **kwargs: Keyword arguments including:
            drivePath: The path to the file on Google Drive.
            localDirectory: The local directory to download the file to.
            filename: The name of the file to download.
            match: Whether to match the file name exactly (default: True).
            backupFolderOnDrive: Optional folder on Google Drive to back up the file to.
    
    Returns:
        GoogleDriveFile | None: The downloaded file, or None if the file isn't found.
    """
    drivePath: str = kwargs['drivePath']
    localDirectory: str = kwargs['localDirectory']
    filename: str = kwargs['filename']
    match: bool = kwargs.get('match', True)
    backupFolderOnDrive: str = kwargs.get('backupFolderOnDrive', None)
    driveDirectory = get_klt_management_directory_on_drive(drivePath)
 
    if match:
        driveFile: GoogleDriveFile = driveDirectory.file(name=filename)
        if not driveFile.exists:
            return logwarning(f'File not found: {filename}')
    else:
        driveFiles: list[GoogleDriveFile] = driveDirectory.files
        driveFiles = [file for file in driveFiles if filename in file.name]
     
        if len(driveFiles) > 1:
            return logerror(f'Multiple files found with name: {filename}')
        elif len(driveFiles) == 1:
            driveFile: GoogleDriveFile = driveFiles[0]
        else:
            return logerror(f'File not found: {filename}')
 
    localDirPath: str = get_local_storage_directory(localDirectory).path
    driveFile.path = os.path.join(localDirPath, driveFile.name)
    driveFile.download()

    if backupFolderOnDrive: 
        onDrive = get_todays_backup_directory_on_drive()
        directory = onDrive.subdirectory(name=backupFolderOnDrive)
    
        if not directory.exists:
            directory.create()
        if not directory.file(name=driveFile.name).exists:
            driveFile.backup(directory.id)
     
    return driveFile


@exception_handlers
def upload_local_file_to_drive(
    driveFile: GoogleDriveFile = None, 
    **kwargs) -> GoogleDriveFile:
    """
    Upload a local file to Google Drive.
    
    Parameters:
        driveFile: Optional Google Drive file object for updating an existing file.
        **kwargs: Keyword arguments including:
            drivePath: The path to the directory on Google Drive.
            localDirectory: The local directory to upload the file from.
            filename: The name of the file to upload.
            mimeType: Optional MIME type for the file.
    
    Returns:
        GoogleDriveFile: The uploaded file.
    """
    if driveFile:
        driveFile.update()
        return driveFile
   
    drivePath: str = kwargs['drivePath']
    localDirectory: str = kwargs['localDirectory']
    filename: str = kwargs['filename']
    driveDirectory = get_klt_management_directory_on_drive(drivePath)
    localDirPath = get_local_storage_directory(localDirectory).path
    path = os.path.join(localDirPath, filename)
    driveFile = driveDirectory.newFile(filename, path)
    driveFile.mimeType = kwargs.get('mimeType', default_mimetype())
    driveFile.upload()
    driveFile.get()
    return driveFile


@exception_handlers
def archive_files_from_previous_years(**kwargs) -> None:
    """
    Archive files from previous years in the KLT Management Drive.
    
    Parameters:
        **kwargs: Keyword arguments including:
            drivePath: The path to the directory on Google Drive.
            localDirectory: The local directory to archive the files to.
    """
    drivePath: str = kwargs['drivePath']
    localDirectory: str = kwargs['localDirectory']
    driveDirectory = get_klt_management_directory_on_drive(drivePath)
    
    log(f'ARCHIVING files from previous years in: {driveDirectory.name}')
 
    driveFiles: list[GoogleDriveFile] = driveDirectory.files
   
    if not driveFiles:
        return logwarning('No files found to archive.')    

    for driveFile in driveFiles:
        if not driveFile.name.endswith('.xlsx'):
            continue

        year = re.search(r'(20[0-4][0-9])', driveFile.name)
        if not year:
            continue

        year = year.group(1)
        if int(year) == dates.year():
            continue
        
        archiveDirectory = driveDirectory.subdirectory(name=year)
        if not archiveDirectory.exists:
            archiveDirectory.create()
      
        localDirPath: str = get_local_storage_directory(localDirectory).path
        driveFile.path = os.path.join(localDirPath, driveFile.name)
        driveFile.move(archiveDirectory.id)
    return log('ARCHIVING complete!')


@exception_handlers
def set_global_permissions(
    file: GoogleDriveFile, 
    role: str = 'reader') -> GoogleDriveFile:
    """
    Set global permissions for a file on Google Drive.
    
    Parameters:
        file: The Google Drive file object.
        role: The role to set for the permissions (default: 'reader').
        
    Returns:
        GoogleDriveFile: The file with the updated permissions.
    """
    permissions: GoogleDrivePermissions = file.permissions
    permissions.type = 'anyone'
    permissions.role = role
    permissions.create()
    return file


def default_mimetype() -> str:
    """
    Get the default MIME type for Excel spreadsheets.
    
    Returns:
        str: The default MIME type.
    """
    return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'