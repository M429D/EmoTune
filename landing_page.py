import streamlit as st

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # Access the first item

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
    log_payment_status("success")  # Log success to CSV
elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
    log_payment_status("fail")  # Log failure to CSV
else:
    st.warning("No payment status provided.")

