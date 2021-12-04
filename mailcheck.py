import re
import argparse
import whois # module python-whois
import dns.resolver# DNSPYTHON
import socket
import smtplib
#
# [x] parse arguments
# [x] check email format
# [x] check if domain name is valid
# [x] extract MX records
# [ ] check with SMTP

#
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--email', type=str, help="Email")
args = parser.parse_args()

def emailFormatValid(email):
    EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    if not re.match(EMAIL_REGEX, email):
        print("Email format is invalid")
        exit()

def getDomain(email):
    DOMAIN_REGEX = r'(?<=@).*'
    emailDomain = re.search(DOMAIN_REGEX, email)
    return emailDomain.group()

def isDomainValid(domain):
    try:
        quiEst = whois.whois(domain)
        return True
    except:
        return False

def mxResolver(domain):
    records = dns.resolver.resolve(domain, 'MX')
    mxRecord = records[0].exchange
    for x in dns.resolver.resolve(domain, 'MX'):
        print(x.to_text())
    return str(mxRecord)

def smtpChat(): # source: https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    # Assume 250 as Success
    if code == 250:
        print('Y')
    else:
        print('N')

mail = args.email

temp = "Adresse: " + mail 
emailFormatValid(mail)
print(temp)
print(getDomain(mail))
dom = "Validité domain: " + str(isDomainValid(getDomain(mail)))
print(dom)
print("MX extraction")
print(mxResolver(getDomain(mail)))
