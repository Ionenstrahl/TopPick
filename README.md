# TopPick
This is gonna be an awesome App, which
- scrapes current data from 17lands.com
- saves the relevant data in a cloud db
- displays images of top draft commons, sorted by color

# Local ausführen
- main.py ausführen

# Auf Strato veröffentlichen
- Docker image bauen: ```docker build -t my-python-app .```
- image local prüfen: ```docker run -p 5000:5000 my-python-app```
- auf V-Server einloggen: ```ssh root@85.215.134.190```