from datetime import datetime
import xmlrpc.client

def list(rpc_url):
  server = xmlrpc.client.Server(rpc_url)
  torrents = server.d.multicall2('', 'main',
    'd.hash=',
    'd.name=',
    'd.timestamp.finished=',
    'd.ratio=',
    'd.custom1=',
    'd.complete=',
    't.multicall=,"t.url="'
  )

  return [ Torrent(t) for t in torrents ]

class Torrent:
  def __init__(self, torrentdata):
    self._data = torrentdata
    self.hash = self._data[0]
    self.name = self._data[1]
    self.finished_at = datetime.fromtimestamp(self._data[2])
    self.ratio = self._data[3] / 1000
    self.tag = self._data[4]
    self.complete = self._data[5] == 1
    self.trackers = [tracker[0] for tracker in self._data[6]]

  @property
  def age_hours(self):
    return (datetime.now() - self.finished_at).total_seconds() // 3600
