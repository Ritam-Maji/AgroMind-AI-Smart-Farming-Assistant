import os
import uuid
import time
from typing import Dict, Any
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("StripeGateway")

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False

class StripeGateway:
    
    @staticmethod
    def create_checkout_session(shop_name: str, cart_items: dict) -> Dict[str, Any]:
        """
        Creates a real Stripe Checkout Session.
        The supplier's raw shop name is passed as product metadata and in descriptions.
        """
        stripe_key = os.getenv("STRIPE_SECRET_KEY")
        
        if not STRIPE_AVAILABLE:
            return {"status": "error", "message": "Stripe python library is not installed."}
            
        if not stripe_key:
            return {"status": "error", "message": "Stripe API Key missing. Please add STRIPE_SECRET_KEY to your .env file to enable actual payments."}
            
        stripe.api_key = stripe_key
        
        line_items = []
        subtotal = 0.0
        
        # Build standard cart items
        for item_name, details in cart_items.items():
            if details["qty"] > 0:
                subtotal += details["qty"] * details["price"]
                line_items.append({
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": item_name,
                            "description": f"Supplied locally by {shop_name}",
                        },
                        "unit_amount": int(details["price"] * 100), # Stripe uses the smallest currency unit (paise)
                    },
                    "quantity": details["qty"],
                })
                
        # Append Delivery and GST tax dynamically
        if subtotal > 0:
            delivery = 150.0
            tax = subtotal * 0.05
            
            line_items.append({
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "Delivery Fee", 
                        "description": f"Direct delivery from {shop_name}"
                    },
                    "unit_amount": int(delivery * 100),
                },
                "quantity": 1,
            })
            
            line_items.append({
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "GST (5%)", 
                        "description": "Government Agricultural Tax"
                    },
                    "unit_amount": int(tax * 100),
                },
                "quantity": 1,
            })
        
        if not line_items:
            return {"status": "error", "message": "Cart is empty."}
            
        try:
            logger.info(f"Generating real Stripe Checkout Session for order at {shop_name}")
            
            # Create actual Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="https://agromind.local/success", # In a real deployment, replace with actual app URL
                cancel_url="https://agromind.local/cancel",
                metadata={
                    "supplier_shop_name": shop_name,
                    "order_source": "AgroMind Desktop App"
                }
            )
            
            return {
                "status": "success",
                "id": session.id,
                "url": session.url
            }
            
        except Exception as e:
            logger.error(f"Stripe API Error: {str(e)}")
            return {"status": "error", "message": f"Stripe Error: {str(e)}"}
