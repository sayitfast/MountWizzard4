#!/bin/bash
PATH=/Library/Frameworks/Python.framework/Versions/3.7/bin:$PATH
source venv/bin/activate
cd mountwizzard4
pip install mc.tar.gz
pip install ib.tar.gz
pip install mw4.tar.gz
decativate
