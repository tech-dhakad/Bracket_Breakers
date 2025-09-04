# app.py
# Mini Online Store: Catalog + Cart + Checkout (Simulated Payment)
# Run: pip install streamlit
#      streamlit run app.py

import streamlit as st
from dataclasses import dataclass, asdict
from typing import List, Dict

st.set_page_config(page_title="Mini Store", page_icon="🛍️", layout="wide")

# -----------------------
# Helpers
# -----------------------
def inr(x: float) -> str:
    return f"₹{x:,.2f}"

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

# -----------------------
# Data models & seed data
# -----------------------
@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str
    image_url: str
    stock: int

PRODUCTS: List[Product] = [
    Product(1, "Wireless Earbuds", 1499.0, "Bluetooth 5.3 — long battery", "https://images.unsplash.com/photo-1585386959984-a4155223168f?q=80&w=800&auto=format&fit=crop", 25),
    Product(2, "Smartwatch", 2999.0, "AMOLED, SpO2, IP68", "https://images.unsplash.com/photo-1518443895914-046387b1ae47?q=80&w=800&auto=format&fit=crop", 15),
    Product(3, "Gaming Mouse", 899.0, "High DPI, programmable buttons", "https://images.unsplash.com/photo-1527814050087-3793815479db?q=80&w=800&auto=format&fit=crop", 40),
    Product(4, "Mechanical Keyboard", 2499.0, "Hot-swap, RGB, compact", "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?q=80&w=800&auto=format&fit=crop", 12),
]

COUPONS = {"WELCOME10": 0.10, "FESTIVE5": 0.05}

# -----------------------
# Session state
# -----------------------
if "products" not in st.session_state:
    st.session_state.products = [asdict(p) for p in PRODUCTS]
if "cart" not in st.session_state:
    st.session_state.cart: Dict[int, Dict] = {}   # pid -> {"qty": n}
if "orders" not in st.session_state:
    st.session_state.orders: List[Dict] = []
if "applied_coupon" not in st.session_state:
    st.session_state.applied_coupon = None
if "coupons" not in st.session_state:
    st.session_state.coupons = COUPONS

# -----------------------
# Product/cart helpers
# -----------------------
def get_product(pid: int):
    for p in st.session_state.products:
        if p["id"] == pid:
            return p
    return None

def add_to_cart(pid: int, qty: int = 1):
    p = get_product(pid)
    if not p:
        st.error("Product not found.")
        return
    if p["stock"] <= 0:
        st.warning("Out of stock.")
        return
    current = st.session_state.cart.get(pid, {"qty": 0})["qty"]
    new_qty = clamp(current + qty, 0, p["stock"])
    st.session_state.cart[pid] = {"qty": new_qty}
    st.toast(f"Added {p['name']} x{qty}")

def set_qty(pid: int, qty: int):
    p = get_product(pid)
    if not p:
        return
    if qty <= 0:
        st.session_state.cart.pop(pid, None)
    else:
        st.session_state.cart[pid] = {"qty": clamp(qty, 0, p["stock"])}

def remove_from_cart(pid: int):
    st.session_state.cart.pop(pid, None)

def cart_items():
    items = []
    for pid, meta in st.session_state.cart.items():
        p = get_product(pid)
        if p and meta["qty"] > 0:
            items.append({"product": p, "qty": meta["qty"], "subtotal": p["price"] * meta["qty"]})
    return items

def cart_totals():
    items = cart_items()
    subtotal = sum(it["subtotal"] for it in items)
    discount = 0.0
    if st.session_state.applied_coupon:
        rate = st.session_state.coupons.get(st.session_state.applied_coupon, 0.0)
        discount = subtotal * rate
    shipping = 0 if subtotal >= 1999 else 49
    tax = 0.18 * (subtotal - discount)
    total = subtotal - discount + shipping + tax
    return {"subtotal": subtotal, "discount": discount, "shipping": shipping, "tax": tax, "total": total}

# -----------------------
# UI
# -----------------------
def header():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        st.markdown("### 🛍️ Mini Store")
    with c2:
        st.text_input("Search", key="q", placeholder="Search products...")
    with c3:
        count = sum(v["qty"] for v in st.session_state.cart.values())
        st.markdown(f"#### 🧺 {count}")

tabs = st.tabs(["Catalog", "Cart", "Checkout", "Orders"])
header()

# --- Catalog ---
with tabs[0]:
    query = (st.session_state.get("q") or "").strip().lower()
    products = st.session_state.products
    if query:
        products = [p for p in products if query in p["name"].lower() or query in p["description"].lower()]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            st.image(p["image_url"], use_container_width=True)
            st.markdown(f"**{p['name']}**")
            st.caption(p["description"])
            st.write(inr(p["price"]))
            st.caption(f"Stock: {p['stock']}")
            qty_key = f"qty_{p['id']}"
            qty = st.number_input("Qty", min_value=1, max_value=p["stock"], value=1, key=qty_key)
            if st.button("Add to cart", key=f"add_{p['id']}"):
                add_to_cart(p["id"], qty)

# --- Cart ---
with tabs[1]:
    items = cart_items()
    if not items:
        st.info("Cart is empty. Add items from Catalog.")
    else:
        st.subheader("Your Cart")
        for it in items:
            p = it["product"]
            cols = st.columns([3,1])
            with cols[0]:
                st.markdown(f"**{p['name']}** — {inr(p['price'])}")
                st.caption(p["description"])
            with cols[1]:
                q = st.number_input(f"Qty {p['id']}", min_value=0, max_value=p["stock"], value=it["qty"], key=f"cart_qty_{p['id']}")
                set_qty(p["id"], q)
                if st.button("Remove", key=f"remove_{p['id']}"):
                    remove_from_cart(p["id"])

        st.divider()
        left, right = st.columns([2,1])
        with left:
            st.subheader("Coupon")
            code = st.text_input("Coupon code", key="coupon_input", placeholder="WELCOME10")
            if st.button("Apply coupon"):
                code_up = (code or "").strip().upper()
                if code_up in st.session_state.coupons:
                    st.session_state.applied_coupon = code_up
                    st.success(f"Coupon {code_up} applied")
                else:
                    st.warning("Invalid coupon")
        with right:
            totals = cart_totals()
            st.write("Subtotal:", inr(totals["subtotal"]))
            st.write("Discount:", "-" + inr(totals["discount"]) if totals["discount"] else inr(0))
            st.write("Shipping:", inr(totals["shipping"]))
            st.write("Tax (18%):", inr(totals["tax"]))
            st.markdown("**Total:** " + inr(totals["total"]))
            if st.button("Proceed to Checkout"):
                st.session_state._active_tab = "Checkout"
                st.experimental_rerun()

# --- Checkout ---
with tabs[2]:
    items = cart_items()
    if not items:
        st.info("Add items to cart first.")
    else:
        totals = cart_totals()
        st.subheader("Checkout")
        with st.form("checkout_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Shipping address")
            payment = st.selectbox("Payment method", ["Simulated (UPI/Card)"])
            submitted = st.form_submit_button("Pay")
            if submitted:
                if not name or not email or not address:
                    st.warning("Fill name, email, and address.")
                else:
                    # Simulated payment — create order immediately
                    order = {
                        "buyer": {"name": name, "email": email, "phone": phone, "address": address},
                        "items": [{"id": it["product"]["id"], "name": it["product"]["name"], "price": it["product"]["price"], "qty": it["qty"], "subtotal": it["subtotal"]} for it in items],
                        "totals": totals,
                        "status": "Paid",
                        "payment_ref": f"SIM-{len(st.session_state.orders)+1:05d}"
                    }
                    st.session_state.orders.append(order)
                    # decrement stock
                    for it in items:
                        pid = it["product"]["id"]
                        p = get_product(pid)
                        if p:
                            p["stock"] = max(0, p["stock"] - it["qty"])
                    # clear cart
                    st.session_state.cart = {}
                    st.session_state.applied_coupon = None
                    st.success(f"Payment successful! Ref: {order['payment_ref']}")
                    st.balloons()
                    st.experimental_rerun()

        with st.expander("Order summary"):
            for it in items:
                st.write(f"- {it['product']['name']} x {it['qty']} = {inr(it['subtotal'])}")
            st.write("---")
            st.write("Subtotal:", inr(totals["subtotal"]))
            st.write("Discount:", inr(totals["discount"]))
            st.write("Shipping:", inr(totals["shipping"]))
            st.write("Tax:", inr(totals["tax"]))
            st.markdown("**Total:** " + inr(totals["total"]))

# --- Orders ---
with tabs[3]:
    if not st.session_state.orders:
        st.info("No orders yet.")
    else:
        st.subheader("Orders")
        for idx, o in enumerate(reversed(st.session_state.orders), start=1):
            st.markdown(f"**Order #{len(st.session_state.orders)-idx+1} — {o['status']}**")
            st.caption(f"Payment Ref: {o['payment_ref']}")
            st.write(f"Buyer: {o['buyer']['name']} — {o['buyer']['email']}")
            with st.expander("Items"):
                for it in o["items"]:
                    st.write(f"- {it['name']} x {it['qty']} = {inr(it['subtotal'])}")
            st.write("Total Paid:", inr(o["totals"]["total"]))
