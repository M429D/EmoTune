import streamlit as st
import time

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Payment success. Thank you for your patronage!")
    
    countdown_placeholder = st.empty()  # Create a placeholder for the countdown
    countdown_time = 7  # Start countdown from 7 seconds

    # Countdown loop
    for i in range(countdown_time, 0, -1):
        countdown_placeholder.write(f"Twilight Coffee Shop is receiving your order in {i} seconds...")
        time.sleep(1)  # Sleep for 1 second

    # After countdown, show the order received message
    countdown_placeholder.write("Order has been received in the kitchen... You may close this tab now to view your order summary.")

elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
    
    countdown_placeholder = st.empty()  # Create a placeholder for the countdown
    countdown_time = 7  # Start countdown from 7 seconds

    # Countdown loop
    for i in range(countdown_time, 0, -1):
        countdown_placeholder.write(f"Redirecting user back to login page {i} seconds...")
        time.sleep(1)  # Sleep for 1 second

    # After countdown, show the order received message
    countdown_placeholder.write(f"<meta http-equiv='refresh' content='0; url=http://localhost:8501/'>", unsafe_allow_html=True)

else:
    st.warning("No payment status provided.")
