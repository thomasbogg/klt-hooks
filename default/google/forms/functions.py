from typing import Any

from libraries.google.drives.file import GoogleDriveFile
from libraries.google.forms.form import GoogleForm
from libraries.google.forms.utils import (
    get_google_forms,
    get_google_forms_connection,
    create_new_form,
)
from default.google.drive.functions import get_klt_management_directory_on_drive
from default.settings import DEFAULT_ACCOUNT, TEST
from libraries.utils import (
    logerror,
    sublog,
)


# Global variables
_FORMS_CONNECTION = None


# Google Forms Connection functions
def connect() -> None:
    """
    Connect to Google Forms API.
    
    Establishes a connection to the Google Forms API using the default account
    and stores it in the global _FORMS_CONNECTION variable.
    """
    global _FORMS_CONNECTION
    _FORMS_CONNECTION = get_google_forms_connection(DEFAULT_ACCOUNT)


def reconnect() -> None:
    """
    Refresh the Google Forms connection.
    
    Calls the connect function to establish a fresh connection with Google Forms API.
    """
    connect()


# Google Forms retrieval functions
def get_form_file(name: str, drivePath: str = 'Forms') -> GoogleDriveFile | None:
    """
    Get a Google Form file from Drive.
    
    Parameters:
        name: The name of the form file to retrieve.
        drivePath: The path in Drive where the form is located.
        
    Returns:
        GoogleDriveFile | None: The form file if found, None otherwise.
    """
    driveDirectory = get_klt_management_directory_on_drive(drivePath)
    if not driveDirectory:
        logerror('Drive Directory not found.')
        return None

    driveFile = driveDirectory.file(name=name)
    if not driveFile.exists:
        logerror(f'Drive File not found: {name}')
        return None
  
    return driveFile


def get_form(id: str | GoogleDriveFile) -> GoogleForm:
    """
    Get a Google Form by ID or file object.
    
    Connects to Google Forms if not already connected, then retrieves the form.
    
    Parameters:
        id: Either a form ID string or a GoogleDriveFile object representing the form.
        
    Returns:
        GoogleForm: The requested form object.
    """
    if not _FORMS_CONNECTION:
        connect()
    if isinstance(id, GoogleDriveFile):
        id = id.id
    
    result: list[GoogleForm] = get_google_forms(
        id=id,
        connection=_FORMS_CONNECTION,
        TEST=TEST
    )
    return result[0]


def get_form_responses(
        id: str, 
        objectType: GoogleForm.Responses = None
) -> None | GoogleForm.Responses:
    """
    Get all responses for a Google Form.
    
    Parameters:
        id: The ID of the form to get responses from.
        objectType: Optional type to convert the responses into 
            (e.g., a custom class).
        
    Returns:
        list[dict]: A list of dictionaries containing response data.
    """
    responses: dict = get_form(id).rawResponses
    if not responses:
        return sublog('Form has NO answers...')
    if objectType:
        responses = objectType(responses)
        sublog(f'Form has {responses.length} answers.')
    return responses


def get_form_responder_uri(id: str) -> str:
    """
    Get the responder URI for a Google Form.
    
    Parameters:
        id: The ID of the form to get the responder URI for.
        
    Returns:
        str: The form's responder URI that can be shared with users.
    """
    return get_form(id).responderUri


def new_form(title, documentTitle) -> GoogleForm:
    if not _FORMS_CONNECTION:
        connect()
    form = create_new_form(
                        connection=_FORMS_CONNECTION, 
                        title=title, 
                        documentTitle=documentTitle, 
                        TEST=TEST)
    form.publish()
    return form