from typing import Any

from libraries.database.row import Row as DatabaseRow


class Manager(DatabaseRow):
    """
    Represents a property manager with company, contact, and specialized roles.
    
    This class handles database operations for property managers, allowing
    retrieval and modification of company information, contact details, and
    specialized contacts for maintenance, liaison, and cleaning services.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property manager object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, tablename='propertyManagers')

    # Basic company and contact information
    @property
    def company(self) -> str | None:
        """
        Get the property management company name.
        
        Returns:
            The company name or None if not set.
        """
        return self._get('company')
    
    @company.setter
    def company(self, value: str) -> None:
        """
        Set the property management company name.
        
        Args:
            value: The company name to set.
        """
        self._set('company', value)

    @property
    def name(self) -> str | None:
        """
        Get the main contact name for the property manager.
        
        Returns:
            The contact name or None if not set.
        """
        return self._get('name')
    
    @name.setter
    def name(self, value: str) -> None:
        """
        Set the main contact name for the property manager.
        
        Args:
            value: The contact name to set.
        """
        self._set('name', value)

    @property
    def email(self) -> str | None:
        """
        Get the main email address for the property manager.
        
        Returns:
            The email address or None if not set.
        """
        return self._get('email')
    
    @email.setter
    def email(self, value: str) -> None:
        """
        Set the main email address for the property manager.
        
        Args:
            value: The email address to set.
        """
        self._set('email', value)

    @property
    def phone(self) -> str | None:
        """
        Get the main phone number for the property manager.
        
        Returns:
            The phone number or None if not set.
        """
        return self._get('phone')
    
    @phone.setter
    def phone(self, value: str) -> None:
        """
        Set the main phone number for the property manager.
        
        Args:
            value: The phone number to set.
        """
        self._set('phone', value)

    # Maintenance contact information
    @property
    def maintenance(self) -> str | None:
        """
        Get the maintenance contact name.
        
        Returns:
            The maintenance contact name or None if not set.
        """
        return self._get('maintenance')
    
    @maintenance.setter
    def maintenance(self, value: str) -> None:
        """
        Set the maintenance contact name.
        
        Args:
            value: The maintenance contact name to set.
        """
        self._set('maintenance', value)

    @property
    def maintenancePhone(self) -> str | None:
        """
        Get the maintenance contact phone number.
        
        Returns:
            The maintenance phone number or None if not set.
        """
        return self._get('maintenancePhone')
    
    @maintenancePhone.setter
    def maintenancePhone(self, value: str) -> None:
        """
        Set the maintenance contact phone number.
        
        Args:
            value: The maintenance phone number to set.
        """
        self._set('maintenancePhone', value)

    @property
    def maintenanceEmail(self) -> str | None:
        """
        Get the maintenance contact email address.
        
        Returns:
            The maintenance email address or None if not set.
        """
        return self._get('maintenanceEmail')
    
    @maintenanceEmail.setter
    def maintenanceEmail(self, value: str) -> None:
        """
        Set the maintenance contact email address.
        
        Args:
            value: The maintenance email address to set.
        """
        self._set('maintenanceEmail', value)

    # Liaison contact information
    @property
    def liaison(self) -> str | None:
        """
        Get the guest liaison contact name.
        
        Returns:
            The liaison contact name or None if not set.
        """
        return self._get('liaison')
    
    @liaison.setter
    def liaison(self, value: str) -> None:
        """
        Set the guest liaison contact name.
        
        Args:
            value: The liaison contact name to set.
        """
        self._set('liaison', value)

    @property
    def liaisonPhone(self) -> str | None:
        """
        Get the guest liaison contact phone number.
        
        Returns:
            The liaison phone number or None if not set.
        """
        return self._get('liaisonPhone')
    
    @liaisonPhone.setter
    def liaisonPhone(self, value: str) -> None:
        """
        Set the guest liaison contact phone number.
        
        Args:
            value: The liaison phone number to set.
        """
        self._set('liaisonPhone', value)

    @property
    def liaisonEmail(self) -> str | None:
        """
        Get the guest liaison contact email address.
        
        Returns:
            The liaison email address or None if not set.
        """
        return self._get('liaisonEmail')
    
    @liaisonEmail.setter
    def liaisonEmail(self, value: str) -> None:
        """
        Set the guest liaison contact email address.
        
        Args:
            value: The liaison email address to set.
        """
        self._set('liaisonEmail', value)

    # Cleaning contact information
    @property
    def cleaning(self) -> str | None:
        """
        Get the cleaning service contact name.
        
        Returns:
            The cleaning contact name or None if not set.
        """
        return self._get('cleaning')
    
    @cleaning.setter
    def cleaning(self, value: str) -> None:
        """
        Set the cleaning service contact name.
        
        Args:
            value: The cleaning contact name to set.
        """
        self._set('cleaning', value)

    @property
    def cleaningPhone(self) -> str | None:
        """
        Get the cleaning service contact phone number.
        
        Returns:
            The cleaning phone number or None if not set.
        """
        return self._get('cleaningPhone')
    
    @cleaningPhone.setter
    def cleaningPhone(self, value: str) -> None:
        """
        Set the cleaning service contact phone number.
        
        Args:
            value: The cleaning phone number to set.
        """
        self._set('cleaningPhone', value)

    @property
    def cleaningEmail(self) -> str | None:
        """
        Get the cleaning service contact email address.
        
        Returns:
            The cleaning email address or None if not set.
        """
        return self._get('cleaningEmail')
    
    @cleaningEmail.setter
    def cleaningEmail(self, value: str) -> None:
        """
        Set the cleaning service contact email address.
        
        Args:
            value: The cleaning email address to set.
        """
        self._set('cleaningEmail', value)
    
    def _get_condition(self) -> str:
        """
        Get the database condition to identify this manager record.
        
        Returns:
            A SQL condition string based on the company name.
        """
        return f'company="{self.company}"'