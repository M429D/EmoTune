import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Initialize Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("dv-project-440516-059101c7605a.json", scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Payment_Status").sheet1  # Replace with your sheet name

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # 'success' or 'fail'

# Record the payment status in Google Sheets
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
    sheet.update("A1", "success")  # Adjust the cell as needed
elif payment_status == "fail":
    st.error("Payment failed. Please try again.")
    sheet.update("A1", "fail")
else:
    st.warning("No payment status provided.")
    sheet.update("A1", "unknown")

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
else:
    st.warning("No payment status provided.")
