#!/bin/bash

sphinx_fe -argfile ../TrainingSet/acoustic-model/feat.params \
-samprate 16000 -c Astrom-fileids.txt \
-di . -do . -ei wav -eo mfc -mswav yes


../TrainingSet/bw \
 -hmmdir ../TrainingSet/acoustic-model\
 -moddeffn ../TrainingSet/acoustic-model/mdef.txt\
 -ts2cbfn .ptm. \
 -feat 1s_c_d_dd \
 -svspec 0-12/13-25/26-38 \
 -cmn current \
 -agc none \
 -dictfn ../TrainingSet/cmudict-en-us.dict\
 -ctlfn Astrom-fileids.txt \
 -lsnfn Astrom-tag-transcription.txt \
 -accumdir . &> training-result-num2word.txt

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