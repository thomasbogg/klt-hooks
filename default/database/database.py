from libraries.database.database import Database as DefaultDatabase
from libraries.database.table import Table
from default.booking.booking import Booking as LoadedBooking
from default.database.tables.accountants import Accountants
from default.database.tables.addresses import Addresses
from default.database.tables.arrivals import Arrivals
from default.database.tables.charges import Charges
from default.database.tables.departures import Departures
from default.database.tables.details import Details
from default.database.tables.emails import Emails
from default.database.tables.extras import Extras
from default.database.tables.forms import Forms
from default.database.tables.guests import Guests
from default.database.tables.managers import Managers
from default.database.tables.owners import Owners
from default.database.tables.prices import Prices
from default.database.tables.properties import Properties
from default.database.tables.sef import SEFDetails
from default.database.tables.specs import Specs
from default.database.tables.touristtax import Touristtax
from default.database.tables.updates import Updates
from default.guest.guest import Guest as LoadedGuest
from default.property.property import Property as LoadedProperty
from default.updates.updates import Update as LoadedUpdate


class Database(DefaultDatabase):
    """
    Extended database class for KLT application.
    
    This class extends the default database functionality with specific
    tables and methods for the KLT application.
    """

    def __init__(self, loadObject: LoadedBooking | LoadedProperty | LoadedGuest | LoadedUpdate = None, TEST: bool = False) -> None:
        """
        Initialize the database connection and set up the tables.
        
        Parameters:
            loadObject: The object type to load from the database.
            TEST: Boolean indicating if the database is in test mode.
        """
        super().__init__('KLT.db', 'KLT', TEST=TEST)
        self._load_object = loadObject

    def _table(self, name: str = None, object = None) -> Table:
        """
        Get or create a table object.
        
        Parameters:
            name: The name of the table.
            object: The table class to instantiate if not already in cache.
            
        Returns:
            The requested table object.
        """
        if name not in self._tables:
            self._tables[name] = object()
        return self._tables[name]
    
    @property
    def propertyAccountants(self) -> Accountants:
        """
        Get the property accountants table object.
        
        Returns:
            Accountants: The accountants table object.
        """
        return self._table(name='accountants', object=Accountants)
    
    @property
    def details(self) -> Details:
        """
        Get the booking details table object.
        
        Returns:
            Details: The details table object.
        """
        return self._table(name='bookings', object=Details)
    
    @property
    def guests(self) -> Guests:
        """
        Get the guests table object.
        
        Returns:
            Guests: The guests table object.
        """
        return self._table(name='guests', object=Guests)
    
    @property
    def properties(self) -> Properties:
        """
        Get the properties table object.
        
        Returns:
            Properties: The properties table object.
        """
        return self._table(name='properties', object=Properties)
    
    @property
    def arrivals(self) -> Arrivals:
        """
        Get the arrivals table object.
        
        Returns:
            Arrivals: The arrivals table object.
        """
        return self._table(name='arrivals', object=Arrivals)
    
    @property
    def departures(self) -> Departures:
        """
        Get the departures table object.
        
        Returns:
            Departures: The departures table object.
        """
        return self._table(name='departures', object=Departures)
    
    @property
    def charges(self) -> Charges:
        """
        Get the charges table object.
        
        Returns:
            Charges: The charges table object.
        """
        return self._table(name='charges', object=Charges)
    
    @property
    def extras(self) -> Extras:
        """
        Get the extras table object.
        
        Returns:
            Extras: The extras table object.
        """
        return self._table(name='extras', object=Extras)

    @property
    def emails(self) -> Emails:
        """
        Get the emails table object.
        
        Returns:
            Emails: The emails table object.
        """
        return self._table(name='emails', object=Emails)
    
    @property
    def forms(self) -> Forms:
        """
        Get the forms table object.
        
        Returns:
            Forms: The forms table object.
        """
        return self._table(name='forms', object=Forms)
    
    @property
    def touristtax(self) -> Touristtax:
        """
        Get the tourist tax table object.
        
        Returns:
            Touristtax: The tourist tax table object.
        """
        return self._table(name='touristtax', object=Touristtax)
    
    @property
    def propertyOwners(self) -> Owners:
        """
        Get the property owners table object.
        
        Returns:
            Owners: The owners table object.
        """
        return self._table(name='owners', object=Owners)
    
    @property
    def propertySEFDetails(self) -> SEFDetails:
        """
        Get the property sef details table object.
        
        Returns:
            SEFDetails: The property sef details table object.
        """
        return self._table(name='SEFDetails', object=SEFDetails)
    
    @property
    def propertySpecs(self) -> Specs:
        """
        Get the property specifications table object.
        
        Returns:
            Specs: The property specifications table object.
        """
        return self._table(name='specs', object=Specs)
    
    @property
    def propertyPrices(self) -> Prices:
        """
        Get the property prices table object.
        
        Returns:
            Prices: The property prices table object.
        """
        return self._table(name='prices', object=Prices)
    
    @property
    def propertyManagers(self) -> Managers:
        """
        Get the property managers table object.
        
        Returns:
            Managers: The property managers table object.
        """
        return self._table(name='managers', object=Managers)
    
    @property
    def propertyAddresses(self) -> Addresses:
        """
        Get the property addresses table object.
        
        Returns:
            Addresses: The property addresses table object.
        """
        return self._table(name='addresses', object=Addresses)
    
    @property
    def updates(self) -> Updates:
        """
        Get the updates table object.
        
        Returns:
            Updates: The updates table object.
        """
        return self._table(name='updates', object=Updates)
    
    def fetchall(self) -> list[LoadedBooking | LoadedProperty | LoadedGuest | LoadedUpdate]:
        """
        Fetch all records from the database and load them into the specified object type.
        
        Returns:
            A list of LoadedBooking, LoadedProperty, LoadedGuest, or LoadedUpdate objects.
        """
        return super().fetchall(self._load_object)
    
    def fetchone(self) -> LoadedBooking | LoadedProperty | LoadedGuest | LoadedUpdate | None:
        """
        Fetch a single record from the database and load it into the specified object type.
        
        Returns:
            A LoadedBooking, LoadedProperty, LoadedGuest, LoadedUpdate object, or None if no record is found.
        """
        return super().fetchone(self._load_object)