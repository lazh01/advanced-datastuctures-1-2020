import random;
import math;

levelcap = 32;
p = 0.5;

class SkipList:
  def __init__(self, height):
    self.head = [None] * height;
    self.maxlevel = height;
    self.level = height;
    self.size = 0;

def getSize(skipList):
  return skipList.size;

def  IncreaseMaximumLevelOfList(skiplist):
  level = maxlevel(skiplist);
  p = header(skiplist);
  q = forward(p)[level];
  while q is not None:
    if level(q) > level:
      forward(p)[level + 1] = q;
      p = q;
    q = forward(q)[level];
  forward(p)[level + 1] = None;
  skiplist.maxlevel = skiplist.maxlevel + 1;

def randomLevel():
  level = 1;
  while random.random() < p and level < levelcap:
    level = level + 1;
  return(level);


def header(skiplist):
  return skiplist;

def maxlevel(skiplist):
  return skiplist.maxlevel

class SkipListIndex:
  def __init__(self, key, height, value):
    self.key = key;
    self.value = value;
    self.head = [None] * height;
    self.level = height;

def forward(slindex):
  return slindex.head;

def Key(slindex):
  return slindex.key;

def getValue(slindex):
  return slindex.value;

def setValue(slindex, newValue):
  slindex.value = newValue;

def level(skiplist):
  return skiplist.level;

def L(n):
  if n == 0:
    return 0;
  return math.log(n, int(1/p));

def free(x):
  return;

def Search(skiplist, searchkey):
  x = header(skiplist);

  for i in reversed(range(maxlevel(x))):
    while forward(x)[i] is not None and Key(forward(x)[i]) < searchkey:
      x = forward(x)[i];
  x = forward(x)[0];
  if x is not None and Key(x) == searchkey:
    return getValue(x);
  else:
    return(None);

def insert(skiplist, searchKey, newValue):
  update = [None] * levelcap;
  x = header(skiplist);
  for i in reversed(range(maxlevel(skiplist))):
    while forward(x)[i] is not None and Key(forward(x)[i]) < searchKey:
      x = forward(x)[i];
    update[i] = x;
  x = forward(x)[0];

  if x is not None and Key(x) == searchKey:
    setValue(x, newValue);
    return None;
  else:
    x = SkipListIndex(searchKey, randomLevel(), newValue);
    for i in range (min(level(x), maxlevel(skiplist))):
      forward(x)[i] = forward(update[i])[i];
      forward(update[i])[i] = x;
  skiplist.size = skiplist.size + 1;
  if int(L(getSize(skiplist))) > maxlevel(skiplist):
    IncreaseMaximumLevelOfList(skiplist);
  return x;
  
def delete(skiplist, searchKey):
  update = [None] * levelcap;
  x = header(skiplist);
  for i in reversed(range(maxlevel(skiplist))):
    while forward(x)[i] is not None and Key(forward(x)[i]) < searchKey:
      x = forward(x)[i];
    update[i] = x;
  
  x = forward(x)[0];
  if x is not None and Key(x) == searchKey:
    for i in range (min(level(x), maxlevel(skiplist))):
      forward(update[i])[i] = forward(x)[i]; 
    free(x);
    skiplist.size = skiplist.size - 1;
    if(int(math.ceil(L(getSize(skiplist)))) < maxlevel(skiplist)):
      skiplist.maxlevel = skiplist.maxlevel - 1;
    return 1;
  return None;


#listp = SkipList(32);
#insert(listp, 89, 12);
#insert(listp, 23, 78);
#insert(listp, 104, 212);
#insert(listp, 50, 13);
#Delete(listp, 89);
#print(Search(listp, 104));