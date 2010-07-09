from specstore import SpecStore
from pprint import pprint
import os

s=SpecStore(os.path.dirname(__file__))
pprint(s)
