from csv import DictReader
from os import path

from default.database.functions import get_database
from default.property.accountant import Accountant
from default.property.address import Address
from default.property.data.accountants import Accountants
from default.property.data.addresses import Addresses
from default.property.data.managers import Managers
from default.property.data.owners import Owners
from default.property.prices import Prices
from default.property.data.properties import Properties
from default.property.data.sef import SEFDetails as SEFDetailsData
from default.property.data.specs import Specs as PropertySpecsData
from default.property.manager import Manager
from default.property.owner import Owner
from default.property.property import Property
from default.property.sef import SEFDetails
from default.property.specs import Specs
from default.update.wrapper import update
from libraries.utils import log, sublog


#######################################################
# MAIN UPDATE FUNCTION
#######################################################

def update_properties_information_in_database() -> str:
    """
    Update all property-related information in the database.
    
    This function calls all the specialized update functions to refresh
    the database with the latest property data, including addresses,
    accountants, managers, owners, properties, and property specifications.
    
    Returns:
        A success message.
    """
    update_database_addresses()
    update_database_accountants()
    update_database_managers()
    update_database_owners()
    update_database_properties()
    update_database_properties_specs()
    update_database_properties_prices()
    update_database_properties_sef_details()

    return 'Successfully updated all properties information in database!'


#######################################################
# DATABASE UPDATE FUNCTIONS
#######################################################

@update
def update_database_accountants() -> str:
    """
    Update accountant information in the database.
    
    Gets accountant data from the Accountants data class and updates
    or inserts records in the database accordingly.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for company in Accountants.companies():
        log(f'DOING: {company}')
  
        accountant = Accountant(database)
        accountant.company = company
        accountant.name = Accountants.names()[company]
        accountant.phone = Accountants.phones()[company]
        accountant.email = Accountants.emails()[company]
  
        send_to_database(accountant)
  
    database.close()
    return 'Successfully sent all accountants to database'


@update
def update_database_owners() -> str:
    """
    Update owner information in the database.
    
    Gets owner data from the Owners data class and updates
    or inserts records in the database accordingly.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for name in Owners.all():
        log(f'DOING: {name}')
  
        owner = Owner(database)
        owner.name = name
        owner.email = Owners.emails()[name]
        owner.phone = Owners.phones()[name]
        owner.nifNumber = Owners.nif_numbers()[name]
        owner.defaultClean = Owners.default_clean()[name]
        owner.defaultMeetGreet = Owners.default_meet_greet()[name]
        owner.takesEuros = Owners.take_euros()[name]
        owner.takesPounds = Owners.take_pounds()[name]
        owner.wantsAccounting = Owners.want_accounting()[name]
        owner.cleansAreInvoiced = Owners.cleans_are_invoiced()[name]
        owner.rentalCommissionsAreInvoiced = Owners.rental_commissions_are_invoiced()[name]
        owner.isPaidRegularly = Owners.are_paid_regularly()[name]
  
        send_to_database(owner)
  
    database.close()
    return 'Successfully sent all owners to database'


@update
def update_database_managers() -> str:
    """
    Update property manager information in the database.
    
    Gets manager data from the Managers data class and updates
    or inserts records in the database accordingly.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for company in Managers.companies():
        log(f'DOING: {company}')
  
        manager = Manager(database)
        manager.company = company
        manager.name = Managers.names()[company]
        manager.phone = Managers.phones()[company]
        manager.email = Managers.emails()[company]
        manager.maintenance = Managers.maintenance()[company]
        manager.maintenancePhone = Managers.maintenance_phones()[company]
        manager.maintenanceEmail = Managers.maintenance_emails()[company]
        manager.liaison = Managers.liaison()[company]
        manager.liaisonPhone = Managers.liaison_phones()[company]
        manager.liaisonEmail = Managers.liaison_emails()[company]
        manager.cleaning = Managers.cleaning()[company]
        manager.cleaningPhone = Managers.cleaning_phones()[company]
        manager.cleaningEmail = Managers.cleaning_emails()[company]
  
        send_to_database(manager)
  
    database.close()
    return 'Successfully sent all managers to database'


@update
def update_database_addresses() -> str:
    """
    Update property address information in the database.
    
    Gets address data from the Addresses data class and updates
    or inserts records in the database accordingly.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for location in Addresses.locations():
        log(f'DOING: {location}')
  
        address = Address(database)
        address.location = location
        address.coordinates = Addresses.coordinates()[location]
        address.street = Addresses.street()[location]
        address.map = Addresses.map()[location]
        address.directions = Addresses.directions()[location]
        address.nearestBins = Addresses.nearest_bins()[location]
        address.nearestSupermarket = Addresses.nearest_supermarket()[location]
        address.nearestCornerShop = Addresses.nearest_corner_shop()[location]
  
        send_to_database(address)
  
    database.close()
    return 'Successfully sent all addresses to database'


@update
def update_database_properties() -> str:
    """
    Update property listings in the database.
    
    Gets property data from the Properties data class and updates
    or inserts records in the database accordingly, including
    foreign key relationships to other tables.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for name in Properties.all():
        log(f'DOING: {name}')
  
        property = Property(database)
        property.name = name
        property.shortName = Properties.short_names()[name]
        property.managerId = property.getForeignKeyId(Manager, 'company', Properties.management_companies()[name])
        property.addressId = property.getForeignKeyId(Address, 'location', Properties.locations()[name])
        property.ownerId = property.getForeignKeyId(Owner, 'name', Properties.owner_names()[name])
        property.priceId = Properties.price_ids()[name]
        property.accountantId = property.getForeignKeyId(Accountant, 'company', Properties.accountants()[name])
        property.bookingComName = Properties.booking_com_names()[name]
        property.airbnbName = Properties.airbnb_names()[name]
        property.vrboId = Properties.vrbo_ids()[name]
        property.standardCleaningFee = Properties.standard_cleaning_fees()[name]
        property.weClean = Properties.we_clean()[name]
        property.weBook = Properties.we_book()[name]
        property.ownerRegistersGuests = Properties.owners_register_guests()[name]
        property.sendOwnerBookingForms = Properties.send_owner_booking_forms()[name]
        property.alNumber = Properties.al_numbers()[name]
  
        send_to_database(property)
  
    database.close()
    return 'Successfully sent all properties to database!'


@update
def update_database_properties_specs() -> str:
    """
    Update property specifications in the database.
    
    Gets property specification data from the PropertySpecsData class
    and updates or inserts records in the database accordingly,
    linking to the properties table.
    
    Returns:
        A success message.
    """
    database = get_database()
  
    for name in Properties.all():
        log(f'DOING: {name}')
  
        specs = Specs(database)
        specs.propertyId = specs.getForeignKeyId(Property, 'name', name)
        specs.bedrooms = PropertySpecsData.bedrooms()[name]    
        specs.bathrooms = PropertySpecsData.bathrooms()[name]    
        specs.squareMetres = PropertySpecsData.square_metres()[name]    
        specs.isListed = PropertySpecsData.are_listed()[name]    
        specs.isSeaView = PropertySpecsData.are_sea_view()[name]    
        specs.isUpperFloor = PropertySpecsData.are_upper_floor()[name]    
        specs.isBeachfront = PropertySpecsData.are_beachfront()[name]   
        specs.maxGuests = PropertySpecsData.maximum_guests()[name]     

        send_to_database(specs)
  
    database.close()        
    return 'Successfully sent all properties specs to database!'


@update
def update_database_properties_sef_details() -> str:
    """
    Update property SEF details in the database.
    
    Gets SEF details from the SEFDetails data class and updates
    or inserts records in the database accordingly, linking to the
    properties table.
    
    Returns:
        A success message.
    """
    database = get_database()

    for name in Properties.all():
        log(f'DOING: {name}')

        sef = SEFDetails(database)
        sef.propertyId = sef.getForeignKeyId(Property, 'name', name)
        sef.unidadeHoteleira = SEFDetailsData.unidadesHoteleiras()[name]
        sef.estabelecimento = SEFDetailsData.estabelecimentos()[name]
        sef.chaveDeAutenticacao = SEFDetailsData.chavesDeAutenticacao()[name]

        send_to_database(sef)

    database.close()
    return 'Successfully sent all properties sef details to database!'


@update
def update_database_properties_prices() -> str:
    """
    Update property prices in the database.
    
    Gets property price data from the prices.csv file and updates
    or inserts records in the database accordingly.
    
    Returns:
        A success message.
    """
    if not path.exists('default/property/data/prices.csv'):
        raise FileNotFoundError('prices.csv file not found in default/property/data/')
    
    database = get_database()
    with open('default/property/data/prices.csv', 'r', encoding='utf-8') as file:
        reader = DictReader(file)
        for row in reader:
           
            prices = Prices(database)
            prices.name = row.pop('name')
            prices.year = int(row.pop('year'))
            for month, price in row.items():
                setattr(prices, month, float(price))
            send_to_database(prices)
    
    database.close()
    return 'Successfully sent all property prices to database!'


#######################################################
# HELPER FUNCTIONS
#######################################################

def send_to_database(row: Accountant | Address | Manager | Owner | Prices | Property | SEFDetails | Specs) -> None:
    """
    Send a row object to the database by updating or inserting it.
    
    Args:
        row: A database row object to save (Accountant, Address, Manager, etc.)
        
    Returns:
        None
    """
    if row.exists():
        row.update()
        sublog('...updated in database successfully')
    else:
        row.insert()
        sublog('...inserted in database successfully')