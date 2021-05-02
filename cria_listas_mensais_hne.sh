#!/bin/bash

# MONTHS = (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)
MONTHS=(1 2 3 4 5 6 7 8 9 10 11 12)

YEARS=(2016 2017)

# echo $YEARS
# echo $MONTHS

for y in $(seq -w 2016 1 2017)
do
    echo $y
    for m in $(seq -w 1 1 12)
    do
        echo $m
        find /home/hp/Documents/dados/pnboia/ -type f -name "${y}${m}*.HNE" > /home/hp/Documents/salinopolis/listas/lista_hne_fortaleza_${y}${m}.txt
    done
done
