import os
import uuid
import time
from typing import Dict, Any, Optional
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("RazorpayGateway")

try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False

class RazorpayGateway:
    
    @staticmethod
    def get_client() -> Optional[Any]:
        key_id = os.getenv("RAZORPAY_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        
        if RAZORPAY_AVAILABLE and key_id and key_secret:
            return razorpay.Client(auth=(key_id, key_secret))
        return None
        
    @staticmethod
    def create_payment_link(amount_inr: float, description: str, customer_details: Dict[str, str]) -> Dict[str, Any]:
        """
        Creates a Razorpay Payment Link.
        If real API keys and the razorpay package are missing, it generates a Mock Razorpay Checkout session.
        """
        client = RazorpayGateway.get_client()
        amount_paise = int(amount_inr * 100) # Razorpay accepts amounts in paise
        
        if client:
            try:
                logger.info(f"Generating real Razorpay Payment Link for {amount_inr} INR")
                payment_link = client.payment_link.create({
                    "amount": amount_paise,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": description,
                    "customer": {
                        "name": customer_details.get("name", "Farmer"),
                        "email": customer_details.get("email", "farmer@agromind.com"),
                        "contact": customer_details.get("contact", "+919999999999")
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "notes": {
                        "source": "AgroMind Desktop App"
                    }
                })
                
                return {
                    "status": "success",
                    "type": "real",
                    "id": payment_link.get("id"),
                    "url": payment_link.get("short_url")
                }
            except Exception as e:
                logger.error(f"Razorpay API Error: {str(e)}. Falling back to mock gateway.")
                
        # Mock Razorpay Gateway Response
        logger.info("Using Razorpay Mock Gateway...")
        mock_id = f"plink_mock_{uuid.uuid4().hex[:12]}"
        
        return {
            "status": "success",
            "type": "mock",
            "id": mock_id,
            "url": f"#mock_razorpay_checkout_{mock_id}",
            "amount": amount_inr,
            "description": description
        }
