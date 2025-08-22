import streamlit as st
from datetime import datetime
import io
import time  # for wait delay

# Set page config
st.set_page_config(page_title="Cloud SuperMart Billing System", layout="centered")

# Title
st.title("🛒 Cloud SuperMart Billing System")

# Customer details
name = st.text_input("Enter your Name:")
phone = st.text_input("Enter your Phone Number:")

# Show item list
if st.checkbox("Show Items List"):
    st.markdown("""
    ### 🛍 Available Items:
    - Flour/Atta: Starting from Rs 20  
    - Dal/Lentils: Starting from Rs 60  
    - Coffee: Starting from Rs 50  
    - Tea: Starting from Rs 50  
    - Sugar: Rs 30/kg  
    - Spices: Starting from Rs 60  
    - Rice: Rs 500 - 2,000 (per family pack)  
    - Dairy Products: Rs 40 - 300 (per litre/pack)  
    - Snacks: Rs 30 - 500 (per pack/assortment)  
    - Beverages: Rs 50 - 1,500 (per bottle/pack)  
    - Salt: Rs 20/kg  
    - Oil: Rs 80/kg  
    - Paneer: Rs 110/kg  
    - Maggie: Rs 50/pack  
    - Boost: Rs 90/pack  
    - Colgate: Rs 85/pack  
    """)

# Items dictionary (fixed billing prices for simplicity)
items = {
    # Grocery & staples
    "flour/atta": 20,
    "dal/lentils": 60,
    "coffee": 50,
    "tea": 50,
    "sugar": 30,
    "spices": 60,
    "rice (family pack)": 500,
    "salt": 20,
    "oil": 80,
    # Other items
    "dairy products": 40,
    "snacks": 30,
    "beverages": 50,
    "paneer": 110,
    "maggie": 50,
    "boost": 90,
    "colgate": 85
}

# Session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.subheader("🛍 Select Items to Add to Cart")

# Multi-select for items
selected_items = st.multiselect("Choose items:", options=list(items.keys()))

# Collect quantities for each selected item
item_quantities = {}
if selected_items:
    st.markdown("#### Enter Quantity for Selected Items:")
    for item in selected_items:
        qty = st.number_input(f"{item} (Rs {items[item]}/unit):", min_value=1, step=1, key=item)
        item_quantities[item] = qty

# Add to cart button
if st.button("Add Selected Items to Cart"):
    for item, qty in item_quantities.items():
        price = qty * items[item]
        st.session_state.cart.append({
            "item": item,
            "quantity": qty,
            "unit_price": items[item],
            "price": price
        })
    st.success("✅ Items added to cart!")

# Display Cart & Generate Bill
if st.session_state.cart:
    st.subheader("🧾 Your Cart")
    total = sum(i['price'] for i in st.session_state.cart)
    gst = total * 0.05
    subtotal_with_gst = total + gst

    # Discount logic
    discount = 0
    if subtotal_with_gst > 2500:
        discount = subtotal_with_gst * 0.15
        discount_msg = "15% Discount Applied 🎉"
    elif subtotal_with_gst > 1000:
        discount = subtotal_with_gst * 0.10
        discount_msg = "10% Discount Applied 🎉"
    else:
        discount_msg = "No Discount"

    final_amount = subtotal_with_gst - discount

    # Cart table
    cart_table = {
        "Item": [i["item"] for i in st.session_state.cart],
        "Quantity": [i["quantity"] for i in st.session_state.cart],
        "Unit Price (Rs)": [i["unit_price"] for i in st.session_state.cart],
        "Price (Rs)": [i["price"] for i in st.session_state.cart]
    }

    st.table(cart_table)

    st.markdown("---")
    st.markdown(f"*Subtotal:* Rs {total}")
    st.markdown(f"*GST (5%):* Rs {gst:.2f}")
    st.markdown(f"*{discount_msg}* (-Rs {discount:.2f})")
    st.markdown(f"### 🧾 Final Amount: Rs {final_amount:.2f}")
    st.markdown("---")

    # Bill format
    if st.button("Generate Bill"):
        st.subheader("🧾 Bill Receipt")

        # Placeholder for waiting message
        placeholder = st.empty()
        placeholder.info("🕒 Generating bill... Please wait 3 seconds")
        time.sleep(3)  # wait before showing bill

        bill_content = f"""
        ============================================
                Cloud SuperMart Billing System
        ============================================
        Customer Name : {name}
        Phone Number  : {phone}
        Date & Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        --------------------------------------------
        Items Purchased:
        """

        for i, entry in enumerate(st.session_state.cart):
            bill_content += f"\n{i+1}. {entry['item'].title()} - {entry['quantity']} unit(s) - Rs {entry['price']}"

        bill_content += f"""
        --------------------------------------------
        Subtotal       : Rs {total}
        GST (5%)       : Rs {gst:.2f}
        {discount_msg} : -Rs {discount:.2f}
        Final Amount   : Rs {final_amount:.2f}
        ============================================
         🎉 Thank you for shopping at Cloud SuperMart!
               Visit us again!
        ============================================
        """

        # Replace loading message with bill
        placeholder.text(bill_content)

        # Download option
        bill_file = io.BytesIO(bill_content.encode())
        st.download_button(
            label="⬇️ Download Bill",
            data=bill_file,
            file_name=f"Bill_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # Success message after bill is shown
        st.success("✅ Bill Generated Successfully! 🎉 Thank you for shopping at Cloud SuperMart. Visit us again.")
