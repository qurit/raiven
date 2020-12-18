import dramatiq
import requests

from dramatiq.brokers.stub import StubBroker

# noinspection PyProtectedMember
from api.pipelining._tasks import dramatiq


@dramatiq.actor
def simple_actor(url):
    response = requests.get(url)
    assert len(response.text.split(" "))


# noinspection PyUnusedLocal
def test_broker(stub_broker, stub_worker):
    assert type(stub_broker) is StubBroker


def test_simple_actor(stub_broker, stub_worker):
    simple_actor.send("http://example.com")
    stub_broker.join(simple_actor.queue_name)
    stub_worker.join()
