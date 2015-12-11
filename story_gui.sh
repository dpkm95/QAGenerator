#!/bin/bash
python triplet_extractor/linux_main.py > json_input && echo json_input | py ../qa/input_parser_story_gui.py && py story_gui.py
