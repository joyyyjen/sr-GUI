#!/bin/bash

sphinx_fe -argfile ../TrainingSet/acoustic-model/feat.params \
-samprate 16000 -c ted-Astrom.fileids \
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
 -ctlfn ted-Astrom.fileids \
 -lsnfn ted-Astrom.transcription \
 -accumdir .

cp -a ../TrainingSet/acoustic-model model2-update-dict

../TrainingSet/map_adapt \
    -moddeffn ../TrainingSet/acoustic-model/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn ../TrainingSet/acoustic-model/means \
    -varfn ../TrainingSet/acoustic-model/variances \
    -mixwfn ../TrainingSet/acoustic-model/mixture_weights \
    -tmatfn ../TrainingSet/acoustic-model/transition_matrices \
    -accumdir . \
    -mapmeanfn model2-update-dict/means \
    -mapvarfn model2-update-dict/variances \
    -mapmixwfn model2-update-dict/mixture_weights \
    -maptmatfn model2-update-dict/transition_matrices

