import requests

class FloodAPI:
  def __init__(self, root):
    self._root = root

  def login(self, username, password):
    url = f"{self._root.rstrip('/')}/api/auth/authenticate"
    data = {'username': username, 'password': password}
    res = requests.post(url, json=data)
    if res.status_code == 200:
      return res.cookies['jwt']

  def delete(self, torrent_hash, cookie):
    cookies = {'jwt': cookie}

    url = f"{self._root.rstrip('/')}/api/torrents/delete"
    data = {'hashes': [torrent_hash], 'deleteData': True}
    return requests.post(url, json=data, cookies=cookies)
