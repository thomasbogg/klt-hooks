from default.settings import DEEPL_KEY, DEFAULT_LANGUAGE
from libraries.google.account import GoogleAccount
from libraries.google.mail.message import GoogleMailMessage
from libraries.google.mail.messages import GoogleMailMessages
from default.booking.booking import Booking
from default.google.mail.functions import new_email, send_email
from libraries.translator.deepl import Deepl


def new_guest_email(
    account: GoogleAccount = None,
    user: GoogleMailMessages = None, 
    subject: str = None, 
    booking: Booking = None
) -> tuple[GoogleMailMessages, GoogleMailMessage]:
    """
    Create a new email message for the guest.
    
    Args:
        account: The Google account to send from.
        user: The Google Mail user object if already authenticated.
        subject: The subject line for the email.
        booking: The booking object containing guest information.
        
    Returns:
        A tuple containing the user and the email message objects.
    """
    to = booking.guest.email
    name = booking.guest.firstName
    user, message = new_email(account=account, user=user, subject=subject, to=to, name=name)
    language = booking.guest.preferredLanguage
    if booking.guest.preferredLanguage != DEFAULT_LANGUAGE:
        message.translator = Deepl(authKey=DEEPL_KEY, targetLang=language)
    return user, message


def send_guest_email(
    user: GoogleMailMessages = None, 
    message: GoogleMailMessage = None, 
    bookingId: int = None
) -> GoogleMailMessage | None:
    """
    Send an email to the guest and track its status.
    
    Args:
        user: The Google Mail user object.
        message: The prepared email message object.
        bookingId: The booking ID associated with the email for tracking purposes.
        
    Returns:
        The sent email message object or None if sending failed.
    """
    return send_email(user=user, message=message, checkSent=(bookingId is None))


# Email creation functions
def new_guest_arrival_email(
    account: GoogleAccount = None,
    topic: str = None,
    booking: Booking = None
) -> tuple[GoogleMailMessages, GoogleMailMessage]:
    """
    Create a new email for guest arrival communication.
    
    Args:
        account: The Google account to use for sending the email
        topic: The topic of the email
        booking: The booking object containing guest information
        
    Returns:
        A tuple containing the email service and message objects
    """
    subject = f'{topic} for {booking.guest.lastName} to {booking.property.name}'
    return new_guest_email(account=account, subject=subject, booking=booking)