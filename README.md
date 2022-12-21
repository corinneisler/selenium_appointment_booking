# selenium_appointment_booking

I created this Python script using Selenium to automatically book an appointment for me at the Finnish Immigration Service, as appointments were hard to come by and new slots usually were booked within only a few minutes. As I did not have time to constantly check for appointments myself, I created and ran this script that constantly searches for open appointment slots by imitating user behaviour on the website (clicking through the weeks, scanning for open time slots, clicking on the correct elements and filling in my personal data when an appointment becomes available). 

I also included error handling, so an automatic email was sent to me when an error arose. This happened a number of times when first using the script, as there were some issues with the code. But it is also handy in other situations, such as if the internet connection is interrupted.

I used the following resources (among others) to create this script:

https://selenium-python.readthedocs.io/locating-elements.html
https://medium.com/@rinu.gour123/python-send-email-via-smtp-ad2d259d7240
