import streamlit as st
import time

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Payment success. Thank you for your patronage!")
    st.write(f"Please close this tab and verify on our website that payment has been made to confirm your transaction.")
else:
    st.warning("No payment status provided.")
