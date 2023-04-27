#!/bin/bash
# reqs files need to end with a terminating /n. Complain to POSIX.
inputfile=reqs.txt

sed -i 's/\r$//' "$inputfile"

while read -r package; do
  version=$(pip show "$package" | grep Version | awk '{print $2}')
  echo "$package==$version" >> requirements.txt
done < "$inputfile"
