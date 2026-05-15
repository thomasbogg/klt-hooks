from typing import Any

from libraries.database.row import Row as DatabaseRow


class Guest(DatabaseRow):
    """
    Represents a guest in the system.
    
    This class provides methods to access and modify guest information stored in the database.
    """

    def __init__(self, database: Any | None = None):
        """
        Initialize a Guest object.
        
        Parameters:
            database: The database connection to use.
        """
        super().__init__(database, 'guests')
    
    # Basic guest information properties
    @property
    def firstName(self) -> str | None:
        """Get the guest's first name."""
        return self._get('firstName')
    
    @firstName.setter
    def firstName(self, value: str | None) -> None:
        """Set the guest's first name."""
        self._set('firstName', value)

    @property
    def lastName(self) -> str | None:
        """Get the guest's last name."""
        return self._get('lastName')

    @lastName.setter
    def lastName(self, value: str | None) -> None:
        """Set the guest's last name."""
        self._set('lastName', value)
        
    @property
    def fullName(self) -> str:
        """Get the guest's full name (first name + last name)."""
        firstName = self.firstName or ""
        lastName = self.lastName or ""
        return f'{" ".join([firstName, lastName])}'.strip()

    @property
    def name(self) -> str:
        """Get the guest's full name (alias for fullName)."""
        return self.fullName
        
    @property
    def prettyName(self) -> str:
        """
        Get a formatted display name for the guest.
        
        Returns:
            A user-friendly version of the guest's name or a description.
        """
        if self.firstName is None:
            return self.lastName or ""
        if 'owner' in self.firstName.lower() or 'family' in self.firstName.lower():
            return 'Owner/Family'
        
        lastName = self.lastName or ""
        if 'owner' in lastName.lower() or 'family' in lastName.lower():
            return 'Owner/Family'
        
        if lastName and not (lastName[0].isdigit() or lastName[-1].isdigit()):
            return self.fullName
        
        return 'Unknown Guest'
        
    # Contact information properties
    @property
    def email(self) -> str | None:
        """Get the guest's email address."""
        return self._get('email')

    @email.setter
    def email(self, value: str | None) -> None:
        """Set the guest's email address."""
        self._set('email', value)

    @property
    def emailAddress(self) -> str | None:
        """Get the guest's email address (alias for email)."""
        return self.email
    
    @emailAddress.setter
    def emailAddress(self, value: str | None) -> None:
        """Set the guest's email address (alias for email)."""
        self.email = value

    @property
    def phone(self) -> str | None:
        """Get the guest's phone number."""
        return self._get('phone')

    @phone.setter
    def phone(self, value: str | None) -> None:
        """Set the guest's phone number."""
        self._set('phone', value)

    @property
    def phoneNumber(self) -> str | None:
        """Get the guest's phone number (alias for phone)."""
        return self.phone
    
    @phoneNumber.setter
    def phoneNumber(self, value: str | None) -> None:
        """Set the guest's phone number (alias for phone)."""
        self.phone = value
    
    # Identity information properties
    @property
    def idCard(self) -> str | None:
        """Get the guest's ID card number."""
        return self._get('idCard')

    @idCard.setter
    def idCard(self, value: str | None) -> None:
        """Set the guest's ID card number."""
        self._set('idCard', value)
        
    @property
    def passport(self) -> str | None:
        """Get the guest's passport number (alias for idCard)."""
        return self.idCard
    
    @passport.setter
    def passport(self, value: str | None) -> None:
        """Set the guest's passport number (alias for idCard)."""
        self.idCard = value

    @property
    def nifNumber(self) -> str | None:
        """Get the guest's NIF number."""
        return self._get('nifNumber')
    
    @nifNumber.setter
    def nifNumber(self, value: str | None) -> None:
        """Set the guest's NIF number."""
        self._set('nifNumber', value)

    @property
    def nif(self) -> str | None:
        """Get the guest's NIF number (alias for nifNumber)."""
        return self.nifNumber
    
    @nif.setter
    def nif(self, value: str | None) -> None:
        """Set the guest's NIF number (alias for nifNumber)."""
        self.nifNumber = value

    @property
    def nationality(self) -> str | None:
        """Get the guest's nationality."""
        return self._get('nationality')
    
    @nationality.setter
    def nationality(self, value: str | None) -> None:
        """Set the guest's nationality."""
        self._set('nationality', value)

    @property
    def preferredLanguage(self) -> str:
        """Get the guest's preferred language for interaction"""
        return self._get('preferredLanguage')
    
    @preferredLanguage.setter
    def preferredLanguage(self, value: str) -> None:
        """Set the guest's preferred language for interaction"""
        if not isinstance(value, str):
            raise TypeError(
                f'Value for preferred language must be string. Given "{value}" is {type(value)}')
        self._set('preferredLanguage', value)
    
    # Status properties
    @property
    def isBlock(self) -> bool:
        """
        Check if this guest record represents a booking block.
        
        Returns:
            True if this is a booking block, False otherwise.
        """
        lastName = self.lastName or ""
        if 'late check' in lastName.lower():
            return True
        if 'unbookable' in lastName.lower():
            return True
        if 'block -' in lastName.lower():
            return True
        return False
    
    # Database interaction methods
    def exists(self) -> bool:
        """
        Check if the guest already exists in the database.
        
        Returns:
            True if the guest exists in the database, False otherwise.
        """
        if 'id' in self._values and super().exists():
            return True
            
        try:
            if self.email:
                id = self.database.runSQL(
                    f'SELECT id FROM guests WHERE email = "{self.email}"')._cursor.fetchone()
                if id:
                    self.id = id[0]
                    return True
        except:
            pass
            
        try:
            if self.phone:
                id = self.database.runSQL(
                    f'SELECT id FROM guests WHERE phone = "{self.phone}"')._cursor.fetchone()
                if id:
                    self.id = id[0]
                    return True
        except:
            pass
            
        return False
    
    def hasNewDetails(self) -> bool:
        """
        Check if the guest has details that differ from what's in the database.
        
        Returns:
            True if the guest has new details compared to the database, False otherwise.
        """
        if not self._values:
            return False
        
        if len(self._values) == 1:
            return False
        
        if not self.exists():
            return True
        
        try:
            query_result = self.database.runSQL(
                f'SELECT firstName, lastName, email, phone, idCard, nifNumber, preferredLanguage FROM guests WHERE id={self.id}'
            )._cursor.fetchone()
            
            if not query_result:
                return True
                
            firstName, lastName, email, phone, idCard, nifNumber, preferredLanguage = query_result
            
            if self.firstName and self.firstName != firstName:
                return True
            if self.lastName and self.lastName != lastName:    
                return True
            
            try:
                if self.email and self.email != email:
                    return True
                if self.phone and self.phone != phone:
                    return True
            except Exception:
                pass
            
            try:
                if self.idCard and self.idCard != idCard:
                    return True
            except Exception:
                pass    
            
            try:
                if self.nifNumber and self.nifNumber != nifNumber:
                    return True
            except Exception:
                pass
            
            try:
                if self.preferredLanguage and self.preferredLanguage != preferredLanguage:
                    return True
            except Exception:
                pass
                
            return False
        except Exception:
            return True