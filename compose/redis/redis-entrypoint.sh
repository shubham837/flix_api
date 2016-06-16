#!/bin/sh
set -e

awk -F, 'NR > 0{ print "SET", "\"gr_auth_key:"$1"\"", "'"'"'"$3"'"'"'" }' /tmp/Auth.csv | redis-cli -h redis
awk -F, 'NR > 0{ print "SET", "\"gr_acc_tok:"$2"\"",  "'"'"'"$4"'"'"'" }' /tmp/Auth.csv | redis-cli -h redis

echo "Successfully Set Default Auth Keys"
