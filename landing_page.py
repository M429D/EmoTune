import streamlit as st
import gspread

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
else:
    st.warning("No payment status provided.")
