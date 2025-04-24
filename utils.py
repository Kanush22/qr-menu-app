import qrcode
import os

def generate_qr(table_id, url_base="https://your-app-name.streamlit.app"):
    """
    Generates a QR code for a given table that directs to the Streamlit app with the table_id in the query.
    """
    # Include table_id in the URL to direct to the correct table menu
    qr_url = f"{url_base}?table_id={table_id}"
    
    # Generate the QR code image
    qr = qrcode.make(qr_url)

    # Ensure the 'qr_codes' folder exists
    os.makedirs("qr_codes", exist_ok=True)  # Create the folder if it doesn't exist
    
    # Save the QR code as a PNG image in the 'qr_codes' folder
    path = f"qr_codes/{table_id}.png"
    qr.save(path)
    
    # Return the file path
    return path
