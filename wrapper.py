import traceback

from libraries.google.drives.file import GoogleDriveFile
from correspondence.self.functions import (
    new_email_to_self,
    send_email_to_self
)
from libraries.dates import dates
#from default.google.drive.functions import (
#    get_klt_management_directory_on_drive,
#    reconnect,
#    upload_local_file_to_drive
#)
from default.settings import (
    #CLOUD_UPDATE_EMAIL_FOLDER, 
    #CLOUD_UPDATE_EMAIL_SUBJECT, 
    #DATABASE_NAME, 
    #DATABASE_PATH, 
    DEFAULT_ACCOUNT,
    LOCAL,
)
#from libraries.interface.interface import Interface
from libraries.utils import logerror

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
        #interface = Interface(divider=90)
        #interface.divide()
        #sections = interface.subsections()
        #sections.log(f'NOW RUNNING: {func.__name__}')
        #start = dates.now()
     
        try:
            run = func(*args, **kwargs)
            #sections.log(run)    
        except Exception as e:
            _contact_self(
                        subject=f'ERROR IN {func.__name__}', 
                        body=str(traceback.format_exc(chain=False)))
            #_log_exception(sections)
     
        #end = dates.now()
        #sections.log(f'UPDATE runtime: {end - start}')
        #sections.log(f'TOTAL runtime: {end - LOAD_START}')
    return wrapper
#
#
#def pull_database(func):
#    """
#    Decorator for functions that need database access.
#    
#    Pulls the latest database from cloud storage before executing the function,
#    then uploads the potentially modified database back to the cloud after execution.
#    
#    Args:
#        func: The function to wrap.
#        
#    Returns:
#        The wrapped function.
#    """
#    def wrapper(*args, **kwargs):
#
#        pullDatabase = kwargs.get('pullDatabase', True)
#        if not pullDatabase:
#            return func(*args, **kwargs)
#        
#        if not LOCAL:
#            _contact_self(subject=CLOUD_UPDATE_EMAIL_SUBJECT, body=f'Started cloud update at {dates.now()}')
#        else:
#            if _current_update_message_exists():
#                logerror('Cannot pull database as Cloud Update Ongoing')
#                return
#        
#        interface = Interface(divider=90)
#        interface.divide()
#        sections = interface.subsections()
#        sections.log('Clearing cache and pulling database from CLOUD...')
#        
#        clear_cache_and_conflicts()
#        driveFile = _get_database_file_on_drive()
#        driveFile.download()
#        try: 
#            func(*args, **kwargs)
#        except Exception:
#            _log_exception(sections)
#        
#        sections.smallDivide()  
#        sections.log('Clearing cache and storing database on CLOUD...')
#        driveFile.connection =  reconnect()
#        upload_local_file_to_drive(driveFile)
#        clear_cache_and_conflicts()
#        interface.divide()
#
#        if not LOCAL:
#            _delete_current_update_messages()
#
#    return wrapper
#
#
#def _get_database_file_on_drive() -> GoogleDriveFile:
#    """
#    Get the database file from Google Drive.
#    
#    Locates the database file in the management directory on Google Drive.
#    
#    Returns:
#        The database file on Google Drive.
#        
#    Raises:
#        FileNotFoundError: If the database file is not found.
#    """
#    driveDirectory = get_klt_management_directory_on_drive('Database')
#    driveFile = driveDirectory.file(name=DATABASE_NAME)
#    if not driveFile.exists:
#        raise FileNotFoundError(
#            f'Database file not found in Drive Directory {driveDirectory.id}.')
#    driveFile.path = DATABASE_PATH
#    return driveFile
#
#
#def _log_exception(sections: Interface) -> None:
#    """
#    Log an exception to the console.
#    
#    Args:
#        sections: The interface subsections object used for logging.
#        
#    Returns:
#        None
#    """
#    sections.log('ERROR: Could not complete.')
#    sections.divide()
#    traceback.print_exc(chain=False)
#    sections.divide()
#
#
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


#def _current_update_message_exists():
#    from default.google.mail.functions import get_user
#    messages = get_user(DEFAULT_ACCOUNT)
#    messages.folder(CLOUD_UPDATE_EMAIL_FOLDER)
#    messages.subject(CLOUD_UPDATE_EMAIL_SUBJECT)
#    return len(messages.list) > 0
#
#
#def _delete_current_update_messages():
#    from default.google.mail.functions import get_user
#    messages = get_user(DEFAULT_ACCOUNT)
#    messages.folder(CLOUD_UPDATE_EMAIL_FOLDER)
#    messages.subject(CLOUD_UPDATE_EMAIL_SUBJECT)
#    for message in messages.list:
#        message.delete()