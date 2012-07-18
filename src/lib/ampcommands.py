from twisted.protocols import amp


class GetNodeInfo(amp.Command):
    arguments = []
    response = [('node_type', amp.Integer()),
                ('node_version', amp.Integer()),
                ('protocol_version', amp.Integer()),
                ('num_lights', amp.Integer())]
