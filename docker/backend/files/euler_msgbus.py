from copr_backend.helpers import BackendConfigReader
from kafka import KafkaProducer
import os
import datetime
import uuid
import json


def message_from_worker_job(topic, job, who, ip, pid):
    message = {}
    content = {
        'user': job.submitter,
        'copr': job.project_name,
        'owner': job.project_owner,
        'pkg': job.package_name,
        'build': job.build_id,
        'chroot': job.chroot,
        'version': job.package_version,
        'status': job.status,
    }
    content.update({'ip': ip, 'who': who, 'pid': pid})

    message_types = {
        'build.start': {
            'what': "build start: user:{user} copr:{copr}" \
                    " pkg:{pkg} build:{build} ip:{ip} pid:{pid}",
        },
        'build.end': {
            'what': "build end: user:{user} copr:{copr} build:{build}" \
                    " pkg:{pkg} version:{version} ip:{ip} pid:{pid} status:{status}",
        },
    }
    content['what'] = message_types[topic]['what'].format(**content)
    message['body'] = content
    now = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc)
    headers = {
        "fedora_messaging_schema": topic,
        "sent-at": now.isoformat(),
    }
    message['headers'] = headers
    message['id'] = str(uuid.uuid4())
    message['topic'] = topic
    return message


class EulerMessageSender:
    def __init__(self, name, log):
        self.log = log
        self.name = name
        self.pid = os.getpid()

    def announce(self, topic, job, host):
        msg = message_from_worker_job(topic, job, self.name, host, self.pid)
        self.send_message(msg)

    def send_message(self, msg):
        """ Send message to kafka """
        config_file = os.environ.get("EULER_MESSAGE_CONFIG", "/etc/copr/msgbus-euler.conf")
        opts = BackendConfigReader(config_file).read()
        producer = KafkaProducer(
            bootstrap_servers=opts.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        producer.send("test_message_center", msg.__str__().encode("utf-8"))
        producer.flush()
