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
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
from invoke import task, context, Collection


def runMW(c, param):
    # c.run(param, echo=False, hide='out')
    c.run(param)


def printMW(param):
    print('\n\033[95m\033[1m' + param + '\033[0m')


@task
def build_resource(c):
    printMW('building resources')
    # runMW(c, 'cp ./data/deltat.data ./mw4/resource/deltat.data')
    # runMW(c, 'cp ./data/deltat.preds ./mw4/resource/deltat.preds')
    # runMW(c, 'cp ./data/Leap_Second.dat ./mw4/resource/Leap_Second.dat')
    resourceDir = './mw4/resource/'
    runMW(c, f'pyrcc5 -o {resourceDir}resources.py {resourceDir}resources.qrc')


@task
def build_widgets(c):
    printMW('building widgets')
    widgetDir = './mw4/gui/widgets/'
    widgets = ['hemisphere', 'image', 'main', 'measure', 'message',
               'satellite', 'keypad', 'devicePopup']
    for widget in widgets:
        name = widgetDir + widget
        runMW(c, f'python -m PyQt5.uic.pyuic -x {name}.ui -o {name}_ui.py')


@task()
def test_mc(c):
    printMW('testing mountcontrol')
    with c.cd('../mountcontrol'):
        runMW(c, 'flake8')
        runMW(c, 'pytest mountcontrol/test/* --cov-config tox.ini --cov mountcontrol/')


@task()
def test_ib(c):
    printMW('testing indibase')
    with c.cd('../indibase'):
        runMW(c, 'flake8')
        runMW(c, 'pytest indibase/test/test_units --cov-config .coveragerc --cov mw4/')


@task()
def test_mw(c):
    printMW('testing mountwizzard')
    with c.cd('.'):
        runMW(c, 'flake8')
        runMW(c, 'pytest mw4/test/* --cov-config .coveragerc --cov mw4/')


@task(pre=[])
def build_mc(c):
    printMW('building dist mountcontrol')
    with c.cd('../mountcontrol'):
        runMW(c, 'rm -f dist/*.tar.gz')
        runMW(c, 'python setup.py sdist')
        runMW(c, 'cp dist/mountcontrol*.tar.gz ../MountWizzard4/dist/mountcontrol.tar.gz')


@task(pre=[])
def build_ib(c):
    printMW('building dist indibase')
    with c.cd('../indibase'):
        runMW(c, 'rm -f dist/*.tar.gz')
        runMW(c, 'python setup.py sdist')
        runMW(c, 'cp dist/indibase*.tar.gz ../MountWizzard4/dist/indibase.tar.gz')


@task(pre=[build_resource, build_widgets, build_mc, build_ib])
def build_mw(c):
    printMW('building dist mountwizzard4')
    with c.cd('.'):
        runMW(c, 'rm -f dist/mountwizzard4*.tar.gz')
        runMW(c, 'python setup.py sdist')
        runMW(c, 'cp dist/mountwizzard4*.tar.gz ../MountWizzard4/dist/mountwizzard4.tar.gz')


@task(pre=[])
def upload_mc(c):
    printMW('uploading dist mountcontrol')
    with c.cd('../mountcontrol/dist'):
        runMW(c, 'twine upload mountcontrol-*.tar.gz -r pypi')


@task(pre=[])
def upload_ib(c):
    printMW('uploading dist indibase')
    with c.cd('../indibase/dist'):
        runMW(c, 'twine upload indibase-*.tar.gz -r pypi')


@task(pre=[])
def upload_mw(c):
    printMW('uploading dist mountwizzard4')
    with c.cd('./dist'):
        runMW(c, 'twine upload mountwizzard4-*.tar.gz -r pypi')


@task(pre=[upload_mc, upload_ib, upload_mw])
def upload_all(c):
    printMW('uploading dist complete')


@task(pre=[build_resource, build_widgets, build_mc, build_ib])
def install_all(c):
    printMW('installing in work dir')
    with c.cd('./dist'):
        runMW(c, 'pip install indibase.tar.gz')
        runMW(c, 'pip install mountcontrol.tar.gz')
