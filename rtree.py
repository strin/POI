# coding: utf-8
import sys, os, math

def create_datapoint(keys, vals):
  dp = dict()
  for (key, val) in zip(keys, vals):
    dp.update({key: val})
  return dp

def load_data(path):
  f = file(path).readlines()
  keys = f[0].split(',')
  data = list()
  for line in f[1:]:
    line = line.decode('utf-8')
    vals = line.split(',')
    data += [create_datapoint(keys, vals)]
  return data

def load_category(path):
  f = file(path).readlines()
  keys = f[0].split(',')
  (dict1, dict2, dict3) = (dict(), dict(), dict())
  name1 = name2 = None
  for (li, line) in enumerate(f[1:]):
    line = line.decode('utf-8')
    line = line.split(',')
    if line[2] != '':
      if len(dict3) > 0:
        dict2[name2] = dict3
        dict3 = dict()
      name2 = line[2]
    if line[0] != '':
      if len(dict2) > 0:
        dict1[name1] = dict2
        dict2 = dict()
      name1 = line[0]
    dict3[line[4]] = int(line[5])
  if len(dict3) > 0:
    dict2[name2] = dict3
  if len(dict2) > 0:
    dict1[name1] = dict2
  return dict1


def get_center_x(data):
  return float(data[0]['X_COORD'])

def get_center_y(data):
  return float(data[0]['Y_COORD'])

def get_category(data):
  return set([d['CATEGORY'] for d in data])

def distance(p1, p2):
  return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))





def nearest_neighbor(data, point, category = 0):
  min_dis = float('inf')
  min_d = None
  for d in data:
    p = (float(d['Y_COORD']), float(d['X_COORD']))
    c = int(d['CATEGORY'])
    if category == 0 or c == category:
      if distance(p, point) < min_dis:
        min_dis = distance(p, point)
        min_d = d
  return min_d

def range_search(data, point, range, category = 0):
  res = []
  for d in data:
    p = (float(d['Y_COORD']), float(d['X_COORD']))
    c = int(d['CATEGORY'])
    if category == 0 or c == category:
      if distance(p, point) <= range / float(110000): # divide by earth radius.
        res += [d]
  return res


if __name__ == '__main__':
  # data = load_data('data/POI_jiaotong.txt')
  category = load_category('data/category.csv')
  print ' '.join(category.keys())


