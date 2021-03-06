############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.7.5
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
from unittest import mock
import time
import pytest

# external packages

# local import
from mw4.powerswitch.kmRelay import KMRelay


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    global app
    app = KMRelay()
    yield
    del app


def test_host_0():
    app.host = None
    assert app.host is None


def test_host_1():
    app.host = 1.1
    assert app.host is None


def test_host_2():
    app.host = ('localhost', 80)
    assert app.host == ('localhost', 80)


def test_user():
    app.user = 'astro'
    assert app.user == 'astro'


def test_password():
    app.password = 'astro'
    assert app.password == 'astro'


def test_startTimers_1():
    app.host = None
    suc = app.startCommunication()
    assert not suc


def test_startTimers_2():
    app.host = ('localhost', 80)
    suc = app.startCommunication()
    assert suc


def test_startTimers_3():
    app.host = ('localhost', 80)
    with mock.patch.object(app.timerTask,
                           'start',):
        suc = app.startCommunication()
        assert suc


def test_stopTimers_1():
    with mock.patch.object(app.timerTask,
                           'stop',):
        suc = app.stopCommunication()
        assert suc


def test_debugOutput_1():
    suc = app.debugOutput()
    assert not suc


def test_debugOutput_2():
    class Test:
        reason = 'reason'
        status_code = 200
        elapsed = 1
        text = 'test'
        url = 'test'

    suc = app.debugOutput(Test())
    assert suc


def getRelay_1():
    app.host = None
    suc = app.getRelay()
    assert suc is None


def getRelay_2():
    app.host = host
    app.mutexPoll.lock()
    suc = app.relay.getRelay()
    assert suc is None


def getRelay_3():
    app.host = host
    app.mutexPoll.unlock()
    suc = app.relay.getRelay()
    assert not suc


def test_cyclePolling_1():
    app.host = None
    app.user = 'test'
    app.password = 'test'
    suc = app.cyclePolling()
    assert not suc


def test_cyclePolling_2():
    app.host = ('localhost', 80)
    app.user = 'test'
    app.password = 'test'
    suc = app.cyclePolling()
    assert not suc


def test_cyclePolling_3():
    class Test:
        reason = 'OK'
        text = 'test'

    app.user = 'test'
    app.password = 'test'
    app.host = ('localhost', 80)
    with mock.patch.object(app,
                           'getRelay',
                           return_value=Test()):
        suc = app.cyclePolling()
        assert suc


def test_status1(qtbot):
    returnValue = """<response>
                     <relay0>0</relay0>
                     <relay1>0</relay1>
                     <relay2>0</relay2>
                     <relay3>0</relay3>
                     <relay4>0</relay4>
                     <relay5>0</relay5>
                     <relay6>0</relay6>
                     <relay7>0</relay7>
                     <relay8>0</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 8):
            app.set(i, 0)

        with qtbot.waitSignal(app.statusReady):
            app.cyclePolling()
        assert [0, 0, 0, 0, 0, 0, 0, 0] == app.status


def test_status2(qtbot):
    returnValue = """<response>
                     <relay0>1</relay0>
                     <relay1>1</relay1>
                     <relay2>1</relay2>
                     <relay3>1</relay3>
                     <relay4>1</relay4>
                     <relay5>1</relay5>
                     <relay6>1</relay6>
                     <relay7>1</relay7>
                     <relay8>1</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 8):
            app.set(i, 1)

        with qtbot.waitSignal(app.statusReady):
            app.cyclePolling()
        assert [1, 1, 1, 1, 1, 1, 1, 1] == app.status


def test_status3(qtbot):
    returnValue = """<response>
                     <relay0>1</relay0>
                     <relay1>1</relay1>
                     <relay2>1</relay2>
                     <relay3>1</relay3>
                     <relay4>1</relay4>
                     <relay5>1</relay5>
                     <relay6>1</relay6>
                     <relay7>1</relay7>
                     <relay8>1</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 8):
            app.switch(i)

        with qtbot.waitSignal(app.statusReady):
            app.cyclePolling()
        assert [1, 1, 1, 1, 1, 1, 1, 1] == app.status


def test_status4(qtbot):
    returnValue = """<response>
                     <relay0>0</relay0>
                     <relay1>0</relay1>
                     <relay2>0</relay2>
                     <relay3>0</relay3>
                     <relay4>0</relay4>
                     <relay5>0</relay5>
                     <relay6>0</relay6>
                     <relay7>0</relay7>
                     <relay8>0</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        with mock.patch.object(time,
                               'sleep'):
            for i in range(0, 8):
                app.pulse(i)

            with qtbot.waitSignal(app.statusReady):
                app.cyclePolling()
            assert [0, 0, 0, 0, 0, 0, 0, 0] == app.status


def test_getRelay_1(qtbot):
    app.mutexPoll.lock()
    suc = app.getRelay()
    app.mutexPoll.unlock()
    assert not suc


def test_cyclePolling_1():
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.cyclePolling()
        assert not suc


def test_getByte_1():
    relay = 7
    state = True
    app.status = [False] * 8

    value = app.getByte(relayNumber=relay, state=state)
    assert value == 0x80


def test_getByte_2():
    relay = 7
    state = False
    app.status = [True] * 8

    value = app.getByte(relayNumber=relay, state=state)
    assert value == 0x7F


def test_pulse_1(qtbot):
    ret = None

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.pulse(7)
        assert not suc


def test_pulse_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.pulse(7)
        assert not suc


def test_pulse_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.pulse(7)
        assert suc


def test_switch_1(qtbot):
    ret = None

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.switch(7)
        assert not suc


def test_switch_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.switch(7)
        assert not suc


def test_switch_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.switch(7)
        assert suc


def test_set_1(qtbot):
    ret = None

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.set(7, True)
        assert not suc


def test_set_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.set(7, True)
        assert not suc


def test_set_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app,
                           'getRelay',
                           return_value=ret):
        suc = app.set(7, False)
        assert suc
