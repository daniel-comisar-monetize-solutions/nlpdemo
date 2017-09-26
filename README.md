# NLP Demo

The purpose of this project is to analyze pdf manuals and help users navigate the contents. This is just a demo with one page and a sqlite3 database baked in.

To build the app, use Docker:

    docker build -t nlpdemo .
    docker run -d -p 80:80 nlpdemo
    xdg-open http://localhost
