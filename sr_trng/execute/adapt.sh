#!/bin/sh
echo $@
echo "the model path is" $1
echo "the PKG_DIR is" $2

sphinx_fe -argfile $2/acoustic-model/feat.params \
-samprate 16000 -c $1/fileid.txt \
-di $1 -do $3 -ei wav -eo mfc -mswav yes

echo "BW"

$2/bw \
 -hmmdir $2/acoustic-model\
 -moddeffn $2/acoustic-model/mdef.txt\
 -ts2cbfn .ptm. \
 -feat 1s_c_d_dd \
 -svspec 0-12/13-25/26-38 \
 -cmn current \
 -agc none \
 -dictfn $2/cmudict-en-us.dict\
 -cepdir $3\
 -ctlfn $1/fileid.txt \
 -lsnfn $1/tag-trans.txt \
 -accumdir $3 &> $3/training-result.txt

cp -a $2/acoustic-model $4
echo "MAP ADAPT"

$2/map_adapt \
    -moddeffn $2/acoustic-model/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn $2/acoustic-model/means \
    -varfn $2/acoustic-model/variances \
    -mixwfn $2/acoustic-model/mixture_weights \
    -tmatfn $2/acoustic-model/transition_matrices \
    -accumdir $3 \
    -mapmeanfn $4/means \
    -mapvarfn $4/variances \
    -mapmixwfn $4/mixture_weights \
    -maptmatfn $4/transition_matrices