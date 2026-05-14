from datetime import date
from ssl import SSLEOFError, SSLError

from libraries.google.account import GoogleAccount
from libraries.google.connect import GoogleAPIService
from libraries.google.mail.message import GoogleMailMessage
from libraries.google.mail.messages import GoogleMailMessages
from libraries.google.mail.utils import (
    get_google_mail_connection,
    get_google_mail_user,
    get_refreshed_google_mail_connection
)
from libraries.dates import dates
from settings import DEFAULT_ACCOUNT
from libraries.utils import logwarning


# Global variables
_MAIL_CONNECTION = None
_MAIL_USER = None


def ssl_exception_handler(func):
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
        except (SSLEOFError, SSLError) as e:
            logwarning(
                f'SSL error in Google Mail call {func.__name__}, reconnecting and retrying once: {e}'
            )
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, (GoogleMailMessages, GoogleMailMessage)):
                    if (
                        arg.connection.connectionTime >= 
                        _MAIL_CONNECTION.connectionTime
                    ):
                        reconnect()
                    arg.connection = _MAIL_CONNECTION
            return func(*args, **kwargs)
    return wrapper


# Google Mail Connection functions
def connect() -> None:
    """
    Connect to Google Mail API.
    
    Establishes a connection to the Google Mail API using the default account
    and stores it in the global _MAIL_CONNECTION variable.
    """
    global _MAIL_CONNECTION
    _MAIL_CONNECTION = get_google_mail_connection(DEFAULT_ACCOUNT)


def reconnect() -> None:
    """
    Refresh the Google Mail connection.
    
    Calls the Google Mail API to refresh the connection for the default account
    and updates the global _MAIL_CONNECTION variable.
    """
    global _MAIL_CONNECTION
    _MAIL_CONNECTION = get_refreshed_google_mail_connection(DEFAULT_ACCOUNT)


# User retrieval functions
def get_user(account: GoogleAccount) -> GoogleMailMessages:
    """
    Get the Google Mail user for the given account.
    
    Parameters:
        account: The Google account to use for accessing mail.
        
    Returns:
        GoogleMailMessages: Object for interacting with the user's mailbox.
        
    Raises:
        ValueError: If the Google Mail user is not found for the account.
    """
    connection: GoogleAPIService = get_google_mail_connection(account)
    user: GoogleMailMessages = get_google_mail_user(account, connection)
    if not user:
        raise ValueError(f'Google Mail user not found for account {account}.')
    return user


def get_default_user() -> GoogleMailMessages:
    """
    Get the default Google Mail user.
    
    Connects to Google Mail if not already connected and retrieves the 
    default user based on DEFAULT_ACCOUNT settings.
    
    Returns:
        GoogleMailMessages: Object for the default user.
    """
    if not _MAIL_CONNECTION:
        connect()
    global _MAIL_USER
    _MAIL_USER = get_google_mail_user(
        DEFAULT_ACCOUNT, 
        _MAIL_CONNECTION
    )
    return _MAIL_USER


# Email retrieval functions
@ssl_exception_handler
def get_inbox(
    user: GoogleMailMessages | None = None, 
    sender: str | None = None, 
    subject: str | None = None
) -> list[GoogleMailMessage]: 
    """
    Get emails from the inbox with optional filters.
    
    Parameters:
        user: The Google Mail user object, or None to use default user.
        sender: Optional filter for sender's email address.
        subject: Optional filter for email subject.
        
    Returns:
        list[GoogleMailMessage]: Email messages matching the criteria.
    """
    if not user or not isinstance(user, GoogleMailMessages):
        user = _MAIL_USER if _MAIL_USER else get_default_user()
    return user.inbox().sender(sender).subject(subject).list


@ssl_exception_handler
def get_sent(
    user: GoogleMailMessages | None = None, 
    subject: str | None = None, 
    to: str | None = None, 
    start: date | None = None, 
    end: date | None = None
) -> list[GoogleMailMessage]:
    """
    Get sent emails with optional filters.
    
    Parameters:
        user: The Google Mail user object, or None to use default user.
        subject: Optional filter for email subject.
        to: Optional filter for recipient's email address.
        start: Optional start date for filtering emails.
        end: Optional end date for filtering emails.
        
    Returns:
        list[GoogleMailMessage]: Sent email messages matching the criteria.
    """
    if not user or not isinstance(user, GoogleMailMessages):
        user = _MAIL_USER if _MAIL_USER else get_default_user()
    return user.sent().subject(subject).to(to).start(start).end(end).list


# Email creation and sending functions
def new_email(
    account: GoogleAccount | None = None, 
    user: GoogleMailMessages | None = None, 
    subject: str | None = None, 
    to: str | None = None, 
    name: str | None = None
) -> tuple[GoogleMailMessages, GoogleMailMessage]:
    """
    Create a new email message.
    
    Parameters:
        account: The Google account to use, or None to use default account.
        user: The Google Mail user object, or None to use default user.
        subject: The subject of the email.
        to: The recipient's email address.
        name: The recipient's name for the greeting.
        
    Returns:
        tuple[GoogleMailMessages, GoogleMailMessage]: 
            A tuple containing (user, message) objects.
        
    Raises:
        ValueError: If the user or account is not valid.
    """
    if not user and not account:
        user = _MAIL_USER if _MAIL_USER else get_default_user()
    
    elif not user:
        if not isinstance(account, GoogleAccount):
            raise ValueError(
                f'Account provided for new email is not GoogleAccount: {type(account)}.')
       
        user = get_user(account)
    
    elif not isinstance(user, GoogleMailMessages):
        raise ValueError(
            f'User provided for new email is not GoogleMailMessages: {type(user)}.')
    
    message: GoogleMailMessage = user.message()
    message.subject = subject
    message.to = to
    message.greeting.name = name
    message.signature.name = user.account.name
    message.signature.details = user.account.details
    message.sender = user.account.emailAddress
    return user, message


@ssl_exception_handler
def send_email(
    user: GoogleMailMessages | None = None, 
    message: GoogleMailMessage | None = None, 
    checkSent: bool = False
) -> GoogleMailMessage | None:
    """
    Send an email, optionally checking if it was already sent.
    
    Parameters:
        user: The Google Mail user object, or None to use default user.
        message: The email message to send.
        checkSent: Whether to check if a similar message was already sent recently.
        
    Returns:
        GoogleMailMessage | None: The sent message object, or None if the message 
                                 was already sent and checkSent is True.
        
    Raises:
        ValueError: If no message is provided.
    """
    if not message:
        raise ValueError('No message provided to send email.')
    
    if checkSent:
        if not user or not isinstance(user, GoogleMailMessages):
            user = _MAIL_USER if _MAIL_USER else get_default_user()
    
        sent: list[GoogleMailMessage] = get_sent(
            user, 
            message.subject, 
            message.to, 
            dates.calculate(days=-1), 
            dates.calculate(days=1)
        )
        if sent:
            message.clear_recipients()
            return None
    
    return message.send()