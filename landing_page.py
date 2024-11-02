import streamlit as st
import time

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Payment success. Thank you for your patronage!")
   
    countdown_placeholder = st.empty()  # Create a placeholder for the countdown
    countdown_time = 30  # Start countdown from 7 seconds

    # Countdown loop
    for i in range(countdown_time, 0, -1):
        countdown_placeholder.write(f"Please close this tab and click 'I have paid' on our website to confirm your transaction within {i} seconds...")
        time.sleep(1)  # Sleep for 1 second
else:
    st.warning("No payment status provided.")
