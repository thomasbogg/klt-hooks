from default.google.mail.functions import get_default_user, get_inbox, new_email
from settings import DEFAULT_ACCOUNT
from libraries.google.account import GoogleAccount
from libraries.google.mail.message import GoogleMailMessage
from libraries.google.mail.messages import GoogleMailMessages
from libraries.dates import dates


#######################################################
# EMAIL CREATION FUNCTIONS
#######################################################

def new_email_to_self(
        account: GoogleAccount = DEFAULT_ACCOUNT, 
        subject: str = None) -> tuple[GoogleMailMessages, GoogleMailMessage]:
    """
    Create a new email message to self.
    
    Args:
        account: The Google Account to send the email from
        subject: The subject of the email
        
    Returns:
        A tuple containing the Google Mail user and the email message
        
    Raises:
        ValueError: If the subject is not provided
    """
    if not subject:
        raise ValueError('No subject provided for email to self.')
    subject = f'{subject} - {dates.prettyDate()}'
    user = get_default_user() if account == DEFAULT_ACCOUNT else None
    user, message = new_email(
                            account=account, 
                            user=user,
                            subject=subject, 
                            to=account.emailAddress, 
                            name='Self'
    )
    message.greeting.formal()
    return user, message


def send_email_to_self(
        user: GoogleMailMessages = None, 
        message: GoogleMailMessage = None) -> None:
    """
    Send an email to self.
    
    Args:
        user: The Google Mail user to send the email from
        message: The email message to send
        
    Returns:
        None
        
    Raises:
        ValueError: If the message is not valid
    """
    if not message:
        raise ValueError('No message provided for email to self.')
    if not user:
        user = get_default_user()
    if not get_inbox(user=user, sender=user.account.emailAddress, subject=message.subject):
        message.send()
    return None