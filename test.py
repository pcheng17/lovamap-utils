import itertools
import sys
import time
import threading


ids = list(result['global']['names'])
global_dict = {
    'names': [result['global']['names'][id] for id in ids],
    'values': [result['global']['values'][id] for id in ids],
}

intersubs_dict = {}
for id, str in result['intersubs']['names'].items():
    vals = result['intersubs']['values'][id]
    if isinstance(vals, matlab.double):
        # Need to "flatten" the list because every element comes wrapped in its own list.
        intersubs_dict[str] = [val for sublist in vals for val in sublist]
    else:
        intersubs_dict[str] = vals

subs_dict = {}
for id, str in result['subs']['names'].items():
    vals = result['subs']['values'][id]
    if isinstance(vals, matlab.double):
        # Need to "flatten" the list because every element comes wrapped in its own list.
        subs_dict[str] = [val for sublist in vals for val in sublist]
    else:
        subs_dict[str] = vals

if isinstance(result['isInteriorSub'], matlab.logical):
    result['isInteriorSub'] = [val for sublist in result['isInteriorSub'] for val in sublist]
