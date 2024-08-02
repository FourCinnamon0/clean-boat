import time
import wifi
import thrusters

from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient

thrusters = thrusters.Thrusters()
#deadline = time.ticks_add(time.ticks_ms(), 300)


class TestClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            msg = msg.split("\n")[-2]
            msg = msg.split(" ")

            deadline = time.ticks_add(time.ticks_ms(), 300)

            thrusters.apply_power(int(msg[0]), int(msg[1]))

        except ClientClosedError:
            print("Connection close error")
            self.connection.close()
        except e:
            print("exception:" + str(e) + "\n")
            raise e


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("index.html", 100)

    def _make_client(self, conn):
        return TestClient(conn)


wifi.run()

server = TestServer()
server.start()

while True:
    server.process_all()
    if time.ticks_diff(deadline, time.ticks_ms()) < 0:
        thrusters.apply_power(0, 0, 0, 0)
        deadline = time.ticks_add(time.ticks_ms(), 100000)

server.stop()
