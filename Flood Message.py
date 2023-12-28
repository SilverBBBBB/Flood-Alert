import requests
import pywhatkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
def send_sms_via_email( Number:str, message:str, provider:str, sender_credential:tuple, subject:str, smtp_server="smtp.gmail.com", smtp_port=587):

# Sender credentials
    sender_email, password = sender_credential

    # Recipient's email (formatted for SMS)
    recipient_email = f"{7324077121}@tmomail.net"  # Example for TMobile; change domain for other carriers

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message
    msg.attach(MIMEText(message, 'plain'))

    # Setup the server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login Credentials for sending the email
    server.login(msg['From'], password)

    # Send the message
    server.send_message(msg)
    server.quit()


# The URL of the site to scrape
url = "https://water.weather.gov/ahps2/river.php?wfo=phi&wfoid=18692&riverid=203991&pt%5B%5D=145973&allpoints=145972%2C145973%2C144003%2C145974&data%5B%5D=all"

# Send a request to the website
response = requests.get(url)

# If the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the div with class 'stage_stage_flow'
    stage_div = soup.find("div", class_="stage_stage_flow")
    
    # If the div is found
    if stage_div:
        # Extract just the number from the returned string
        stage_text = stage_div.text.strip()  # E.g., "Latest Stage: 10.77"
        stage_value = float(stage_text.split()[-1])  # Split and convert the last element to float
        print("River stage:", stage_value)

        if stage_value > 5:
            message = f"The river is about to flood and is currently at {stage_value}"
            subject = f"Flood Alert"
            send_sms_via_email("7324077121", message, subject, ("lebovitche@gmail.com", "uddv nxgz ndgb penc"), "Flood Alert")
    else:
        print("The 'stage_stage_flow' div was not found.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
