#!/bin/bash
. binaries.sh
raw=$1
base=`basename $raw` \
min=`${X2X} +sf ${raw} | ${MINMAX} | ${X2X} +fa | head -n 1`; \
max=`${X2X} +sf ${raw} | ${MINMAX} | ${X2X} +fa | tail -n 1`; \
echo "Extracting f0 from ${raw}"; \
count=`echo "0.005 * ${SAMPFREQ}" | ${BC} -l`; \
${STEP} -l `printf "%.0f" ${count}` -v 0.0 | \
${X2X} +fs > tmp.head; \
count=`echo "0.025 * ${SAMPFREQ}" | ${BC} -l`; \
${STEP} -l `printf "%.0f" ${count}` -v 0.0 | \
${X2X} +fs > tmp.tail; \
cat tmp.head ${raw} tmp.tail | \
${X2X} +sf > tmp; \
leng=`${X2X} +fa tmp | ${WC} -l`; \
${NRAND} -l ${leng} | ${SOPR} -m ${NOISEMASK} | ${VOPR} -a tmp | \
${X2X} +fs > tmp.raw; \
${TCLSH} getf0.tcl -l -lf0 -H ${UPPERF0} -L ${LOWERF0} -p ${FRAMESHIFT} -r ${SAMPFREQ} tmp.raw | \
${X2X} +af > $2/${base%.*}.lf0;
