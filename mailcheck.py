import re
import argparse
import whois # modulepython-whois
import dns.resolver# DNSPYTHON

# [x] parse arguments
# [x] check email format
# [x] check if domain name is valid
# [x] extract MX records
# [ ] check with SMTP

#
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', type=str, help="Email")
    return parser.parse_args()

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
    for x in dns.resolver.resolve(domain, 'MX'):
        print(x.to_text())


args = parse_args()
mail = args.email

temp = "Adresse: " + mail 
emailFormatValid(mail)
print(temp)
print(getDomain(mail))
dom = "Validité domain: " + str(isDomainValid(getDomain(mail)))
print(dom)
print("MX extraction")
mxResolver(getDomain(mail))