from libraries.database.column import Column
from libraries.database.database import Database
from libraries.database.table import Table
from libraries.dates import dates
from default.settings import DEFAULT_LANGUAGE


def create_database() -> Database:
    """
    Create and initialize the KLT database with all required tables.
    
    Returns:
        Database: The connected database instance.
    """
    database = Database('KLT.db', 'KLT').connect()
    create_addresses_table(database)
    create_managers_table(database)
    create_owners_table(database)  
    create_accountants_table(database)
    create_prices_table(database)
    create_properties_table(database)
    create_specs_table(database)
    create_sef_table(database)
    create_guests_table(database)
    create_bookings_table(database)
    create_arrivals_table(database)
    create_departures_table(database)
    create_charges_table(database)
    create_extras_table(database)
    create_forms_table(database)
    create_emails_table(database)
    create_updates_table(database)
    create_touristtax_table(database)
    return database


def create_addresses_table(database: Database) -> Database:
    """
    Create the propertyAddresses table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertyAddresses')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='location', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='street', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='coordinates', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='map', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='directions', tablename=table.name, dataType='text')
    table.columns = Column(name='nearestBins', tablename=table.name, dataType='text')
    table.columns = Column(name='nearestCornerShop', tablename=table.name, dataType='text')
    table.columns = Column(name='nearestSupermarket', tablename=table.name, dataType='text')
    table.create()
    return database


def create_managers_table(database: Database) -> Database:
    """
    Create the propertyManagers table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertyManagers')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='company', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='name', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='email', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='phone', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='maintenance', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='maintenancePhone', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='maintenanceEmail', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='liaison', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='liaisonPhone', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='liaisonEmail', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='cleaning', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='cleaningPhone', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='cleaningEmail', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='finance', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='financeEmail', tablename=table.name, dataType='text').notNull()
    table.create()
    return database


def create_owners_table(database: Database) -> Database:
    """
    Create the propertyOwners table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertyOwners')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='name', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='email', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='phone', tablename=table.name, dataType='text').unique()
    table.columns = Column(name='nifNumber', tablename=table.name, dataType='text').unique()
    table.columns = Column(name='defaultClean', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='defaultMeetGreet', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='takesEuros', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='takesPounds', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='wantsAccounting', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='cleansAreInvoiced', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='rentalCommissionsAreInvoiced', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='isPaidRegularly', tablename=table.name, dataType='boolean').notNull()
    table.create()
    return database


def create_accountants_table(database: Database) -> Database:
    """
    Create the propertyAccountants table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertyAccountants')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='company', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='name', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='email', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='phone', tablename=table.name, dataType='text').notNull().unique()
    table.create()
    return database


def create_prices_table(database: Database) -> Database:
    """
    Create the propertyPrices table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertyPrices')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='year', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='name', tablename=table.name, dataType='text').notNull()
    for month in dates.stringMonths():
        table.columns = Column(name=month.lower(), tablename=table.name, dataType='real').notNull()
    table.columns = Column(name='festive', tablename=table.name, dataType='real').notNull()
    table.columns = Column(name='earlyWinterMonthlyRate', tablename=table.name, dataType='real').notNull()
    table.columns = Column(name='lateWinterMonthlyRate', tablename=table.name, dataType='real').notNull()
    table.create()
    return database


def create_properties_table(database: Database) -> Database:
    """
    Create the properties table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='properties')
    table.columns = Column(database, 'id', table.name, 'integer').primaryKey()
    table.columns = Column(name='name', tablename=table.name, dataType='text').notNull().unique()
    table.columns = Column(name='shortName', tablename=table.name, dataType='text').notNull().unique()
    ownerId = Column(name='ownerId', tablename=table.name, dataType='integer').notNull().foreignKey().references('propertyOwners', 'id').onDelete('set null')
    managerId = Column(name='managerId', tablename=table.name, dataType='integer').notNull().foreignKey().references('propertyManagers', 'id').onDelete('set null')
    addressId = Column(name='addressId', tablename=table.name, dataType='integer').notNull().foreignKey().references('propertyAddresses', 'id').onDelete('set null')
    priceId = Column(name='priceId', tablename=table.name, dataType='integer').foreignKey().references('propertyPrices', 'id').onDelete('set null')
    accountantId = Column(name='accountantId', tablename=table.name, dataType='integer').foreignKey().references('propertyAccountants', 'id').onDelete('set null')
    table.columns = [ownerId, managerId, addressId, priceId, accountantId]
    table.foreignKeys = [ownerId, managerId, addressId, priceId, accountantId]
    table.columns = Column(name='alNumber', tablename=table.name, dataType='integer')
    table.columns = Column(name='weBook', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='bookingComName', tablename=table.name, dataType='text')
    table.columns = Column(name='airbnbName', tablename=table.name, dataType='text')
    table.columns = Column(name='vrboId', tablename=table.name, dataType='text')
    table.columns = Column(name='weClean', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='standardCleaningFee', tablename=table.name, dataType='real').notNull()
    table.columns = Column(name='sendOwnerBookingForms', tablename=table.name, dataType='boolean').notNull()
    table.create()
    return database


def create_specs_table(database: Database) -> Database:
    """
    Create the propertySpecs table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertySpecs')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    propertyId = Column(name='propertyId', tablename=table.name, dataType='integer').notNull().foreignKey().references('properties', 'id')
    table.columns = propertyId
    table.foreignKeys = propertyId
    table.columns = Column(name='isListed', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='isSeaView', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='isUpperFloor', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='isBeachfront', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='bedrooms', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='bathrooms', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='squareMetres', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='maxGuests', tablename=table.name, dataType='integer').notNull()
    table.create()
    return database


def create_sef_table(database: Database) -> Database:
    """
    Create the propertySEFDetails table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='propertySEFDetails')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    propertyId = Column(name='propertyId', tablename=table.name, dataType='integer').notNull().foreignKey().references('properties', 'id')
    table.columns = propertyId
    table.foreignKeys = propertyId
    table.columns = Column(name='unidadeHoteleira', tablename=table.name, dataType='text')
    table.columns = Column(name='estabelecimento', tablename=table.name, dataType='text')
    table.columns = Column(name='chaveDeAutenticacao', tablename=table.name, dataType='text')
    table.create()
    return database


def create_guests_table(database: Database) -> Database:
    """
    Create the guests table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='guests')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='firstName', tablename=table.name, dataType='text')
    table.columns = Column(name='lastName', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='email', tablename=table.name, dataType='text')
    table.columns = Column(name='phone', tablename=table.name, dataType='text')
    table.columns = Column(name='idCard', tablename=table.name, dataType='text')
    table.columns = Column(name='nifNumber', tablename=table.name, dataType='text')
    table.columns = Column(name='nationality', tablename=table.name, dataType='text')
    preferredLanguage = Column(name='preferredLanguage', tablename=table.name, dataType='text')
    preferredLanguage.defaultValue = DEFAULT_LANGUAGE
    table.columns = preferredLanguage
    table.create()
    return database


def create_bookings_table(database: Database) -> Database:
    """
    Create the bookings table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='bookings')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    propertyId = Column(name='propertyId', tablename=table.name, dataType='integer').notNull().foreignKey().references('properties', 'id').onDelete('no action')
    guestId = Column(name='guestId', tablename=table.name, dataType='integer').notNull().foreignKey().references('guests', 'id').onDelete('no action')
    table.columns = [propertyId, guestId]
    table.foreignKeys = [propertyId, guestId]
    table.columns = Column(name='PIMSId', tablename=table.name, dataType='integer')
    table.columns = Column(name='platformId', tablename=table.name, dataType='text')
    table.columns = Column(name='platformAddress', tablename=table.name, dataType='text')
    table.columns = Column(name='isOwner', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='enquiryStatus', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='enquiryDate', tablename=table.name, dataType='text')
    table.columns = Column(name='enquirySource', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='adults', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='children', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='babies', tablename=table.name, dataType='integer').notNull()
    table.columns = Column(name='manualGuests', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='lastUpdated', tablename=table.name, dataType='text').notNull()
    table.create()
    return database


def create_arrivals_table(database: Database) -> Database:
    """
    Create the arrivals table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='arrivals')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='date', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='flightNumber', tablename=table.name, dataType='text')
    table.columns = Column(name='isFaro', tablename=table.name, dataType='boolean')
    table.columns = Column(name='time', tablename=table.name, dataType='text')
    table.columns = Column(name='details', tablename=table.name, dataType='text')
    table.columns = Column(name='selfCheckIn', tablename=table.name, dataType='boolean')
    table.columns = Column(name='meetGreet', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='manualDate', tablename=table.name, dataType='boolean')
    table.create()
    return database


def create_departures_table(database: Database) -> Database:
    """
    Create the departures table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='departures')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='date', tablename=table.name, dataType='text').notNull()
    table.columns = Column(name='flightNumber', tablename=table.name, dataType='text')
    table.columns = Column(name='isFaro', tablename=table.name, dataType='boolean')
    table.columns = Column(name='time', tablename=table.name, dataType='text')
    table.columns = Column(name='details', tablename=table.name, dataType='text')
    table.columns = Column(name='clean', tablename=table.name, dataType='boolean').notNull()
    table.columns = Column(name='manualDate', tablename=table.name, dataType='boolean')
    table.create()
    return database


def create_charges_table(database: Database) -> Database:
    """
    Create the charges table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='charges')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='bankTransfer', tablename=table.name, dataType='boolean')
    table.columns = Column(name='creditCard', tablename=table.name, dataType='boolean')
    table.columns = Column(name='currency', tablename=table.name, dataType='text')
    table.columns = Column(name='basicRental', tablename=table.name, dataType='real')
    table.columns = Column(name='admin', tablename=table.name, dataType='real')
    table.columns = Column(name='security', tablename=table.name, dataType='real')
    table.columns = Column(name='securityMethod', tablename=table.name, dataType='text')
    table.columns = Column(name='platformFee', tablename=table.name, dataType='real')
    table.columns = Column(name='extraNights', tablename=table.name, dataType='real')
    table.columns = Column(name='manualCharges', tablename=table.name, dataType='boolean')
    table.create()
    return database


def create_extras_table(database: Database) -> Database:
    """
    Create the extras table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='extras')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='cot', tablename=table.name, dataType='boolean')
    table.columns = Column(name='highChair', tablename=table.name, dataType='boolean')
    table.columns = Column(name='welcomePack', tablename=table.name, dataType='boolean')
    table.columns = Column(name='welcomePackModifications', tablename=table.name, dataType='text')
    table.columns = Column(name='midStayClean', tablename=table.name, dataType='boolean')
    table.columns = Column(name='lateCheckout', tablename=table.name, dataType='boolean')
    table.columns = Column(name='otherRequests', tablename=table.name, dataType='text')
    table.columns = Column(name='extraNights', tablename=table.name, dataType='boolean')
    table.columns = Column(name='airportTransfers', tablename=table.name, dataType='boolean')
    table.columns = Column(name='airportTransferInboundOnly', tablename=table.name, dataType='boolean')
    table.columns = Column(name='airportTransferOutboundOnly', tablename=table.name, dataType='boolean')
    table.columns = Column(name='childSeats', tablename=table.name, dataType='text')
    table.columns = Column(name='excessBaggage', tablename=table.name, dataType='text')
    table.columns = Column(name='ownerIsPaying', tablename=table.name, dataType='boolean')
    table.create()
    return database


def create_forms_table(database: Database) -> Database:
    """
    Create the forms table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='forms')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='balancePayment', tablename=table.name, dataType='text')
    table.columns = Column(name='arrivalQuestionnaire', tablename=table.name, dataType='text')
    table.columns = Column(name='guestRegistration', tablename=table.name, dataType='text')
    table.columns = Column(name='guestRegistrationDone', tablename=table.name, dataType='boolean')
    table.columns = Column(name='securityDeposit', tablename=table.name, dataType='text')
    table.columns = Column(name='PIMSuin', tablename=table.name, dataType='text')
    table.columns = Column(name='PIMSoid', tablename=table.name, dataType='text')
    table.create()
    return database


def create_emails_table(database: Database) -> Database:
    """
    Create the emails table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='emails')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='balancePayment', tablename=table.name, dataType='boolean')
    table.columns = Column(name='arrivalQuestionnaire', tablename=table.name, dataType='boolean')
    table.columns = Column(name='securityDepositRequest', tablename=table.name, dataType='boolean')
    table.columns = Column(name='arrivalInformation', tablename=table.name, dataType='boolean')
    table.columns = Column(name='guestRegistrationForm', tablename=table.name, dataType='boolean')
    table.columns = Column(name='checkInInstructions', tablename=table.name, dataType='boolean')
    table.columns = Column(name='finalDaysReminder', tablename=table.name, dataType='boolean')
    table.columns = Column(name='goodbye', tablename=table.name, dataType='boolean')
    table.columns = Column(name='management', tablename=table.name, dataType='boolean')
    table.columns = Column(name='payOwner', tablename=table.name, dataType='boolean')
    table.columns = Column(name='securityDepositReturn', tablename=table.name, dataType='boolean')
    table.columns = Column(name='airportTransfers', tablename=table.name, dataType='boolean')
    table.columns = Column(name='guestRegistrationFormToOwner', tablename=table.name, dataType='boolean')
    table.columns = Column(name='paused', tablename=table.name, dataType='boolean')
    table.create()
    return database


def create_updates_table(database: Database) -> Database:
    """
    Create the updates table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='updates')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    table.columns = Column(name='date', tablename=table.name, dataType='text').notNull()
    bookingId = Column(name='bookingId', tablename=table.name, dataType='integer').notNull().foreignKey().references('bookings', 'id')
    table.columns = bookingId
    table.foreignKeys = bookingId
    table.columns = Column(name='details', tablename=table.name, dataType='integer')
    table.columns = Column(name='extras', tablename=table.name, dataType='integer')
    table.columns = Column(name='emailSent', tablename=table.name, dataType='boolean').notNull()
    table.create()
    return database


def create_touristtax_table(database: Database) -> Database:
    """
    Create the touristtax table in the database.
    
    Parameters:
        database: The database connection.
        
    Returns:
        Database: The database instance for chaining.
    """
    table = Table(database, name='touristtax')
    table.columns = Column(name='id', tablename=table.name, dataType='integer').primaryKey()
    chargesId = Column(name='chargesId', tablename=table.name, dataType='integer').notNull().foreignKey().references('charges', 'id')
    table.columns = chargesId
    table.foreignKeys = chargesId
    table.columns = Column(name='total', tablename=table.name, dataType='real')
    table.columns = Column(name='orderId', tablename=table.name, dataType='text')
    table.columns = Column(name='orderToken', tablename=table.name, dataType='text')
    table.columns = Column(name='paid', tablename=table.name, dataType='boolean')
    table.create()
    return database