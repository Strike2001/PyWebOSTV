from threading import Event

from pytest import raises

from pywebostv.controls import WebOSControlBase
from pywebostv.controls import arguments, process_payload
from pywebostv.controls import MediaControl

from utils import FakeClient


class TestArgumentExtraction(object):
    def test_bad_argument_param(self):
        with raises(ValueError):
            arguments(None)

        with raises(ValueError):
            arguments({})

    def test_extract_positional_args(self):
        args = arguments(1)
        assert args([1], {2: 3}, "blah") == {2: 3}

        with raises(TypeError):
            assert args()

    def test_extract_keyword_args(self):
        args = arguments("arg")
        assert args(arg=1) == 1

        with raises(TypeError):
            assert args()

    def test_args_default_value(self):
        args = arguments(2, default={1, 2})
        assert args() == {1, 2}
        assert args("a", "b", "c") == "c"

    def test_kwargs_default_value(self):
        args = arguments("key", default="value")
        assert args() == "value"
        assert args("a", "b", key="blah") == "blah"

    def test_postprocess(self):
        args = arguments(2, postprocess=lambda x: 1, default={1, 2})
        assert args() == {1, 2}
        assert args("a", "b", "c") == 1


class TestProcessPayload(object):
    def test_process_payload(self):
        payload = {
            "level1": {
                "level2": [1, 3],
                "level2a": lambda *a, **b: "{}{}".format(len(a), len(b))
            },
            "level1a": {1, 2}
        }
        expected = {
            "level1": {
                "level2": [1, 3],
                "level2a": "22"
            },
            "level1a": {1, 2}
        }
        assert process_payload(payload, 1, 2, a=4, b=5) == expected

    def test_just_callable_arg(self):
        assert process_payload(lambda x: x**2, 2) == 4


class TestWebOSControlBase(object):
    def test_exec_command_blocking(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "test": {"uri": "/test"}
        }

        client.setup_response("/test", {"resp": True})
        assert control_base.test() == {"resp": True}

    def test_exec_command_callback(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "test": {"uri": "/test"}
        }

        response = []
        event = Event()

        def callback(status, resp):
            response.append((status, resp))
            event.set()

        client.setup_response("/test", {"resp": True})
        control_base.test(callback=callback)
        event.wait()

        assert response == [(True, {"resp": True})]

    def test_exec_command_failed_callback(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "test": {
                "uri": "/test",
                "validation": lambda *args: False,
                "validation_error": "Error"
            }
        }

        response = []
        event = Event()

        def callback(status, resp):
            response.append((status, resp))
            event.set()

        client.setup_response("/test", {"resp": True})
        control_base.test(callback=callback)
        event.wait()

        assert response == [(False, "Error")]

    def test_exec_command_failed_blocking(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "test": {
                "uri": "/test",
                "validation": lambda *args: False,
                "validation_error": "Error"
            },
        }

        client.setup_response("/test", {"resp": True})
        with raises(ValueError):
            control_base.test(block=True)

    def test_exec_timeout(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "test": {
                "uri": "/test",
            },
        }

        client.setup_response("/another-uri", {"resp": True})
        with raises(Exception):
            control_base.test(timeout=1)


class TestMediaControl(object):
    def test_volume_up(self):
        client = FakeClient()
        media = MediaControl(client)
        media.volume_up()

        client.assert_sent_message_without_id({
            "type": "request",
            "uri": "ssap://audio/volumeUp"
        })

    def test_volume_down(self):
        client = FakeClient()
        media = MediaControl(client)
        media.volume_down()

        client.assert_sent_message_without_id({
            "type": "request",
            "uri": "ssap://audio/volumeDown"
        })

    def test_mute(self):
        client = FakeClient()
        media = MediaControl(client)
        media.mute(True, block=False)

        client.assert_sent_message_without_id({
            "type": "request",
            "uri": "ssap://audio/setMute",
            "payload": {"mute": True}
        })

    def test_unmute(self):
        client = FakeClient()
        media = MediaControl(client)
        media.mute(False, block=False)

        client.assert_sent_message_without_id({
            "type": "request",
            "uri": "ssap://audio/setMute",
            "payload": {"mute": False}
        })

    def set_volume(self):
        client = FakeClient()
        media = MediaControl(client)
        media.set_volume(30)

        client.assert_sent_message_without_id({
            "type": "request",
            "uri": "ssap://audio/setVolume",
            "payload": {"volume": 30}
        })
