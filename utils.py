import re
import hashlib
from urllib.request import urlopen
from datetime import datetime
from unicode_tr import unicode_tr
from slugify import slugify

'''
' CONNECTION TEST
'''
def networkOn():
    try:
        urlopen('http://google.com', timeout=1)
        return True
    except: 
        return False

'''
' HOUR CONTROL
'''
def checkHour():
    now = datetime.now()
    if now.hour >= 8:
        return True 

'''
' SLUG
'''
def slugFormat(string):
    return slugify(string)

'''
' VALUE
'''
def getValue(data, lower = False):
    return str('') if data is None else str((upperFormat(data) if lower == False else lowerFormat(data)))

'''
' DATE FORMAT
'''
def getCurDateXml(fDateTime, dTime = True):

    if fDateTime is not None:
        nowDate = datetime.strptime(str(fDateTime), "%Y-%m-%d %H:%M:%S")
    else:
        nowDate = datetime.now()

    nowTime = nowDate.strftime("%H:%M:%S")
    secTime = sum(int(x) * 60 ** i for i, x in enumerate(reversed(nowTime.split(':'))))

    date1 = datetime(1899, 12, 30, 0, 0, 0)
    delta = nowDate - date1

    getDate = delta.days
    getTime = int(secTime*115.740)

    if dTime:
        return ','.join([str(getDate), str(getTime)])
    else:
        return getDate

'''
' MD5 HASH
'''
def getHash(string):
    return hashlib.md5(string.encode()).hexdigest()

'''
' UPPER FORMAT
'''
def upperFormat(string):
    return unicode_tr(string).upper()

'''
' LOWER FORMAT
'''
def lowerFormat(string):
    return unicode_tr(string).lower()

'''
' ŞU ANKİ ZAMAN
'''
def nowTime(today = False):
    return datetime.strftime(datetime.now(), ("%d.%m.%Y 00:00:00" if today else "%d.%m.%Y %H:%M:%S"))

'''
' SANİYE FARKI
'''
def diffSecond(time1, time2):
    d = datetime.strptime(time1, "%d.%m.%Y %H:%M:%S")
    n = datetime.strptime(time2, "%d.%m.%Y %H:%M:%S")
    return (n-d).total_seconds()

'''
' MİKROSANİYE TO SANİYE
'''
def toSecond(second):
    return (second * 1000)

'''
' SPAN
'''
def spanStyle(string, color = '#000'):
    return '<span style="font-weight:bold;color:%s">%s</span>' % (color, string)