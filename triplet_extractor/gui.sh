#!/bin/bash
python linux_main_gui.py | py ../qa/input_parser_story_gui.py > story_ui_qa && py story_ui.py

