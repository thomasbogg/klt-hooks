from libraries.database.column import Column
from libraries.database.database import Database
from libraries.database.table import Table


def create_database() -> Database:
    """
    Create and initialize the KLT Hooks database with all required tables.
    
    Returns:
        Database: The connected database instance.
    """
    database = Database('klt_hooks.db', 'klt_hooks').connect()
    create_touristtax_table(database)
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
    table.columns = Column(name='date', tablename=table.name, dataType='text')
    table.columns = Column(name='orderId', tablename=table.name, dataType='text')
    table.columns = Column(name='paid', tablename=table.name, dataType='boolean')
    table.create()
    return database