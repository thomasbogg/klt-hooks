import datetime
import regex as re

from default.booking.booking import Booking
from default.database.functions import (
    search_valid_bookings,
    set_property_location,
)
from default.dates import dates
from default.guest.functions import guest_has_stayed_before
from phonenumbers import (
    PhoneNumberFormat,
    format_number,
    parse as parse_number
)
from libraries.utils import (
    isListError,
    isString,
    log,
    logerror,
    only_digits_in_string,
    sublog,
    to_string_or_error
)


#######################################################
# UTILITY FUNCTIONS
#######################################################

def logbooking(booking: Booking, header: str = '', inline: str = '', tabs: int = 2) -> None:
    """
    Log booking information with optional header and inline formatting.
    
    Args:
        booking: The booking to log
        header: Optional header text to display above booking
        inline: Optional text to display inline with booking
        
    Returns:
        None
    """
    if header:
        log(header, tabs=tabs)
    elif not inline:
        log('_____Booking_____', tabs=tabs)

    if inline:
        sublog(f'{inline} {booking.__repr__()}', tabs=tabs)
    else:
        sublog(booking.__repr__(), tabs=tabs)
    return None


def hideCharges(func):
    """
    Decorator that returns 'Und.' for a booking if charges are hidden.
    
    Args:
        func: The function to wrap
        
    Returns:
        The wrapped function
    """
    def wrapper(booking: Booking, *args, **kwargs):
        if booking.charges.hide:
            return 'Und.'
        return func(booking, *args, **kwargs)
    return wrapper


def managementCheck(func):
    """
    Decorator that checks if booking qualifies for management services.
    
    Args:
        func: The function to wrap
        
    Returns:
        The wrapped function that returns False if conditions aren't met
    """
    def wrapper(booking: Booking):
        if not booking.managementStatusIsOkay:
            return False
        if not booking.property.weClean:
            return False
        return func(booking)
    return wrapper


#######################################################
# BOOKING STATUS FUNCTIONS
#######################################################

def total_nights(arrival: datetime.date, departure: datetime.date) -> int | None:
    """
    Calculate the total number of nights between arrival and departure.
    
    Args:
        arrival: The arrival date
        departure: The departure date
        
    Returns:
        Number of nights or None if dates are invalid
    """
    if not arrival or not departure:
        return None
    if not isinstance(arrival, dates) or not isinstance(departure, dates):
        return logerror(
            f'arrival or departure for tot. nights calc is not dates: {arrival}, {departure}')
    return dates.subtractDates(arrival, departure)


def is_same_day_changeover(booking: Booking) -> bool:
    """
    Check if there's another booking with the same departure date.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if there's another booking on the same departure date
    """
    date = booking.departure.date
    search = search_valid_bookings(
        start=date, end=date, propertyName=booking.property.name)
    return len(search.fetchall()) > 0


def has_unconfirmed_status(booking: Booking) -> bool:
    """
    Check if booking has an unconfirmed status.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if status is unconfirmed (provisional, open enquiry, etc.)
    """
    status = booking.details.enquiryStatus.lower()
    if 'provisional' in status:
        return True
    if 'open enquiry' in status:
        return True
    if 'waiting for' in status:
        return True
    return False


def determine_hide_charges(booking: Booking) -> bool:
    """
    Determine if charges should be hidden for this booking.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if charges should be hidden
    """
    if not booking.details.isPlatform:
        return False
    if booking.arrival.date <= dates.date():
        return False
    if dates.subtractDates(booking.arrival.date, dates.date()) < 27:
        return False
    return True


def determine_need_for_invoice(booking: Booking) -> bool:
    """
    Determine if this booking requires an invoice.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if an invoice is needed
    """
    if booking.property.owner.rentalCommissionsAreInvoiced:
        return True
    if not booking.details.isPlatform:
        return False
    if booking.arrival.year < 2024:
        return False
    if booking.arrival.year < 2025:
        if booking.details.enquirySource == 'Booking.com':
            return False
    return True


def determine_use_exchange_rate(booking: Booking) -> bool:
    """
    Determine if exchange rate should be used for this booking.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if exchange rate should be used
    """
    takesEuros = booking.property.owner.takesEuros
    takesPounds = booking.property.owner.takesPounds
    return not (takesEuros and takesPounds)


#######################################################
# GUEST EXPERIENCE FUNCTIONS
#######################################################

@managementCheck
def determine_meet_greet(booking: Booking) -> bool:
    """
    Determine if meet and greet service is required.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if meet and greet service is required
    """
    return booking.arrival.meetGreet


@managementCheck
def determine_clean(booking: Booking) -> bool:
    """
    Determine if cleaning service is required.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if cleaning service is required
    """
    return booking.departure.clean


def determine_security_deposit_request(booking: Booking) -> float | None:
    """
    Determine security deposit amount for the booking.
    
    Args:
        booking: The booking to check
        
    Returns:
        Security deposit amount or None if not applicable
    """
    if booking.details.isOwner:
        return None
    if booking.details.isPlatform:
        return None
    if guest_has_stayed_before(booking):
        return None
    if not booking.charges.security:
        return None
    if booking.charges.securityMethod != 'Cash':
        return None
    return booking.charges.security


def determine_self_check_in(booking: Booking) -> bool:
    """
    Determine if self check-in is applicable for the booking.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if self check-in is applicable
    """
    if (
        not booking.property.isClubeDoMonaco and
        not booking.property.isQuintaDaBarracuda
    ):
        return False
    
    if booking.arrival.selfCheckIn:
        return True
    
    if booking.arrival.isLate:
        if booking.property.isQuintaDaBarracuda:
            return determine_key_box_for_self_check_in(booking)   
        return True
    
    return False


def determine_key_box_for_self_check_in(booking: Booking) -> None:
    """
    Check if the booking requires a key box for self check-in.
    
    Args:
        booking: The booking object to check.
        
    Returns:
        None
    """
    def __get_same_day_arrivals(booking: Booking) -> list[Booking]:
        """
        Get bookings with the same arrival date as the given booking.
        
        Args:
            booking: The booking object to check.
            
        Returns:
            List of bookings with the same arrival date.
        """
        search = search_valid_bookings(start=booking.arrival.date, end=booking.arrival.date)
        
        select = search.arrivals.select()
        select.selfCheckIn()
        
        set_property_location(search, isBarracuda=True)
        where = search.arrivals.where()
        where.selfCheckIn().isNotNullEmptyOrFalse()

        results = search.fetchall()
        search.close()
        return results
    
    sameDayArrivals = __get_same_day_arrivals(booking)
    keyBox = 'Key Box'
   
    if not sameDayArrivals:
        keyBox += ' 1'
    elif len(sameDayArrivals) == 1:
        arrival = sameDayArrivals[0].arrival
        keyBox += ' 2' if '1' in arrival.selfCheckIn else ' 1'
    else:
        return False
    
    booking.arrival.selfCheckIn = keyBox
    booking.arrival.update()
    return True


def determine_tourist_tax_nights(booking: Booking) -> int:
    """
    Determine if tourist tax applies to this booking.
    
    Args:
        booking: The booking to check
        
    Returns:
        EUR value if tourist tax applies, 0 otherwise
    """
    def calculate_tourist_tax_nights(bookings: list[Booking]) -> float:
        """
        Calculate the tourist tax for a given property based on its specifications.
        This is a placeholder function and should be implemented with the actual tax calculation logic.
        """
        # Example calculation (this should be replaced with the actual logic):
        total = 0
        for booking in bookings:
            # Assuming a flat rate of 1.5 per guest per night for demonstration
            nights = booking.totalNights
            adults = booking.details.adults
            if nights > 7:
                nights = 7  # Cap at 7 nights for tax calculation
            total += adults * nights
        return total

    if booking.arrival.date < dates.date(2026, 5, 23):
        return 0
    if booking.details.isOwner:
        return 0
    if not booking.property.alNumber:
        return 0
    if not isinstance(booking.property.alNumber, int):
        return 0
    if booking.details.enquirySource == 'Booking.com':
        return 0
    if booking.details.enquirySource == 'Direct':
        return 0
    if booking.property.alNumber < 999:
        return 0
    if booking.departure.date.month < 4:
        return 0
    if booking.departure.date.month == 4:
        if booking.totalNights > 14:
            return 0
        if booking.departure.date.day < 6:
            return 0
    if booking.arrival.date.month > 10:
        return 0
    if booking.arrival.date.month == 10:
        if booking.arrival.date.day > 23:
            return 0
    return calculate_tourist_tax_nights([booking])


def determine_extra_bed(booking: Booking) -> bool:
    """
    Determine if an extra bed is needed based on property and guest count.
    
    Args:
        booking: The booking to check
        
    Returns:
        True if an extra bed is needed
    """
    shortName = booking.property.shortName
    if shortName not in ('B02', 'D15'):
        return False
    if shortName == 'B02' and booking.details.totalGuests > 2:
        return True
    if shortName == 'D15' and booking.details.totalGuests > 3:
        return True
    return False


#######################################################
# FINANCIAL CALCULATION FUNCTIONS
#######################################################

@hideCharges
def determine_management_fee(booking: Booking) -> float:
    """
    Calculate the total management fee for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Total management fee amount
    """
    if not booking.property.weClean:
        return 0
    total = 0
    total += determine_cleaning_fee(booking)
    total += determine_meet_greet_fee(booking)
    total += determine_extra_bed_fee(booking)
    if booking.extras.ownerIsPaying:
        for extra in booking.extras:
            total += determine_price_of_extra(booking, extra) or 0
    return total


@hideCharges
def determine_cleaning_fee(booking: Booking) -> float:
    """
    Calculate the cleaning fee for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Cleaning fee amount
    """
    if not determine_clean(booking):
        return 0
    total = booking.property.standardCleaningFee
    guests = booking.details.totalGuests
    bedrooms = booking.property.specs.bedrooms
    if booking.departure.date > dates.date(2025, 12, 31):
        if bedrooms == 1:
            total += 10
        else:
            total += 15
    if guests / bedrooms > 2:
        if booking.departure.date > dates.date(2025, 12, 31):
            total += 15
        else:
            total += 10
    return total


@hideCharges
def determine_meet_greet_fee(booking: Booking) -> float:
    """
    Calculate the meet and greet fee for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Meet and greet fee amount
    """
    if not determine_meet_greet(booking):
        return 0
    if booking.departure.date > dates.date(2025, 12, 31):
        return 28
    return 25


@hideCharges
def determine_extra_bed_fee(booking: Booking) -> float:
    """
    Calculate the extra bed fee for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Extra bed fee amount
    """
    if not determine_extra_bed(booking):
        return 0
    return 25


@hideCharges
def determine_commission(booking: Booking) -> float:
    """
    Calculate the commission for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Commission amount
    """
    rental = booking.charges.basicRental + booking.charges.extraNights
    if not dates.isHighSeason(booking.arrival.date):
        return 0.10 * rental
    if booking.property.owner.wantsAccounting:
        if not dates.isNewVATRegime(booking.arrival.date):
            return rental * 0.17
    return rental * 0.15


@hideCharges
def determine_commission_after_IVA(booking: Booking) -> float:
    """
    Calculate the commission after IVA (VAT) for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Commission amount after IVA
    """
    commission = determine_commission(booking)
    if not determine_need_for_invoice(booking):
        return commission
    return commission / 1.23


@hideCharges
def determine_klt_commission(booking: Booking, postIVA=True) -> float:
    """
    Calculate the KLT portion of the commission.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        KLT commission amount
    """
    if postIVA:
        commission = determine_commission_after_IVA(booking)
    else:
        commission = determine_commission(booking)
    return commission * determine_commission_partition(booking)[0]


@hideCharges
def determine_non_klt_commission(booking: Booking, postIVA=True) -> float:
    """
    Calculate the non-KLT portion of the commission.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Non-KLT commission amount
    """
    if postIVA:
        commission = determine_commission_after_IVA(booking)
    else:
        commission = determine_commission(booking)
    return commission * determine_commission_partition(booking)[1]


@hideCharges
def determine_platform_fee(booking: Booking) -> float:
    """
    Calculate the platform fee for the booking.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Platform fee amount
    """
    if not determine_need_for_invoice(booking):
        return 0
    return booking.charges.platformFee


@hideCharges
def determine_platform_fee_IVA(booking: Booking) -> float:
    """
    Calculate the IVA (VAT) on the platform fee.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Platform fee IVA amount
    """
    return determine_platform_fee(booking) * .23


@hideCharges
def determine_platform_fee_with_IVA(booking: Booking) -> float:
    """
    Calculate the platform fee including IVA (VAT).
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Platform fee amount including IVA
    """
    return determine_platform_fee(booking) * 1.23


@hideCharges
def determine_owner_payment(booking: Booking, minusPlatIVA: bool = True) -> float:
    """
    Calculate the total payment to the property owner.
    
    Args:
        booking: The booking to calculate for
        minusPlatIVA: Whether to subtract platform IVA from the payment
        
    Returns:
        Owner payment amount
    """
    platFee = determine_platform_fee_IVA(booking) if minusPlatIVA else 0
    return (
        booking.charges.basicRental +
        booking.charges.extraNights -
        determine_commission(booking) - 
        platFee
    )


@hideCharges
def determine_owner_invoice(booking: Booking) -> float:
    """
    Calculate the invoice amount for the property owner.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Owner invoice amount
    """
    total = 0
    if not determine_need_for_invoice(booking):
        return total
    
    total += determine_commission(booking)
    if booking.property.owner.cleansAreInvoiced:
        total += determine_management_fee(booking)
    total += determine_platform_fee_with_IVA(booking)
    return total


@hideCharges
def determine_owner_balance(booking: Booking) -> float:
    """
    Calculate the owner's balance after deducting management fee.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Owner balance amount
    """
    return determine_owner_payment(booking) - determine_management_fee(booking)


@hideCharges
def determine_total_to_be_receipted(booking: Booking) -> float:
    """
    Calculate the total amount to be receipted.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Total amount to be receipted
    """
    rental = booking.charges.basicRental
    admin = booking.charges.adminFee
    platform = determine_platform_fee(booking)
    return rental + admin + platform


@hideCharges
def determine_total_paid_by_guest(booking: Booking) -> float:
    """
    Calculate the total amount paid by the guest.
    
    Args:
        booking: The booking to calculate for

    Returns:
        Total amount paid by the guest
    """
    if booking.details.isOwner:
        return 0
    if booking.details.isPlatform:
        return booking.charges.basicRental + booking.charges.platformFee
    return booking.charges.basicRental + booking.charges.adminFee


def determine_total_paid_to_klt(booking: Booking) -> float:
    """
    Calculate the total amount paid to KLT.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Total amount paid to KLT
    """
    return determine_klt_received_payment(booking)


@hideCharges
def determine_klt_received_payment(booking: Booking) -> float:
    """
    Calculate the total payment received by KLT.
    
    Args:
        booking: The booking to calculate for
        
    Returns:
        Total payment received by KLT
    """
    if booking.details.isOwner:
        return 0
    if booking.details.isPlatform:
        return booking.charges.basicRental
    return booking.charges.basicRental + booking.charges.adminFee        
        

def determine_commission_partition(booking: Booking) -> tuple[float, float]:
    """
    Determine the KLT and non-KLT portions of the commission.
    
    Args:
        booking: The booking to calculate for
    Returns:
        A tuple containing KLT and non-KLT commission amounts
    """
    if booking.arrival.year > 2026:
        return 1, 0
    if booking.arrival.year > 2023:
        return 2/3, 1/3
    return 3/5, 2/5

#######################################################
# GUEST INFORMATION PARSING FUNCTIONS
#######################################################

@isString
def determine_phonenumber(value: str) -> str | None:
    """
    Parse and format a phone number from text input.
    
    Args:
        value: The text containing a phone number
        
    Returns:
        Formatted phone number or None if invalid
    """
    def UK_or_PT(digits: str) -> str:
        if re.search(r'^9[1236]', digits):
            return '351' + digits 
        if digits[0:2] == '07':
            return '44' + digits[1:]
        return digits
    
    digits = only_digits_in_string(value)
    if len(digits) < 5:
        return None
    if digits[:2] == '00':
        digits = digits[2:]
    digits = UK_or_PT(digits)
    try:
        return format_number(
            parse_number('+' + digits), 
            PhoneNumberFormat.INTERNATIONAL)
    except:
        return digits


@isString
def determine_flight_number(value: str) -> str | None:
    """
    Extract a flight number from text input.
    
    Args:
        value: The text containing a flight number
        
    Returns:
        Flight number or None if not found
    """
    search = re.search(r'(^[a-z][a-z0-9][a-z]?[ ]?[0-9][0-9][0-9]?[0-9]?)', value.lower())
    if not search:
        return None
    if 'eta' in search.group(1).lower():
        return None
    return search.group(1).upper().replace(' ', '')


@isString
def determine_flight_time(value: str) -> tuple | None:
    """
    Extract flight time from text input.
    
    Args:
        value: The text containing a flight time
        
    Returns:
        Time as a tuple or None if not found
    """
    search = re.search(r'[0-9a-z][ ]+([012]?[0-9])[ Hh.:,;]?([0-5][0-9])', value)
    if not search:
        return None
    try: 
        return dates.time(search.group(1), search.group(2))
    except ValueError: 
        return search.group(1), search.group(2)


@isString
def determine_lisbon_in_string(value: str) -> bool | None:
    """
    Check if "Lisbon" is mentioned in the text.
    
    Args:
        value: The text to check
        
    Returns:
        True if Lisbon is mentioned, None if value is invalid
    """
    if not value: 
        return None
    if not isinstance(value, str): 
        return value 
    value = value.strip()
    return 'lisb' in value.lower()


@isString
def determine_hiring_a_car_in_string(value: str) -> bool:
    """
    Check if car hire is mentioned in the text.
    
    Args:
        value: The text to check
        
    Returns:
        True if car hire is mentioned
    """
    value = value.lower()
    if 'car' in value and 'hir' in value:
        return True
    if 'rent' in value and 'car' in value:
        return True
    return False


def determine_owner_family_in_name(name: str) -> bool:
    """
    Check if name indicates a property owner family member.
    
    Args:
        name: The name to check
        
    Returns:
        True if the name indicates a family member of the owner
    """
    name = name.lower()
    familyTerms = [
        'owner', 'parents', 'family', 'cousin', 'brother', 
        'sister', 'aunt', 'uncle', 'mother', 'father', 
        'friend', 'sobrinho'
    ]
    
    for term in familyTerms:
        if term in name:
            return True
            
    specialTerms = [
        r'(^| )tio( |$)',
        r'(^| )mãe( |$)',
        r'(^| )pai( |$)'
    ]
    
    for pattern in specialTerms:
        if re.search(pattern, name):
            return True
            
    return False


#######################################################
# EXTRAS DETERMINATION FUNCTIONS
#######################################################

@isListError
def determine_extras_in_list(values: list[str], booking: Booking = None) -> list[str]:
    """
    Determine extras requested based on a list of text values.
    
    Args:
        values: List of text strings to analyze
        booking: Optional booking to update with extras
        
    Returns:
        List of extra attributes identified
    """
    attrs = list()
    if booking and not isinstance(booking.extras.otherRequests, list):
        booking.extras.otherRequests = list()
    for value in values:
        value = value.strip().lower()
        if determine_owner_in_string(value):
            if booking:
                booking.extras.otherRequests.append(value)
        elif determine_airport_transfer_in_string(value):
            if determine_inbound_in_string(value):
                attrs.append('airportTransferInboundOnly')
            elif determine_outbound_in_string(value):
                attrs.append('airportTransferOutboundOnly')
            else:
                attrs.append('airportTransfers')
        elif determine_cot_and_chair_in_string(value):
            attrs.extend(['cot', 'highChair'])
        elif determine_cot_in_string(value):
            attrs.append('cot')
        elif determine_high_chair_in_string(value):
            attrs.append('highChair')
        elif determine_late_checkout_in_string(value):
            attrs.append('lateCheckout')
        elif determine_welcome_pack_in_string(value):
            attrs.append('welcomePack')
            if booking:
                mods = determine_welcome_pack_modifications_in_string(value)
                booking.extras.welcomePackModifications = mods
        elif determine_mid_stay_clean_in_string(value):
            attrs.append('midStayClean')
        else:
            if booking:
                booking.extras.otherRequests.append(value)
    if booking:
        for attr in attrs:
            setattr(booking.extras, attr, True)
    return attrs


def determine_price_of_extra(booking: Booking, extra: str) -> float:
    """
    Determine the price of a specific extra for a booking.
    
    Args:
        booking: The booking to check
        extra: The extra item to price
        
    Returns:
        Price of the extra
    """
    extra = to_string_or_error(extra).lower()
    if 'airport transfer' in extra:
        if 'inbound' in extra:
            if booking.details.totalGuests > 4:
                price = 60
            else:
                price = 45
            if booking.arrival.time > dates.time(20, 30):
                price += 10
            return price
        if 'outbound' in extra:
            if booking.details.totalGuests > 4:
                price = 60
            else:
                price = 45
            if booking.departure.time < dates.time(8, 30):
                price += 10
            return price
        if booking.details.totalGuests > 4:
            price = 114
        else:
            price = 84
        if booking.arrival.time > dates.time(20, 30):
            price += 10
        if booking.departure.time < dates.time(8, 30):
            price += 10
        return price
    if 'cot' in extra and 'high chair' in extra:
        if booking.totalNights < 10:
            return 35
        return 50
    if 'cot' in extra or 'high chair' in extra:
        if booking.totalNights < 10:
            return 25
        return 40
    if 'welcome pack' in extra:
        #if booking.extras.welcomePackModifications:
        #    return 40
        if booking.arrival.date > dates.date(2025, 12, 31):
            return 35
        return 30
    if 'mid-stay clean' in extra:
        if booking.property.specs.bedrooms == 1:
            return 60
        return 75
    if 'extra nights' in extra:
        return booking.charges.extraNights
    #return logerror(f'extra given to determine price of is not recognised: {extra}')


def determine_cot_and_chair_in_string(value: str) -> bool:
    """
    Check if text mentions both cot and high chair.
    
    Args:
        value: The text to check
        
    Returns:
        True if both cot and high chair are mentioned
    """
    return re.match(r'(^c[&+]?h$|cot[ +&]+h?i?g?h?[ ]*chair)', value.lower()) is not None


def determine_cot_in_string(value: str) -> bool:
    """
    Check if text mentions a cot.
    
    Args:
        value: The text to check
        
    Returns:
        True if cot is mentioned
    """
    return re.match(r'(cot|^c$)', value.lower()) is not None


def determine_high_chair_in_string(value: str) -> bool:
    """
    Check if text mentions a high chair.
    
    Args:
        value: The text to check
        
    Returns:
        True if high chair is mentioned
    """
    return re.match(r'(h?i?g?h?[ ]*chair|^hc$)', value.lower()) is not None


def determine_welcome_pack_in_string(value: str) -> bool:
    """
    Check if text mentions a welcome pack.
    
    Args:
        value: The text to check
        
    Returns:
        True if welcome pack is mentioned
    """
    return re.match(r'(w?e?l?c?o?m?e?[ ]?pack|^wp$)', value.lower()) is not None


def determine_welcome_pack_modifications_in_string(value: str) -> str | None:
    """
    Extract welcome pack modifications from text.
    
    Args:
        value: The text containing modifications
        
    Returns:
        Modifications string or None if not found
    """
    modifications = re.search(r'[ ]*\((.+)\)', value)
    if modifications: 
        return modifications.group(1)
    return None


def determine_late_checkout_in_string(value: str) -> bool:
    """
    Check if text mentions late check-out.
    
    Args:
        value: The text to check
        
    Returns:
        True if late check-out is mentioned
    """
    return re.match(r'(late check[-]?out|^lc$)', value.lower()) is not None


def determine_mid_stay_clean_in_string(value: str) -> bool:
    """
    Check if text mentions mid-stay cleaning.
    
    Args:
        value: The text to check
        
    Returns:
        True if mid-stay cleaning is mentioned
    """
    return re.match(r'(mid[-]?s?t?a?y?[ ]?clean|^mc$)', value.lower()) is not None


def determine_airport_transfer_in_string(value: str) -> bool:
    """
    Check if text mentions airport transfer.
    
    Args:
        value: The text to check
        
    Returns:
        True if airport transfer is mentioned
    """
    return re.match(r'^a?i?r?p?o?r?t?[ ]*transfer', value.lower()) is not None


def determine_inbound_in_string(value: str) -> bool:
    """
    Check if text mentions inbound transfer.
    
    Args:
        value: The text to check
        
    Returns:
        True if inbound is mentioned
    """
    return 'inbound' in value.lower()


def determine_outbound_in_string(value: str) -> bool:
    """
    Check if text mentions outbound transfer.
    
    Args:
        value: The text to check
        
    Returns:
        True if outbound is mentioned
    """
    return 'outbound' in value.lower()


def determine_owner_in_string(value: str) -> bool:
    """
    Check if text mentions property owner.
    
    Args:
        value: The text to check
        
    Returns:
        True if owner is mentioned
    """
    return 'owner' in value.lower()