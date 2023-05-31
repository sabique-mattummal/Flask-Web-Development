
# Task 1 - Content collection from website using selenium
# Task - 2 Mail despatch system
#Task 3 - Timimg logic

# Import modules and class
from content import Content
from mail import MailDespatcher
import datetime
import html

# Objects from class 
content = Content()
mail_despatcher = MailDespatcher()

time_now = datetime.datetime.now().hour
morning_message = 'Good Morning'
evening_message = 'Good Evening'
email = 'to_mail'
message = content.create_quote().encode('utf-8')

if time_now == 7:
    day_wish = morning_message
    #mail_despatcher.sent_mail(email=email, message=message, day_wish=day_wish)
elif time_now == 19:
    day_wish = evening_message
    mail_despatcher.sent_mail(email=email, message=message, day_wish=day_wish)






