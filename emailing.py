import imghdr
import smtplib

from email.message import EmailMessage


def get_credentials():
    with open("credentials", "r") as file:
        credentials_string = file.readline()
        credentials = credentials_string.split(" ")
        return credentials[0], credentials[1]


def send_email(image_path,
               email_receiver):

    # get the credentials
    email_sender, password_sender = get_credentials()

    email_message = EmailMessage()
    email_message["Subject"] = "New object in scene"
    email_message.set_content("Detected new object")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_sender, password_sender)
    gmail.sendmail(email_sender, email_receiver, email_message.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email("images/19.png", "lsocolovici@yahoo.com")
