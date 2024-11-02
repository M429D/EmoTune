import streamlit as st
import time

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
    countdown = 10  # Countdown time in seconds
    for i in range(countdown, 0, -1):
        st.write(f"Closing this tab in {i} seconds...")
        time.sleep(1)  # Sleep for 1 second
    st.write('<script>window.close();</script>', unsafe_allow_html=True)

elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
    countdown = 10  # Countdown time in seconds
    for i in range(countdown, 0, -1):
        st.write(f"Closing this tab in {i} seconds...")
        time.sleep(1)  # Sleep for 1 second
    st.write('<script>window.close();</script>', unsafe_allow_html=True)

else:
    st.warning("No payment status provided.")
