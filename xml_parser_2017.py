# -*- coding: utf-8 -*-
# @Author: yang
# @Date:   2017-03-31 12:40:21
# @Last Modified by:   yang
# @Last Modified time: 2017-04-05 20:48:03

import sys
import os
import re
try:
    import ujson as json  # UltraJSON if available
except:
    import json
from dateutil import parser as dateparser
from operator import itemgetter
from xml.etree import cElementTree as etree
from collections import defaultdict
from tqdm import tqdm

YEAR = 2017

counter = 0

# Assume all we need is Id,title, body,tags 

def parsexml(filename):
    
    counter_all = 0

    it = map(itemgetter(1),
             iter(etree.iterparse(filename, events=('start',))))

    root = next(it)  # get posts element

    try:
        for elem in tqdm(it):

            if counter_all == 100000 :
                break

            counter_all += 1

            if elem.tag == 'row' and int(elem.get('PostTypeId')) == 1 :  # if row and is question 
                year = dateparser.parse(elem.get('CreationDate')).year

                if year == YEAR:   
                    Id = int(elem.get('Id'))
                    title = elem.get('Title')
                    body =  elem.get('Body')
                    tags = elem.get('Tags')

                    if Id and title and body and tags:  # if not None
                        counter += 1
                        values = (Id,title,body,tags)
                        yield values

    except:
            print('bad value here', values)

    


with open('./data_2017', "w") as f:
    for values in parsexml('./Posts.xml'):
        line = "\t".join(map(str, values))
        f.write(line + "\n")

print('Finish! how many questions we have?',counter )

