#!/bin/bash

rsync --exclude .git myvenv -avz . pi@ender:~/amaranta_record/
