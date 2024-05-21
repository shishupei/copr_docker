import json
from fedora_messaging import message


class _CoprMessage(message.Message):
    def __init__(self, *args, **kwargs):
        if 'body' in kwargs:
            body = kwargs.pop('body')
            if 'msg' in body:
                body = body['msg']
            kwargs['body'] = body

        super(_CoprMessage, self).__init__(*args, **kwargs)


class BuildChrootStartedV1(_CoprMessage):
    topic = 'copr.build.start'


class BuildChrootStartedV1DontUse(_CoprMessage):
    topic = 'copr.build.start'


class BuildChrootEndedV1(_CoprMessage):
    topic = 'copr.build.end'
