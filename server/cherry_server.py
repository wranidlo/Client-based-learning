import cherrypy
from server.api_server import app


def main():
    cherrypy.tree.graft(app, "/")

    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "127.0.0.1"
    server.socket_port = 8000
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    main()
