import requests
import json
from django.conf import settings

def initialize_payment(email, amount, reference, callback_url, metadata=None):
    """
    Initialize a Paystack payment transaction.
    
    Args:
        email: Customer's email
        amount: Amount in kobo (smallest currency unit)
        reference: Unique transaction reference
        callback_url: URL to redirect after payment
        metadata: Optional additional data
    
    Returns:
        dict: Response from Paystack API
    """
    url = "https://api.paystack.co/transaction/initialize"
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    
    # Amount should be in kobo (multiply by 100 for NGN)
    # For other currencies, adjust accordingly
    payload = {
        "email": email,
        "amount": int(amount * 100),  # Convert to kobo
        "reference": reference,
        "callback_url": callback_url,
    }
    
    if metadata:
        payload["metadata"] = metadata
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "Payment initialization failed"}


def verify_payment(reference):
    """
    Verify a Paystack payment transaction.
    
    Args:
        reference: Transaction reference
    
    Returns:
        dict: Verification response from Paystack API
    """
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": False, "message": "Payment verification failed"}


def generate_reference():
    """Generate a unique transaction reference"""
    import uuid
    return f"ORD-{uuid.uuid4().hex[:10].upper()}"