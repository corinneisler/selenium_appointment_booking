import time
from datetime import datetime
import smtplib
from email.message import EmailMessage
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# Set driver and url
drv_path = "/Users/USERNAME/Downloads/chromedriver"
driver = webdriver.Chrome(drv_path)
url = 'https://migri.vihta.com/public/migri/#/reservation'
driver.get(url)
time.sleep(10)

try:
    #Find first dropdown element and select value (xpath found with "inspect element" on website)
    dropdown1 = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[4]/div[1]/div/div/button')
    dropdown1.send_keys(Keys.ENTER)

    kansalaisuusasia = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[4]/div[1]/div/div/ul/li[2]/a')
    kansalaisuusasia.click()
    time.sleep(2)

    #Find second dropdown element and select value
    dropdown2 = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[4]/div[2]/div/button')
    dropdown2.send_keys(Keys.ENTER)

    kansalaisuushakemus = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[4]/div[2]/div/ul/li[1]/a')
    kansalaisuushakemus.click()
    time.sleep(2)

    #Find third dropdown element and select value
    dropdown3 = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[7]/div/button')
    dropdown3.send_keys(Keys.ENTER)

    helsinki = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[7]/div/ul/li[1]/a')
    helsinki.click()
    time.sleep(2)

    #Click on "hae vapaat ajat"
    hae_vapaat_ajat = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/button')
    hae_vapaat_ajat.click()
    time.sleep(2)

    next_week = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[5]/div/div[1]/ul/li[13]/a') # arrow to next week
    first_week = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[5]/div/div[1]/ul/li[1]/a') # arrow to first week

    #Loop through the weeks and search for open time slots
    n = 8 # Number of times "next week" is clicked
    found = False
    ts = datetime.now()

    print('Iteration:', i, ts)

    while n >= 0:
        if n == 0: #Skip back to first week and start over
            first_week.click()
            time.sleep(2)
            #driver.refresh()
            n = 8
            i += 1 # Counting iterations
            ts = datetime.now()
            print('Iteration:', i, ts)

            continue
        else:
            next_week.click() # Always skip the current week
            time.sleep(2)
            n -= 1
            # Search for slot:
            # Get all links and match them with Regex pattern
            links = driver.find_elements_by_tag_name('a') # all links on the page
            for link in links:
                text = link.get_attribute('text') # Grab text of the link
                if not re.match('\s\d{2}:\d{2}', text): # Match it with pattern for timeslot
                    continue
                else:
                    open_slot = text.strip() # Remove whitespace
                found = True
                break
            if found:
                print('Appointment found:', open_slot)
                break

    # open_slot is a string, needs to be matched again to the web element
    time_slot = driver.find_element_by_link_text(open_slot)
    time_slot.click()
    time.sleep(3)

    varaa = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[5]/div/div[4]/span/div/div[2]/div/div/div[3]/span/button[1]')
    varaa.click()
    time.sleep(15)

    # Fill in personal data (need to replace place holders with actual data)
    f_etunimi = driver.find_element_by_xpath('//*[@id="inputFirstName"]')
    f_etunimi.send_keys('FIRST NAME')

    f_sukunimi =  driver.find_element_by_xpath('//*[@id="inputlastName"]')
    f_sukunimi.send_keys('LAST NAME')

    f_kansalaisuus = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[1]/div[1]/div/nationality-selector/div/select')
    f_kansalaisuus.click()
    f_kansalaisuus.send_keys('COUNTRY')
    f_kansalaisuus.send_keys(Keys.ENTER)

    f_syntymapaiva = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[2]/div/div/vihta-datepicker/div/select[1]')
    f_syntymapaiva.click()
    f_syntymapaiva.send_keys('DD')
    f_syntymapaiva.send_keys(Keys.ENTER)

    f_syntymakuukausi = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[2]/div/div/vihta-datepicker/div/select[2]')
    f_syntymakuukausi.click()
    f_syntymakuukausi.send_keys('MM')
    f_syntymakuukausi.send_keys(Keys.ENTER)

    f_syntymavuosi = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[2]/div/div/vihta-datepicker/div/select[3]')
    f_syntymavuosi.click()
    f_syntymavuosi.send_keys('YYYY')
    f_syntymavuosi.send_keys(Keys.ENTER)

    f_sukupuoli = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[1]/div[2]/div/gender-selector/div/div/button')
    f_sukupuoli.click()
    nainen = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/form/div[3]/div[1]/div[2]/div/gender-selector/div/div/ul/li[2]/a')
    nainen.click()

    f_sahkoposti = driver.find_element_by_xpath('//*[@id="inputEmail1"]')
    f_sahkoposti.click()
    f_sahkoposti.send_keys('EMAIL')
    f_sukupuoli.send_keys(Keys.ENTER)

    f_viesti =  driver.find_element_by_xpath('//*[@id="inputMessage"]')
    f_viesti.click()
    f_viesti.send_keys('Olen täyttänyt hakemuksen sähköisesti Enter Finlandissa (31.01.2021).')

    vahvista =  driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[4]/a')
    vahvista.click()
    print('Appointment booked!')


    # E-mail alert that time was found (in case autofilling doesn't work as expected)

    #Send email (need to enable IMAP in Gmail settings & allow less secure app access)
    msg = EmailMessage()
    msg.set_content('An appointment has been found, trying to book automatically. Please check.') #Text in email body

    msg['From'] = 'SENDER NAME'
    msg['To'] = 'RECEIVER NAME'
    msg['Subject'] = 'Appointment found'
    sender = 'SENDER EMAIL'
    receiver = ['RECEIVER EMAIL']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, 'PASSWORD')

    server.send_message(msg)
    print('Email sent')
    server.quit()

    time.sleep(10)

# Send email when an error occurrs
except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)

    # Send email
    msg = EmailMessage()
    msg.set_content('An error occured. Please check.') #Text in email body

    msg['From'] = 'SENDER NAME'
    msg['To'] = 'RECEIVER NAME'
    msg['Subject'] = 'Appointment found'
    sender = 'SENDER EMAIL'
    receiver = ['RECEIVER EMAIL']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, 'PASSWORD')

    server.send_message(msg)
    print('Error email sent')
    server.quit()
