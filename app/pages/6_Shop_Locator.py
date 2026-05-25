import streamlit as st
import time
import app.main as main
from app.components.sidebar import render_sidebar
from app.components.map_widget import render_farm_map
from core.location.geocoder import Geocoder
from core.location.shop_finder import ShopFinder
from core.payment.stripe_gateway import StripeGateway

st.set_page_config(page_title="Shop Locator & Fertilizer Marketplace", layout="wide")
main.load_css()
render_sidebar()

# Handle Stripe Checkout Flow State
if st.session_state.get('active_checkout_shop'):
    shop = st.session_state['active_checkout_shop']
    shop_name = shop.get('tags', {}).get('name', 'Local Agro Supplier')
    
    st.header(f"🛒 Secure Checkout: {shop_name}")
    st.markdown("Complete your purchase securely via **Stripe Payments**")
    
    colA, colB = st.columns([2, 1], gap="large")
    with colA:
        st.markdown("### 🛍️ Your Cart")
        
        # Pre-fill standard agricultural catalog if cart is empty
        if 'cart' not in st.session_state:
            st.session_state['cart'] = {
                "Urea (50kg Bag)": {"qty": 0, "price": 280.0},
                "DAP - Diammonium Phosphate (50kg Bag)": {"qty": 0, "price": 1350.0},
                "MOP - Muriate of Potash (50kg Bag)": {"qty": 0, "price": 1700.0},
                "Neem Cake Powder (25kg Bag)": {"qty": 0, "price": 850.0},
                "Liquid Seaweed Extract (5L)": {"qty": 0, "price": 450.0}
            }
            
        for item, details in st.session_state['cart'].items():
            cc1, cc2, cc3 = st.columns([3, 1, 1])
            with cc1:
                st.markdown(f"<div style='padding-top:8px;'><strong>{item}</strong> <br/> <small style='color:#94a3b8;'>₹{details['price']} per unit</small></div>", unsafe_allow_html=True)
            with cc2:
                qty = st.number_input("Qty", min_value=0, value=details['qty'], key=f"qty_{item}", label_visibility="collapsed")
                st.session_state['cart'][item]['qty'] = qty
            with cc3:
                st.markdown(f"<div style='padding-top:8px; font-weight:bold; color:#4ade80;'>₹{qty * details['price']:.2f}</div>", unsafe_allow_html=True)
                
        st.markdown("---")
        
    with colB:
        st.markdown("### 🧾 Order Summary")
        subtotal = sum(d['qty'] * d['price'] for d in st.session_state['cart'].values())
        delivery = 150.0 if subtotal > 0 else 0.0
        tax = subtotal * 0.05
        total = subtotal + delivery + tax
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Subtotal:</span> <span>₹{subtotal:.2f}</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>GST (5%):</span> <span>₹{tax:.2f}</span></div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>Delivery:</span> <span>₹{delivery:.2f}</span></div>
            <hr style="border-color: rgba(255,255,255,0.1);" />
            <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; color: #4ade80;"><span>Total:</span> <span>₹{total:.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if total > 0:
            if st.button("💳 Pay Securely with Stripe", use_container_width=True, type="primary"):
                with st.spinner("Connecting to Stripe Secure Gateway..."):
                    time.sleep(1.2) # Simulate network API latency
                    
                    # Generate real Stripe Checkout Link with raw shop_name
                    payment_data = StripeGateway.create_checkout_session(shop_name, st.session_state['cart'])
                    
                    if payment_data['status'] == 'success':
                        st.success("Stripe Payment Link Generated successfully!")
                        st.markdown(f"[**Click here to complete your transaction securely on Stripe**]({payment_data['url']})", unsafe_allow_html=True)
                    else:
                        st.error(f"Failed to generate checkout: {payment_data['message']}")
        else:
            st.warning("Please add items to your cart to proceed with checkout.")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("⬅️ Cancel & Return to Map", use_container_width=True):
            st.session_state['active_checkout_shop'] = None
            st.rerun()
            
    st.stop() # Halt rendering the main page layout while checkout is active

# --- Main Shop Locator & Marketplace Flow ---

st.header("📍 Agricultural Supplier Locator & Marketplace")
st.markdown("Search for verified agrochemical dealers, view their storefronts, and buy fertilizers securely using **Stripe**.")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Search Parameters")
    search_query = st.text_input("City/Region Override (Optional)", placeholder="e.g. Pune, India")
    radius = st.slider("Search Radius (km)", 5, 100, 25)
    btn = st.button("Scan OpenStreetMap & Load Storefronts", use_container_width=True)
    
# Initialize session states for map and search
if 'shop_markers' not in st.session_state:
    st.session_state['shop_markers'] = []
    
if 'search_coords' not in st.session_state:
    st.session_state['search_coords'] = (st.session_state.get('farm_lat', 0.0), st.session_state.get('farm_lon', 0.0))

with col2:
    if btn:
        with st.spinner("Geocoding and Querying Overpass API..."):
            target_lat = st.session_state.get('farm_lat', 0.0)
            target_lon = st.session_state.get('farm_lon', 0.0)
            
            if search_query:
                coords = Geocoder.get_coordinates(search_query)
                if coords:
                    target_lat, target_lon = coords
                else:
                    st.error("Geocoding failed for that location. Using default farm location.")
            
            radius_meters = radius * 1000
            shops = ShopFinder.find_nearby_shops(target_lat, target_lon, radius_meters)
            
            # Save into session state
            st.session_state['shop_markers'] = shops
            st.session_state['search_coords'] = (target_lat, target_lon)
            st.session_state['search_radius'] = radius
            
    current_lat, current_lon = st.session_state['search_coords']
    shops_to_render = st.session_state['shop_markers']
    r_val = st.session_state.get('search_radius', radius)
    
    if len(shops_to_render) > 0:
        st.success(f"Located {len(shops_to_render)} suppliers within {r_val}km.")
    else:
        st.info("No suppliers currently found or searched for. The map shows your active center.")

    # Render Interactive Map
    render_farm_map(current_lat, current_lon, markers=shops_to_render)
    
st.markdown("---")
if len(shops_to_render) > 0:
    st.subheader("🏪 Partnered Storefronts")
    st.markdown("Click on a storefront to open the marketplace and order fertilizers securely.")
    
    # Render elegant storefront cards
    grid_cols = st.columns(2)
    for idx, shop in enumerate(shops_to_render):
        shop_name = shop.get('tags', {}).get('name', 'Agro Supplier (Unnamed)')
        shop_type = shop.get('tags', {}).get('shop', 'agrochemical').capitalize()
        
        with grid_cols[idx % 2]:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.03); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                    <div>
                        <h4 style="margin: 0; color: #60a5fa; font-size: 1.15rem;">{shop_name}</h4>
                        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.85rem;">Verified {shop_type} Dealer</p>
                    </div>
                    <div style="background: rgba(59, 130, 246, 0.1); color: #60a5fa; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold;">
                        Partner
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🛍️ Order Supplies from {shop_name}", key=f"btn_order_{idx}", use_container_width=True):
                st.session_state['active_checkout_shop'] = shop
                if 'cart' in st.session_state:
                    del st.session_state['cart'] # Reset cart for new shop session
                st.rerun()

    st.markdown("---")
    with st.expander("View Raw Shop Directory (Location & Details)"):
        st.json(shops_to_render)
