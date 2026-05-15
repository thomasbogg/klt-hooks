def determine_location(value: str | None) -> dict[str, bool | None]:
    """
    Parse a location string into a dictionary of location flags.
    
    This function takes a location description string and determines which
    specific locations (Barracuda, Monaco, Corcovada, Cerro) are referenced.
    
    Args:
        value: A location string to parse, or None.
        
    Returns:
        Dictionary with boolean flags for each location.
    """
    if value is None or not value or 'all' in value.lower():
        return {
            'isBarracuda': None, 
            'isMonaco': None, 
            'isCorcovada': None, 
            'isCerro': None,
            'isBalaia': None
        }
    
    result = {}
    value = value.lower()
    
    result['isBarracuda'] = 'barracuda' in value
    result['isMonaco'] = 'monaco' in value
    result['isCorcovada'] = 'corcovada' in value
    result['isCerro'] = 'cerro' in value
    result['isBalaia'] = 'balaia' in value
    
    return result