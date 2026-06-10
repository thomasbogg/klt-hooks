from libraries.database.database import Database as _Database
from libraries.database.table import Table
from default.database.tables.touristtax import Touristtax as TouristtaxTable
from default.database.rows.touristtax import Touristtax as TouristtaxRow
from default.settings import DATABASE_NAME, DATABASE_PATH


class Database(_Database):
    """
    Extended database class for KLT application.
    
    This class extends the default database functionality with specific
    tables and methods for the KLT application.
    """

    def __init__(
            self, 
            path: str = DATABASE_PATH, 
            name: str = DATABASE_NAME, 
            loadObject: TouristtaxRow = None, 
            TEST: bool = False) -> None:
        """
        Initialize the database connection and set up the tables.
        
        Parameters:
            loadObject: The object type to load from the database.
            TEST: Boolean indicating if the database is in test mode.
        """
        super().__init__(path=path, name=name, TEST=TEST)
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
    def touristtax(self) -> TouristtaxTable:
        """
        Get the tourist tax table object.
        
        Returns:
            TouristtaxTable: The tourist tax table object.
        """
        return self._table(name='touristtax', object=TouristtaxTable)

    def fetchall(self) -> list[TouristtaxRow]:
        """
        Fetch all records from the database and load them into the specified object type.
        
        Returns:
            A list of TouristtaxRow objects.
        """
        return super().fetchall(self._load_object)
    
    def fetchone(self) -> TouristtaxRow | None:
        """
        Fetch a single record from the database and load it into the specified object type.
        
        Returns:
            A TouristtaxRow object, or None if no record is found.
        """
        return super().fetchone(self._load_object)