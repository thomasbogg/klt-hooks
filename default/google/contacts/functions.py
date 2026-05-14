from libraries.google.contacts.person import GooglePerson
from libraries.google.contacts.utils import (
    get_google_contacts,
    get_google_contacts_connection,
    new_google_contact
)
from default.settings import DEFAULT_ACCOUNT
from libraries.utils import logerror


# Global variables
_CONTACTS_CONNECTION = None


def connect() -> None:
    """
    Connect to Google Contacts API.
    
    Establishes a connection to the Google Contacts API using the default account
    and stores it in the global _CONTACTS_CONNECTION variable.
    """
    global _CONTACTS_CONNECTION
    _CONTACTS_CONNECTION = get_google_contacts_connection(DEFAULT_ACCOUNT)


def reconnect() -> None:
    """
    Refresh the Google Contacts connection.
    
    Calls connect() to establish a fresh connection to the Google Contacts API.
    """
    connect()


def get_contacts(name: str) -> list[GooglePerson]:
    """
    Get Google Contacts matching a name.
    
    Parameters:
        name: The name of the contact to search for.
        
    Returns:
        A list of GooglePerson objects representing the matching contacts.
        
    Raises:
        Error logged if no name is provided.
    """
    if not name:
        return logerror('No name provided for contact search.')
    
    if not _CONTACTS_CONNECTION:
        connect()
        
    contacts: list[GooglePerson] = get_google_contacts(
        name=name, 
        connection=_CONTACTS_CONNECTION
    )
    return contacts


def create_contact(
    firstName: str | None = None,
    lastName: str | None = None,
    emailAddress: str | None = None,
    phoneNumber: str | None = None,
    **kwargs
) -> GooglePerson:
    """
    Create a new Google Contact.
    
    Parameters:
        firstName: The first name of the contact.
        lastName: The last name of the contact.
        emailAddress: The email address of the contact.
        phoneNumber: The phone number of the contact.
        **kwargs: Additional arguments that may include 'phone' or 'email'.
        
    Returns:
        A GooglePerson object representing the created contact.
        
    Raises:
        ValueError: If first name, last name, or phone number is not provided.
    """
    if not phoneNumber:
        phoneNumber = kwargs.get('phone', None)
        
    if not emailAddress:
        emailAddress = kwargs.get('email', None)
        
    if not (firstName and lastName) or not phoneNumber:
        raise ValueError('No first name and last name, or phone provided for contact creation.')
    
    if not _CONTACTS_CONNECTION:
        connect()
        
    contact: GooglePerson = new_google_contact(
        firstName=firstName,
        lastName=lastName,
        emailAddress=emailAddress,
        phoneNumber=phoneNumber,
        connection=_CONTACTS_CONNECTION
    )
    return contact