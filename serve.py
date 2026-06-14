#!/usr/bin/env python3
"""Dev server for the Terminal Green SN theme.

Serves ext.json and a ZIP download with a unique dev suffix for cache-busting, allowing local theme
development in Standard Notes.
"""
import argparse
import io
import json
import os
import sys
import urllib.parse
import zipfile
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime


class DevHandler(SimpleHTTPRequestHandler):
  """HTTP handler serving ext.json and download.zip with dev suffixing."""
  def end_headers(self):
    self.send_header(
      'Cache-Control', 'no-cache, no-store, must-revalidate')
    super().end_headers()

  def log_message(self, fmt, *args):
    ts = datetime.now().strftime('%H:%M:%S')
    sys.stderr.write(f'[{ts}] {fmt % args}\n')
    sys.stderr.flush()

  def do_GET(self):
    path = self.path.split('?', 1)[0]
    if path == '/ext.json':
      with open('ext.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
      qs = urllib.parse.parse_qs(
        urllib.parse.urlparse(self.path).query)
      dev_suffix = qs.get('s', [startup_token])[0]
      data['url'] = (
        f'http://localhost:{port}/dist/dist.min.css')
      data['latest_url'] = ''
      data['download_url'] = (
        f'http://localhost:{port}/download.zip?s='
        f'{dev_suffix}')
      data['identifier'] = (
        data['identifier'] + '-dev-' + dev_suffix)
      data['name'] = (
        data['name'] + ' (Dev ' + dev_suffix + ')')
      body = json.dumps(data, indent=2)
      ts = datetime.now().strftime('%H:%M:%S')
      sys.stderr.write(
        f'[{ts}] ext.json: id={data["identifier"]} '
        f'suffix={dev_suffix}\n')
      sys.stderr.flush()
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.send_header('Content-Length', str(len(body.encode())))
      self.end_headers()
      self.wfile.write(body.encode())
    elif path == '/download.zip':
      qs = urllib.parse.parse_qs(
        urllib.parse.urlparse(self.path).query)
      dev_suffix = qs.get('s', [os.urandom(4).hex()])[0]
      with open('dist/dist.min.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
      pkg = {
        'name': 'sn-theme-terminal-green',
        'version': '1.0.8',
        'sn': {
          'main': 'dist/dist.min.css',
          'identifier': (
            'com.netrom.sn-theme-terminal-green-dev-' + dev_suffix),
          'name': (
            'Terminal Green (Dev ' + dev_suffix + ')'),
          'content_type': 'SN|Theme',
          'area': 'themes',
        }
      }
      pkg_body = json.dumps(pkg, indent=2)
      buf = io.BytesIO()
      with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('package.json', pkg_body)
        zf.writestr('dist/dist.min.css', css_content)
      zip_data = buf.getvalue()
      ts = datetime.now().strftime('%H:%M:%S')
      sys.stderr.write(
        f'[{ts}] download.zip: id={pkg["sn"]["identifier"]} '
        f'size={len(zip_data)}\n')
      sys.stderr.flush()
      self.send_response(200)
      self.send_header('Content-Type', 'application/zip')
      self.send_header('Content-Length', str(len(zip_data)))
      self.end_headers()
      self.wfile.write(zip_data)
    else:
      super().do_GET()


def main():
  """Entry point: parse args, print instructions, start the dev server."""
  global port, startup_token
  parser = argparse.ArgumentParser(
    description='Dev server for SN Terminal Green theme')
  parser.add_argument(
    '--port', '-p', type=int, default=8001,
    help='Port to listen on (default: 8001)')
  args = parser.parse_args()
  port = args.port
  startup_token = os.urandom(4).hex()

  print(f'Theme server running at http://localhost:{port}')
  print()
  print('Import in Standard Notes:')
  print('  Preferences > Plugins > Import Custom Plugin')
  print(
    f'  http://localhost:{port}/ext.json?s={startup_token}')
  print()
  print('When done, remove this dev theme and '
        're-import from the jsDelivr URL.')
  print('Press Ctrl+C to stop.')
  print()

  HTTPServer(('0.0.0.0', port), DevHandler).serve_forever()


if __name__ == '__main__':
  main()
