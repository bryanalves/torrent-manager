from flask import Flask, make_response, request, render_template
from functools import partial
import json

from . import criteria
from . import torrent
from .floodapi import FloodAPI
from .config import TORRENT_ROOT, TORRENT_DIR, FLOOD_ROOT, FLOOD_USER, FLOOD_PASS

app = Flask(__name__)
flood = FloodAPI(FLOOD_ROOT)

@app.template_filter()
def colorformat(val):
  color = 'text-success' if val[1] else 'text-danger'
  return "<span class='%s'>%s</span>" % (color, val[0])

@app.route('/')
def index():
  app.config['jwt'] = flood.login(FLOOD_USER, FLOOD_PASS)
  torrents = [t for t in torrent.list(TORRENT_ROOT) if t.complete]
  torrents.sort(key=lambda x: x.name.lower())

  linked = partial(criteria.linked, torrent_dir=TORRENT_DIR)

  ignored = json.loads(request.cookies.get('ignored') or '[]')

  data = [[], []]
  for t in torrents:
    if not linked(t)[1]:
      continue

    results = [criteria.age(t), criteria.ratio(t)]
    rec = [t.name, t.hash, *results]
    if t.hash in ignored:
      data[1].append(rec)
    else:
      data[0].append(rec)

  return render_template('torrents.html', data=data)

@app.route('/ignore_torrent', methods = ['POST'])
def ignore_torrent():
  hash = request.form['hash']
  ignored = set(json.loads(request.cookies.get('ignored') or '[]'))
  if hash in ignored:
    ignored.remove(hash)
  else:
    ignored.add(hash)
  resp = make_response('')
  resp.set_cookie('ignored', json.dumps(list(ignored)))

  return resp

@app.route('/delete_torrent', methods = ['POST'])
def delete_torrent():
  hash = request.form['hash']
  jwt = app.config['jwt']
  flood.delete(hash, jwt)
  return ''
