from itertools import chain, combinations
from decimal import Decimal
import functools
import csv
import sys

def find_dishes(dishes, target_price):
  count = len(dishes)
  matches = []
  s = list(range(count))
  subsets = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
  for subset in subsets:
    sum = functools.reduce(lambda s,a : s + dishes[a][1], subset, Decimal('0.0'))
    if sum == target_price:
      dish_titles = ', '.join(map(lambda a : dishes[a][0], subset))
      matches.append(dish_titles)

  return matches


def parse_file(filename):
  target_price = None
  dishes = []
  with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
      if (len(row) == 0):
        continue

      if (len(row) != 2):
        raise Exception('CSV parse error at line: ' + ', '.join(row))

      if target_price is None and row[0] != 'Target price':
        raise Exception('Target price must be present in the beginning')

      try:
        value = Decimal(row[1].strip().lstrip('$'))
      except ValueError:
        raise Exception('Price is invalid at line: ' + ', '.join(row))

      if target_price is None:
        target_price = value
      else:
        dishes.append([row[0], value])

  return (dishes, target_price)


if (len(sys.argv) >= 2):
  filename = sys.argv[1]
  try:
    dishes, target_price = parse_file(filename)
    matches = find_dishes(dishes, target_price)
    if (len(matches) == 0):
      print('There is no combination of dishes that is equal to the target price')
    else:
      for match in matches:
        print(match)
  except Exception as err:
    print('Error: ' + str(err))
