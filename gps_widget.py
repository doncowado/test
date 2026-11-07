"""Reusable Leaflet map widget for a PySide6 desktop application.

This displays coordinates supplied by Python; it does not acquire GPS itself.
"""
import json

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView


MAP_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    html, body, #map { width: 100%; height: 100%; margin: 0; }
    body { background: #e2e8f0; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const map = L.map('map').setView([12.8797, 121.7740], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);
    let marker = null;
    window.updateLocation = (lat, lon) => {
      const coords = [lat, lon];
      if (marker === null) {
        marker = L.marker(coords).addTo(map);
      } else {
        marker.setLatLng(coords);
      }
      map.setView(coords, 16);
    };
  </script>
</body>
</html>"""


class GPSWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.map_view = QWebEngineView(self)
        layout.addWidget(self.map_view)

        self._ready = False
        self._pending_location = None
        # Connect before loading so the signal can't be missed.
        self.map_view.loadFinished.connect(self._on_loaded)
        self.map_view.setHtml(MAP_HTML, QUrl('https://example.com/'))

    def _on_loaded(self, ok):
        self._ready = bool(ok)
        if self._ready and self._pending_location is not None:
            latitude, longitude = self._pending_location
            self._send_location(latitude, longitude)

    def _send_location(self, latitude, longitude):
        # JSON encodes numeric values safely for JavaScript.
        js = 'window.updateLocation({}, {});'.format(
            json.dumps(latitude), json.dumps(longitude)
        )
        self.map_view.page().runJavaScript(js)

    def update_location(self, latitude, longitude):
        """Show supplied coordinates after the web page finishes loading."""
        latitude, longitude = float(latitude), float(longitude)
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError('Invalid latitude or longitude')
        self._pending_location = (latitude, longitude)
        if self._ready:
            self._send_location(latitude, longitude)
