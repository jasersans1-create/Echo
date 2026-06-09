#!/bin/bash

cd /home/chirayu/Jarvis-2.0 || exit 1

source venv/bin/activate

nohup python3 hotkey.py > jarvis.log 2>&1 &
