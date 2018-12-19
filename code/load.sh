#!/bin/bash

while true
do
  echo "New request"
  for i in `seq $((RANDOM%60))`
        do
                curl http://localhost:5050/
        done
  for i in `seq $((RANDOM%60))`
        do
                curl http://localhost:5050/api/trace
        done
  for i in `seq $((RANDOM%60))`
        do
                curl http://localhost:5050/api/apm
        done
  sleep $((RANDOM%15))
done
