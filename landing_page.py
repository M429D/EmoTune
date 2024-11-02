import streamlit as st
import csv
import os

# Get the payment status from URL query parameters
payment_status = st.query_params.get("payment", [""])  # Access the first item

# Log payment status to a CSV file
def log_payment_status(status):
    file_path = "payment_status_log.csv"
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        # If the file doesn't exist, create it and write the header
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Status"])  # Write header
    
    # Read existing data
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        existing_data = list(reader)

    # Write back the header and the new status in the second row
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(existing_data[0])  # Write header
        # If there's existing data, write it to the third row
        if len(existing_data) > 1:
            for row in existing_data[1:]:
                writer.writerow(row)
        # Write the new status in the second row
        writer.writerow([status])  # Append the payment status

# Display the appropriate message based on payment status
if payment_status == "success":
    st.success("Thank you for your payment! Your order has been successfully processed.")
    log_payment_status("success")  # Log success to CSV
elif payment_status == "fail":
    st.error("Payment failed. Please try again or contact support.")
    log_payment_status("fail")  # Log failure to CSV
else:
    st.warning("No payment status provided.")

