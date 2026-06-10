from datetime import date

from default.google.drive.functions import get_klt_management_directory_on_drive
from default.google.drive.functions import reconnect as reconnect_drive
from default.settings import DATABASE_NAME, DATABASE_PATH
from libraries.database.database import Database as Databases
from default.database.database import Database
from libraries.google.drives.file import GoogleDriveFile
from default.database.rows.touristtax import Touristtax


def download_database(
    driveDirectory: str = 'Database', 
    name: str = DATABASE_NAME, 
    path: str = DATABASE_PATH
) -> None:
    """
    Download the database file from Google Drive to the local path.
    
    This function locates the database file in the management directory on Google Drive
    and downloads it to the specified local path for use in the application.
    
    Returns:
        None
    """
    drive = get_klt_management_directory_on_drive(driveDirectory)
    file = drive.file(name=name)
    if not file.exists:
        raise FileNotFoundError(
            f'Database file not found in Drive Directory {driveDirectory.id}.')
    file.path = path
    file.download()
    return file


def upload_database(
    file: GoogleDriveFile = None, 
    driveDirectory: str = 'Database', 
    name: str = DATABASE_NAME, 
    path: str = DATABASE_PATH
) -> None:
    """
    Upload the local database file to Google Drive.
    
    This function locates the database file in the management directory on Google Drive
    and uploads the local database file to it, overwriting the existing file.
    
    Returns:
        None
    """
    if file:
        file.connection = reconnect_drive()
        file.upload()
        return
    directory = get_klt_management_directory_on_drive(driveDirectory)
    file = directory.file(name=name)
    if not file.exists:
        raise FileNotFoundError(
            f'Database file {name} not found in Drive Directory "{directory.name}".')
    file.path = path
    file.upload()


def open_database(
    name: str = DATABASE_NAME, 
    path: str = DATABASE_PATH, 
    loadObject: Touristtax = Touristtax, 
    TEST: bool = False
) -> Database:
    """
    Get a connected database instance configured for Booking objects.
    
    Returns:
        Database: A connected database instance.
    """
    return Database(name=name, path=path, loadObject=loadObject, TEST=TEST).connect()


def last_database_update(path: str) -> str:
    """
    Get the timestamp of the last database update.
    
    Parameters:
        path: Path to the database file.
        
    Returns:
        str: The timestamp of the last update.
    """
    database = Databases(path=path).connect()
    database.runSQL('SELECT lastUpdated from bookings ORDER BY lastUpdated DESC LIMIT 1')
    result = database._cursor.fetchone()[0]
    database.close()
    return result


# Tourist Tax search functions
def search_touristtax_payments(
    database: Database = None, 
    start: date = None, 
    end: date = None
) -> Database:
    """
    Search for tourist tax payments in the database with optional filters.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        start: Optional start date filter.
        end: Optional end date filter.
        
    Returns:
        Database: Database object configured with the search query.
    """
    if not database:
        database = open_database()
    
    search = database
    search.touristtax.isPrimaryTable = True
    
    select = search.touristtax.select()
    select.date()
    select.orderId()
    select.paid()

    if start:
        where = search.touristtax.where()
        where.date().isGreaterThanOrEqualTo(start)
        search.touristtax.order().date()
        
    if end:
        where = search.touristtax.where()
        where.date().isLessThanOrEqualTo(end)
 
    return search


def get_touristtax_payment(
    database: Database = None, 
    id: int = None, 
    orderId: str = None
) -> Database | None:
    """
    Get a tourist tax payment by id or orderId.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        id: Optional tourist tax payment id.
        orderId: Optional order id.
        
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if id is None and orderId is None:
        return None
    
    search = search_touristtax_payments(database)
    where = search.touristtax.where()
    
    if id:
        where.id().isEqualTo(id)
    if orderId:
        where.orderId().isEqualTo(orderId)
    
    return search