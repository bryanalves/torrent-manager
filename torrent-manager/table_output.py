from prettytable import PrettyTable
from functools import partial
from .config import TORRENT_DIR
import criteria

def outputTable(torrents):
  R = "\033[0;31;40m" #RED
  G = "\033[0;32;40m" # GREEN
  # Y = "\033[0;33;40m" # Yellow
  # B = "\033[0;34;40m" # Blue
  N = "\033[0m" # Reset

  linked = partial(criteria.linked, torrent_dir=TORRENT_DIR)
  # CHECK_FUNCS = [linked]
  CHECK_FUNCS = [linked, criteria.age, criteria.ratio]
  table = PrettyTable(['Torrent', 'age', 'ratio'])

  for t in torrents:
    results = []
    add = True
    for func in CHECK_FUNCS:
      val = func(t)
      if func == linked:
        if val[1] == False:
          add = False
      else:
        color = G if val[1] == True else R
        results.append(color+val[0]+N)

    if add:
      table.add_row([t.name, *results])

  return table
