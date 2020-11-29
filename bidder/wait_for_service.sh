#!/bin/bash

# Made to wait from kafka and make sure fault is already ran
set -e

cmd="$@"

until nc -vz kafka 9092; do
  >&2 echo "Waiting for Kafka to be ready... - sleeping"
  sleep 2
done

sleep 10

faust -A streamer.event_stream worker -l info
