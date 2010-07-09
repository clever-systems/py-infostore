from specstore import InfoStore
from pprint import pprint
import os

s=InfoStore(os.path.dirname(__file__))
pprint(s)
