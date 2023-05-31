import smtplib

my_email = "your_email"
password = "password"


class MailDespatcher:
    def sent_mail(self, email, message, day_wish):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email,
                msg=f"Subject:Greetings from BTS Army\n\n{day_wish}\n{message}")
