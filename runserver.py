""" 
creates an application instance and runs the dev server
"""

from libraryapi.application import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
