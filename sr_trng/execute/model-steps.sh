#!/bin/bash

sphinx_fe -argfile $2/acoustic-model/feat.params \
-samprate 16000 -c $1/fileid.txt \
-di $1 -do $3 -ei wav -eo mfc -mswav yes


../TrainingSet/bw \
 -hmmdir $2/acoustic-model\
 -moddeffn $2/acoustic-model/mdef.txt\
 -ts2cbfn .ptm. \
 -feat 1s_c_d_dd \
 -svspec 0-12/13-25/26-38 \
 -cmn current \
 -agc none \
 -dictfn $2/cmudict-en-us.dict\
 -ctlfn $1/fileids.txt \
 -lsnfn $1/tag-trans.txt \
 -accumdir $1 &> $1/training-result.txt

cp -a ../TrainingSet/acoustic-model Astrom_model_num2word

../TrainingSet/map_adapt \
    -moddeffn ../TrainingSet/acoustic-model/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn ../TrainingSet/acoustic-model/means \
    -varfn ../TrainingSet/acoustic-model/variances \
    -mixwfn ../TrainingSet/acoustic-model/mixture_weights \
    -tmatfn ../TrainingSet/acoustic-model/transition_matrices \
    -accumdir . \
    -mapmeanfn Astrom_model_num2word/means \
    -mapvarfn Astrom_model_num2word/variances \
    -mapmixwfn Astrom_model_num2word/mixture_weights \
    -maptmatfn Astrom_model_num2word/transition_matrices