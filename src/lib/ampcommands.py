from twisted.protocols import amp


class GetNodeInfo(amp.Command):
    arguments = []
    response = [('node_type', amp.String()),
                ('node_version', amp.Integer()),
                ('protocol_version', amp.Integer()),
                ('num_pixels', amp.Integer())]


class SetAll(amp.Command):
    arguments = [('values', amp.ListOf(amp.ListOf(amp.Integer())))]
    response = [('status', amp.Integer())]
