import regex as re
from time import sleep

from default.booking.booking import Booking
from default.database.database import Database
from default.database.functions import get_database, search_valid_bookings, search_updates
from default.google.mail.functions import get_default_user, get_inbox, new_email
from default.settings import DEFAULT_ACCOUNT
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


#######################################################
# BOOKING EMAIL FUNCTIONS
#######################################################

def new_bookings_email_to_self(
        account: GoogleAccount = DEFAULT_ACCOUNT, 
        subject: str = None, 
        bookings: list[Booking] = None) -> str:
    """
    Create a new email message to self with booking details.
    
    Args:
        account: The Google Account to send the email from
        subject: The subject of the email
        bookings: The list of bookings to include in the email
        
    Returns:
        A string indicating the email was sent
        
    Raises:
        ValueError: If the subject or bookings are not provided
    """
    if not bookings:
        raise ValueError('No bookings provided for bookings email to self.')
    
    user, message = new_email_to_self(account=account, subject=subject)
    if get_inbox(user=user, sender=user.account.emailAddress, subject=subject):
        return 'Email already sent to self.'
    
    body = message.body
    count = 0
    for booking in bookings:
        count += 1
        body.paragraph(f'{count}) {booking.__repr__()}')
   
    message.send()
    return 'Email sent to self.'


#######################################################
# SECURITY FUNCTIONS
#######################################################

def new_security_code_email_to_self(
        website: str = None, 
        account: GoogleAccount = DEFAULT_ACCOUNT, 
        code: str = None, 
        codeLength: int = 6) -> str:
    """
    Send a security code email to self.
    
    Args:
        website: The website for which the security code is requested
        account: The Google Account to send the email from
        code: The security code to include in the email
        codeLength: The length of the security code
        
    Returns:
        The security code received from the email
        
    Raises:
        ValueError: If the website or account is not provided
    """
    subject = f'Security Code Challenge for Login @ {website}'
    user, message = new_email_to_self(account=account, subject=subject)
    message.body.paragraph(f'Please reply with security code alone.')
    send_email_to_self(user, message)
    
    def _get_code_from_inbox(
            user: GoogleMailMessages, 
            sender: str, 
            subject: str, 
            codeLength: int, 
            count: int = 1, 
            read: list = None) -> tuple[str, list]:
        """
        Recursive function to get security code from inbox.
        
        Args:
            user: The Google Mail user to check inbox
            sender: The email address of the sender
            subject: The subject of the email to search for
            codeLength: The length of the security code
            count: The retry count
            read: List of messages that have been read
            
        Returns:
            Tuple containing the code and list of messages to delete
        """
        if read is None:
            read = []
            
        sleep(10 * count)
        messages = get_inbox(user, sender, subject)
        for message in messages:
            if subject not in message.subject:
                continue
            
            read.append(message)
            content = message.body.plain().body
            search = re.search(r'(\d{' + str(codeLength) + '})', content)
            if not search:
                continue
            
            return search.group(1), read
        count += 1
        return _get_code_from_inbox(user, sender, subject, codeLength, count, read)
    
    code, toDelete = _get_code_from_inbox(
                                        user, 
                                        account.emailAddress, 
                                        subject, 
                                        codeLength, 
                                        1, 
                                        [])
    for message in toDelete:
        message.delete()
    return code


def send_email_reminder_to_self_for_local_update_run(IS_EVENING_RUN: bool = False) -> None:
    """
    Send a test email to self when running the update locally.
    """    
    if not IS_EVENING_RUN:
        return
    
    updates_search = search_updates(
        start=dates.calculate(days=-2), end=dates.calculate(days=1))
   
    select = updates_search.updates.select()
    select.bookingId()
    select.messages()
    
    where = updates_search.updates.where()
    where.messages().isNotNullEmptyOrFalse()
    where.emailSent().isNullEmptyOrFalse()
    updates = updates_search.fetchall()

    database = get_database()
    vrboArrivals = get_vrbo_arrivals_in_28_days(database)
    database.close()
    
    messages = get_airbnb_reviews_box()
    toReview = []
    for message in messages:
        if message.date > dates.calculate(days=-3):
            continue
        toReview.append(message)

    if not updates and not toReview:
        updates_search.close()    
        return

    subject = "LOCAL UPDATE RUN REQUIRED"
    user, message = new_email_to_self(subject=subject)
    body = message.body

    for update in updates:
        body.paragraph(f'-- {update.bookingId}: {update.messages}')

    for arrival in vrboArrivals:
        body.paragraph(f'-- {arrival.id}: VRBO Arrival')
   
    for review in toReview:
        body.paragraph(f'-- {review.subject}')

    send_email_to_self(user, message)
    for update in updates:
        update.emailSent = True
        update.update()

    updates_search.close()    


def get_vrbo_arrivals_in_28_days(database: Database) -> list[Booking]:
    """
    Get upcoming VRBO bookings from the database.
    
    Parameters:
        database: Database connection
        
    Returns:
        List of Booking objects for     VRBO bookings
    """
    search = search_valid_bookings(database)
    
    where = search.details.where()
    where.enquirySource().isEqualTo('Vrbo')
    
    where = search.arrivals.where()
    where.date().isEqualTo(dates.calculate(days=28))
    
    select = search.guests.select()
    select.lastName()
    
    select = search.properties.select()
    select.vrboId()
    
    return search.fetchall()


def get_airbnb_reviews_box() -> list[GoogleMailMessage]:
    """
    Get messages from 'Airbnb Reviews' folder in default user's email

    Args:
        start (datetime.date): Start date for the search
        end (datetime.date): End date for the search

    Returns:
        list (GoogleMailMessage): Messages matching the given dates
    """
    search: GoogleMailMessages = get_default_user()
    search.folder('Airbnb Reviews')
    search.sender('automated@airbnb.com')
    return search.list