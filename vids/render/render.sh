#!/bin/bash
# usage: render.sh ep24 outname
EP=$1; OUTN=$2; cd /home/claude/eps; mkdir -p $EP
N=$(python3 $EP.py nparts 2>/dev/null | tail -1)
rm -f $EP/part*.mp4
( for i in $(seq 0 2 $((N-1))); do python3 $EP.py part $i 2>>$EP/w1.log; done ) &
( for i in $(seq 1 2 $((N-1))); do python3 $EP.py part $i 2>>$EP/w2.log; done ) &
wait
python3 $EP.py audio >/dev/null 2>>$EP/audio.log
: > $EP/list.txt; for i in $(seq 0 $((N-1))); do echo "file 'part$i.mp4'" >> $EP/list.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i $EP/list.txt -c copy $EP/joined.mp4 && \
ffmpeg -y -loglevel error -i $EP/joined.mp4 -i $EP/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $EP/full.mp4 && \
ffmpeg -y -loglevel error -i $EP/full.mp4 -c:v libx264 -crf 23 -preset veryfast -maxrate 14M -bufsize 28M -pix_fmt yuv420p -c:a copy -movflags +faststart /home/claude/eps/$OUTN.mp4 && echo "DONE $OUTN" > $EP/done.txt
