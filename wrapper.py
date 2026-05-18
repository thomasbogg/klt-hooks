from time import sleep
import traceback

from libraries.google.drives.file import GoogleDriveFile
from correspondence.self.functions import (
    new_email_to_self,
    send_email_to_self
)
from libraries.dates import dates
from default.google.drive.functions import (
    get_klt_management_directory_on_drive,
    reconnect,
    upload_local_file_to_drive
)
from default.settings import (
    DATABASE_IN_USE_EMAIL_FOLDER, 
    DATABASE_IN_USE_EMAIL_SUBJECT, 
    DATABASE_NAME, 
    DATABASE_PATH, 
    DEFAULT_ACCOUNT,
)
from libraries.utils import logwarning

#LOAD_START = dates.now()


def update(func):
    """
    Decorator for update functions to handle logging and error handling.
    
    Wraps functions to provide standardized logging at start and end,
    runtime tracking, and error handling with email notifications.
    
    Args:
        func: The function to wrap.
        
    Returns:
        The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            _contact_self(
                        subject=f'ERROR IN {func.__name__}',
                        body=str(traceback.format_exc(chain=False)))
    return wrapper


def pull_database(func):
    """
    Decorator for functions that need database access.
    
    Pulls the latest database from cloud storage before executing the function,
    then uploads the potentially modified database back to the cloud after execution.
    
    Args:
        func: The function to wrap.
        
    Returns:
        The wrapped function.
    """
    def wrapper(*args, **kwargs):

        pullDatabase = kwargs.get('pullDatabase', True)
        if not pullDatabase:
            return func(*args, **kwargs)
        
        while True:
            if not _current_update_message_exists():
                _contact_self(
                    subject=DATABASE_IN_USE_EMAIL_SUBJECT, 
                    body='Running update with database. This message will be automatically deleted when complete.')
                break
            logwarning('Cannot pull database as is it currently in use. Retrying in 1 minute...')
            sleep(60)
        
        driveFile = _get_database_file_on_drive()
        driveFile.download()

        func(*args, **kwargs)
        
        driveFile.connection =  reconnect()
        upload_local_file_to_drive(driveFile)
        
        _delete_current_update_messages()

    return wrapper


def _get_database_file_on_drive() -> GoogleDriveFile:
    """
    Get the database file from Google Drive.
    
    Locates the database file in the management directory on Google Drive.
    
    Returns:
        The database file on Google Drive.
        
    Raises:
        FileNotFoundError: If the database file is not found.
    """
    driveDirectory = get_klt_management_directory_on_drive('Database')
    driveFile = driveDirectory.file(name=DATABASE_NAME)
    if not driveFile.exists:
        raise FileNotFoundError(
            f'Database file not found in Drive Directory {driveDirectory.id}.')
    driveFile.path = DATABASE_PATH
    return driveFile


def _contact_self(subject: str, body: str) -> None:
    """
    Send an email to self with the given subject and body.
    
    Args:
        subject: The subject of the email.
        body: The body of the email.
        
    Returns:
        None
    """
    user, message = new_email_to_self(subject=subject)
    message.body.paragraph(body)
    send_email_to_self(user, message)


def _current_update_message_exists():
    from default.google.mail.functions import get_user
    messages = get_user(DEFAULT_ACCOUNT)
    messages.folder(DATABASE_IN_USE_EMAIL_FOLDER)
    messages.subject(DATABASE_IN_USE_EMAIL_SUBJECT)
    return len(messages.list) > 0


def _delete_current_update_messages():
    from default.google.mail.functions import get_user
    messages = get_user(DEFAULT_ACCOUNT)
    messages.folder(DATABASE_IN_USE_EMAIL_FOLDER)
    messages.subject(DATABASE_IN_USE_EMAIL_SUBJECT)
    for message in messages.list:
        message.delete()