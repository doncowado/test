GPS Desktop Map (PySide6)
========================

Requirements: Python 3.10+ and internet access for the map tiles and Leaflet files.

Fish shell (CachyOS):
  python -m venv .venv
  source .venv/bin/activate.fish
  python -m pip install PySide6 PySide6-Addons
  python desktop.py

The map displays a sample location. It does not retrieve GPS coordinates
from your laptop or phone. Call gps_tracker.update_location(latitude, longitude)
when you have your own consent-based location source.

These two Python files can also be placed into an existing PySide6 project.
