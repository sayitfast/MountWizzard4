#!/bin/bash
PATH=/Library/Frameworks/Python.framework/Versions/3.7/bin:$PATH
rm -rf venv
virtualenv venv -p python3.7
source venv/bin/activate
pip install PyQt5==5.12.2
pip install astropy==3.1.2
pip install matplotlib==3.1.1
pip install wakeonlan==1.1.6
pip install requests==2.22.0
pip install requests-toolbelt==0.9.1
pip install skyfield==1.10
