import traceback

from correspondence.self.functions import (
    new_email_to_self,
    send_email_to_self
)
from default.database.functions import download_database, upload_database
from default.clear import clear_cache


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
            return func(*args, **kwargs)
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
        driveFile = download_database()
        func(*args, **kwargs)
        upload_database(driveFile)
        clear_cache()
    return wrapper


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