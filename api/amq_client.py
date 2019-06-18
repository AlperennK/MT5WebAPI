#Do not modify this

class MyListener(object):
    msg_list = []
    hdr_list = []

    def __init__(self, connection):
        self.msg_list = []
        self.connection = "connection"

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, headers, message):
        self.hdr_list.append(headers)
        self.msg_list.append(message)

