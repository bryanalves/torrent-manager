import os
import glob

def linked(torrent, torrent_dir):
  root = os.path.join(torrent_dir, torrent.tag, torrent.name)

  if os.path.isdir(root):
    files = list(filter(os.path.isfile, glob.glob(glob.escape(root) + "/**", root_dir=root, recursive=True)))
    retval = all([os.stat(os.path.join(root, file)).st_nlink == 1 for file in files])
  else:
    retval = os.stat(root).st_nlink == 1

  return ("Unlinked" if retval else "Linked", retval)

def age(torrent, threshold = 24 * 7 * 2):
  return (str(torrent.age_hours)+'h', torrent.age_hours > threshold)

def ratio(torrent, threshold = 1.0):
  return (str(torrent.ratio)+'%', torrent.ratio > threshold)
