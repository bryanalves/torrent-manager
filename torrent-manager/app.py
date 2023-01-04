from flask import Flask, redirect, make_response, request, render_template

from functools import partial

from . import criteria
from . import torrent
from .floodapi import FloodAPI
from .config import TORRENT_ROOT, TORRENT_DIR, FLOOD_ROOT, FLOOD_USER, FLOOD_PASS

app = Flask(__name__)
flood = FloodAPI(FLOOD_ROOT)

@app.template_filter()
def colorformat(val):
  color = 'text-success' if val[1] == True else 'text-danger'
  return "<span class='%s'>%s</span>" % (color, val[0])

@app.route('/')
def index():
  app.config['jwt'] = flood.login(FLOOD_USER, FLOOD_PASS)
  torrents = torrent.list(TORRENT_ROOT)
  torrents.sort(key=lambda x: x.name.lower())

  linked = partial(criteria.linked, torrent_dir=TORRENT_DIR)

  data = []
  for t in torrents:
    if linked(t)[1] == False:
      continue

    results = [criteria.age(t), criteria.ratio(t)]
    data.append([t.name, t.hash, *results])

  return render_template('torrents.html', data=data)

@app.route('/delete_torrent', methods = ['POST'])
def delete_torrent():
  hash = request.form['hash']
  jwt = app.config['jwt']
  flood.delete(hash, jwt)
  return ''
