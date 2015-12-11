#!/bin/bash
python linux_main.py > json_input && echo json_input | py ../qa/input_parser.py
