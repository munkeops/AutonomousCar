from multiprocessing.connection import Listener

def server(que):
    try:
        while True:
            address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
            listener = Listener(address, authkey=b'secret password')
            conn = listener.accept()
            print('connection accepted from', listener.last_accepted)

            try:
                while True:
                    msg = conn.recv()
                    # do something with msg
                    que.put(msg)
                    # print(msg)
                    if msg == 'close':
                        conn.close()
                        break
            except Exception as e:
                print(e)
            listener.close()
    except Exception as e:
        print(e)