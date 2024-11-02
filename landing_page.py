import streamlit as st
import time

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
    
    # Initial message indicating that the order is being received
    receiving_message = "Twilight Coffee Shop is receiving your order for 5 seconds..."
    countdown_placeholder = st.empty()  # Create a placeholder for messages
    countdown_placeholder.write(receiving_message)
    
    # Wait for 5 seconds
    time.sleep(5)

    # After 5 seconds, show the order received message
    countdown_placeholder.write("Order has been received! You can close this tab now and view your order summary.")

elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
    
    # Similar receiving message for failed payment (if desired)
    receiving_message = "Twilight Coffee Shop is receiving your order for 5 seconds..."
    countdown_placeholder = st.empty()  # Create a placeholder for messages
    countdown_placeholder.write(receiving_message)
    
    # Wait for 5 seconds
    time.sleep(5)

    # After 5 seconds, show the order received message
    countdown_placeholder.write("Order has been received! You can close this tab now and view your order summary.")

else:
    st.warning("No payment status provided.")
