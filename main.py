from app import app, socketio

def test():
    return 'ok'

if __name__ == "__main__":
    socketio.run(app)

    
    
