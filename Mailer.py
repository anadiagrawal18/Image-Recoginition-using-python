import smtplib

def sendmail():
    my_email = "triadsmain@gmail.com"
    password = "czfsnnrgqtgtvads"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,to_addrs="nomeshpatel@gmail.com",msg="Subject: INVADER ALERT \n\nPLEASE HAVE A CHECK ON THE SECURITY FOOTAGE!!!")