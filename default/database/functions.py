from datetime import date

from libraries.database.database import Database as AllDatabases
from default.booking.booking import Booking
from default.database.database import Database
from default.guest.guest import Guest
from default.property.property import Property
from default.property.accountant import Accountant
from default.settings import TEST, VALID_BOOKING_STATUSES
from default.updates.updates import Update


def get_database() -> Database:
    """
    Get a connected database instance configured for Booking objects.
    
    Returns:
        Database: A connected database instance.
    """
    return Database(loadObject=Booking, TEST=TEST).connect()


def last_database_update(path: str) -> str:
    """
    Get the timestamp of the last database update.
    
    Parameters:
        path: Path to the database file.
        
    Returns:
        str: The timestamp of the last update.
    """
    database = AllDatabases(path=path).connect()
    database.runSQL('SELECT lastUpdated from bookings ORDER BY lastUpdated DESC LIMIT 1')
    result = database._cursor.fetchone()[0]
    database.close()
    return result


# Booking search functions
def search_bookings(database: Database = None, start: date = None, 
                   end: date = None, propertyName: str = None, 
                   noBlocks: bool = True) -> Database:
    """
    Search for bookings in the database with optional filters.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        start: Optional start date filter.
        end: Optional end date filter.
        propertyName: Optional property name filter.
        noBlocks: Whether to exclude booking blocks.
        
    Returns:
        Database: Database object configured with the search query.
    """
    if not database:
        database = get_database()
    
    search = database
    search.details.isPrimaryTable = True
    
    select = search.details.select()
    select.id()
    select.guestId()
    select.propertyId()
    
    arrivals = search.arrivals
    if start:
        arrivals.where().date().isGreaterThanOrEqualTo(start)
        arrivals.order().date()
        
    if end:
        arrivals.where().date().isLessThanOrEqualTo(end)
    
    if noBlocks:
       search.guests.where().lastName().isNotLike('BLOCK')
    
    set_property_name(search, propertyName)
    return search


def search_valid_bookings(database: Database = None, start: date = None, 
                         end: date = None, propertyName: str = None, 
                         noBlocks: bool = True) -> Database:
    """
    Search for bookings with valid booking status.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        start: Optional start date filter.
        end: Optional end date filter.
        propertyName: Optional property name filter.
        noBlocks: Whether to exclude booking blocks.
        
    Returns:
        Database: Database object configured with the search query.
    """
    search = search_bookings(database, start, end, propertyName, noBlocks)
    where = search.details.where()
    where.enquiryStatus().isIn(VALID_BOOKING_STATUSES)

    return search


def get_booking(database: Database = None, id: int = None, 
               PIMSId: int = None, platformId: str = None) -> Database | None:
    """
    Get a booking by id, PIMSId, or platformId.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        id: Optional booking id.
        PIMSId: Optional PIMS id.
        platformId: Optional platform id.
        
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if id is None and PIMSId is None and platformId is None:
        return None
    
    search = search_bookings(database, noBlocks=False)
    where = search.details.where()
    
    if id:
        where.id().isEqualTo(id)
    if PIMSId:
        where.PIMSId().isEqualTo(PIMSId)
    if platformId:
        where.platformId().isEqualTo(platformId)
    
    return search


# Property search functions
def search_properties() -> Database:
    """
    Search for properties in the database.
    
    Returns:
        Database: Database object configured with the property search query.
    """
    search: Database = Database(loadObject=Property, TEST=TEST).connect()
    properties = search.properties
    properties.isPrimaryTable = True
    
    select = properties.select()
    select.id()
    select.name()
    select.shortName()
    
    return search


def get_property(id: int = None, name: str = None) -> Database | None:
    """
    Get a property by id or name.
    
    Parameters:
        id: Optional property id.
        name: Optional property name.
        
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if not id and not name:
        return None
    
    search = search_properties()
    properties = search.properties
    properties.isPrimaryTable = True
    
    if id:
        properties.where().id().isEqualTo(id)
    
    set_property_name(search, name)
    
    return search


def get_accountant(id: int = None, company: str = None, name: str = None) -> Database:
    search: Database = Database(loadObject=Accountant, TEST=TEST).connect()
    
    select = search.propertyAccountants.select()
    select.all()
    
    where = search.propertyAccountants.where()
    if id:
        where.id().isEqualTo(id)
    if company:
        where.company().isEqualTo(company)
    if name:
        where.name().isEqualTo(name)
    
    return search


def get_property_price(
    name: str = None, 
    month: str = None, 
    year: int = None
) -> Database | None:
    """
    Get property price by name, month, and year.
    
    Parameters:
        database: The database connection to use. If None, creates a new connection.
        name: Optional property name.
        month: Optional month.
        year: Optional year.
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if not name and not month and not year:
        return None
    
    search = get_property(name=name)

    select = search.propertyPrices.select()
    select.month(month)
    
    where = search.propertyPrices.where()
    if year:
        where.year().isEqualTo(year)
    
    return search


def set_property_name(search: Database, propertyName: str | None) -> Database:
    """
    Set the property name filter for a search query.
    
    Parameters:
        search: The search database object.
        propertyName: The name of the property to filter by.
        
    Returns:
        Database: The updated search database object.
    """
    if propertyName is None:
        return search
    
    if len(propertyName) > 6:
        search.properties.where().name().isEqualTo(propertyName)
    else:
        search.properties.where().shortName().isEqualTo(propertyName)
    
    return search


def set_property_location(search: Database, **kwargs) -> Database:
    """
    Set property location filters for a search query.
    
    Parameters:
        search: The search database object.
        **kwargs: Keyword arguments for property locations:
            isBarracuda: Whether to include Quinta da Barracuda.
            isMonaco: Whether to include Clube do Monaco.
            isCorcovada: Whether to include Parque da Corcovada.
            isCerro: Whether to include Cerro Mar.
            
    Returns:
        Database: The updated search database object.
    """
    isNotIn = list()

    if 'isBarracuda' not in kwargs or not kwargs['isBarracuda']:
        isNotIn.append('Quinta da Barracuda')

    if 'isMonaco' not in kwargs or not kwargs['isMonaco']:
        isNotIn.append('Clube do Monaco')

    if 'isCorcovada' not in kwargs or not kwargs['isCorcovada']:
        isNotIn.append('Parque da Corcovada')

    if 'isCerro' not in kwargs or not kwargs['isCerro']:
        isNotIn.append('Cerro Mar')
    
    for location in isNotIn:
        search.properties.where().name().isNotLike(location)

    return search


# Guest search functions
def search_guests() -> Database:
    """
    Search for guests in the database.
    
    Returns:
        Database: Database object configured with the guest search query.
    """
    search: Database = Database(loadObject=Guest, TEST=TEST).connect()
    guests = search.guests
    guests.isPrimaryTable = True
    
    select = guests.select()
    select.id()
    select.firstName()
    select.lastName()
    
    return search


def get_guest(id: int = None, firstName: str = None, lastName: str = None) -> Database | None:
    """
    Get a guest by id, firstName, or lastName.
    
    Parameters:
        id: Optional guest id.
        firstName: Optional guest first name.
        lastName: Optional guest last name.
        
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if not id and not firstName and not lastName:
        return None
    
    search = search_guests()
    guests = search.guests
    
    if id:
        guests.where().id().isEqualTo(id)
    if firstName:
        guests.where().firstName().isEqualTo(firstName)
    if lastName:
        guests.where().lastName().isEqualTo(lastName)
    
    return search


# Update search functions
def search_updates(start: date = None, end: date = None) -> Database:
    """
    Search for updates in the database.
    
    Parameters:
        start: Optional start date filter.
        end: Optional end date filter.
        
    Returns:
        Database: Database object configured with the updates search query.
    """
    search: Database = Database(loadObject=Update, TEST=TEST).connect()
    updates = search.updates
    updates.isPrimaryTable = True
    
    select = updates.select()
    select.id()
    
    if start and end:
        where = updates.where()
        where.date().isGreaterThanOrEqualTo(start)
        where.date().isLessThanOrEqualTo(end)
    
    return search


def get_update(id: int = None, bookingId: int = None) -> Database | None:
    """
    Get an update by id or bookingId.
    
    Parameters:
        id: Optional update id.
        bookingId: Optional booking id.
        
    Returns:
        Database: Database object configured with the search query, or None if no criteria provided.
    """
    if not id and not bookingId:
        return None
    
    search = search_updates()
    where = search.updates.where()
    
    if id:
        where.id().isEqualTo(id)
    if bookingId:
        where.bookingId().isEqualTo(bookingId)
    
    return search


# Filter functions
def set_enquiry_sources(search: Database, **kwargs) -> Database:
    """
    Set enquiry source filters for a search query.
    
    Parameters:
        search: The search database object.
        **kwargs: Keyword arguments for enquiry sources:
            bookingCom: Whether to include Booking.com.
            airbnb: Whether to include Airbnb.
            vrbo: Whether to include Vrbo.
            direct: Whether to include Direct.
            kklj: Whether to include KKLJ.
            
    Returns:
        Database: The updated search database object.
    """
    isIn = list()
    isNotIn = list()

    if 'bookingCom' in kwargs:
        if kwargs['bookingCom']:
           isIn.append('Booking.com')
        else:
            isNotIn.append('Booking.com')
    
    if 'airbnb' in kwargs:
        if kwargs['airbnb']:
            isIn.append('Airbnb')
        else:
            isNotIn.append('Airbnb')
    
    if 'vrbo' in kwargs:
        if kwargs['vrbo']:
            isIn.append('Vrbo')
        else:
            isNotIn.append('Vrbo')
    
    if 'direct' in kwargs:
        if kwargs['direct']:
            isIn.append('Direct')
        else:
            isNotIn.append('Direct')
    
    if 'kklj' in kwargs:
        if kwargs['kklj']:
            isIn.append('KKLJ')
        else:
            isNotIn.append('KKLJ')
    
    where = search.details.where()
    
    if isIn:
        where.enquirySource().isIn(tuple(isIn))
    if isNotIn:
        where.enquirySource().isNotIn(tuple(isNotIn))
    
    return search


def set_valid_accounts_booking(search: Database) -> Database:
    """
    Set filter for valid account booking statuses.
    
    Parameters:
        search: The search database object.
        
    Returns:
        Database: The updated search database object.
    """
    search.details.where().enquiryStatus().isIn(
        VALID_BOOKING_STATUSES + ('Booking cancelled with fees',)
    )
    return search


def set_valid_management_booking(search: Database) -> Database:
    """
    Set filter for valid management booking statuses.
    
    Parameters:
        search: The search database object.
        
    Returns:
        Database: The updated search database object.
    """
    search.details.where().enquiryStatus().isIn(
        VALID_BOOKING_STATUSES + ('Booking confirmed as replacement',)
    )
    return search


def set_minimum_logging_criteria(search: Database) -> Database:
    """
    Set minimum criteria for logging booking in terminal for debugging.
    
    Parameters:
        search: The search database object.
        
    Returns:
        Database: The updated search database object.
    """
    select = search.details.select()
    select.id()
    select.enquirySource()
    select.enquiryStatus()

    select = search.properties.select()
    select.shortName()

    select = search.arrivals.select()
    select.date()

    select = search.departures.select()
    select.date()

    select = search.guests.select()
    select.firstName()
    select.lastName()
    
    return search