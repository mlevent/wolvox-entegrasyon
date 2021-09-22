import re
import hashlib
from urllib.request import urlopen
from datetime import datetime
from unicode_tr import unicode_tr
import time
from datetime import datetime
from utils import titleFormat, slugFormat

'''
' TİTLE FORMATI
'''
def titleFormat2(string):
    string = re.sub(r"[^0-9]\s+[X]\s+[0-9]+", "x", string)
    return string