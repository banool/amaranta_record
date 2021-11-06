#!/bin/bash

rsync --exclude .git --exclude myvenv -avz . pi@ender:~/amaranta_record/
