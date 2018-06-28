
#!/usr/bin/env bash

base=`pwd`

cd $base/focus/src/sayperm

make clean
make

cp $base/focus/src/sayperm/sayperm $base/bin/
