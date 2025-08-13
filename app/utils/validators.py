import re
from typing import Optional
from pydantic import validator
import phonenumbers
from phonenumbers import NumberParseException


def validate_gstin(gstin: str) -> bool:
    """
    Validate GSTIN format
    Format: 15 characters - 2 digits (state code) + 10 alphanumeric (PAN) + 1 digit (entity number) + 1 alphabet (Z) + 1 alphanumeric (checksum)
    """
    if not gstin or len(gstin) != 15:
        return False
    
    # GSTIN pattern: 2 digits + 10 alphanumeric + 1 digit + Z + 1 alphanumeric
    pattern = r'^[0-9]{2}[A-Z0-9]{10}[0-9]{1}[Z]{1}[A-Z0-9]{1}$'
    return bool(re.match(pattern, gstin.upper()))


def validate_pan(pan: str) -> bool:
    """
    Validate PAN format
    Format: 5 letters + 4 digits + 1 letter
    """
    if not pan or len(pan) != 10:
        return False
    
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan.upper()))


def validate_phone_number(phone: str, country_code: str = "IN") -> bool:
    """
    Validate phone number using phonenumbers library
    """
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False


def validate_pincode(pincode: str) -> bool:
    """
    Validate Indian pincode format (6 digits)
    """
    if not pincode or len(pincode) != 6:
        return False
    
    return pincode.isdigit()


def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validate password strength
    Returns (is_valid, list_of_errors)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors


class GST:
    """GSTIN validation utilities"""
    
    @staticmethod
    def validate(gstin: str) -> bool:
        return validate_gstin(gstin)
    
    @staticmethod
    def extract_pan(gstin: str) -> Optional[str]:
        """Extract PAN from GSTIN"""
        if validate_gstin(gstin):
            return gstin[2:12]
        return None
    
    @staticmethod
    def extract_state_code(gstin: str) -> Optional[str]:
        """Extract state code from GSTIN"""
        if validate_gstin(gstin):
            return gstin[:2]
        return None


class Phone:
    """Phone number validation utilities"""
    
    @staticmethod
    def validate(phone: str, country_code: str = "IN") -> bool:
        return validate_phone_number(phone, country_code)
    
    @staticmethod
    def format(phone: str, country_code: str = "IN") -> Optional[str]:
        """Format phone number to international format"""
        try:
            parsed_number = phonenumbers.parse(phone, country_code)
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            pass
        return None