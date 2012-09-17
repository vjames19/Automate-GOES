'''
Created on Sep 16, 2012

@author: TheZen
'''

import smtplib


def sendEmail(usr, psw,toaddr, msg):
    """
    Sends an email message through GMail once the script is completed.  
    Developed to be used with AWS so that instances can be terminated 
    once a long job is done. Only works for those with GMail accounts.
    
    

    usr : the GMail username, as a string

    psw : the GMail password, as a string 
         
    toaddr : a email address, or a list of addresses, to send the 
             message to
    """ 
    # Initialize SMTP server
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)
    
    # Send email
    subject="GOES-PRWEB LOG"
    m="From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (usr, toaddr, subject)
    server.sendmail(usr, toaddr, m+msg)
    server.quit()