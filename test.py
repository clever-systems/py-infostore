from infostore import InfoStore
from pprint import pprint
import os

s=InfoStore(os.path.dirname(__file__)+'/example-infostore')
pprint(s)
