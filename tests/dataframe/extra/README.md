
This directory contains the script used to generate three input data frame files in the directory one above.

The script can be ran, for example, with the following arguments:

```
./createInputFiles.py -p 5 -i /afs/cern.ch/work/s/sakuma/public/cms/c150130_RA1_data/80X/MC/20160811_B01/ROC_MC_SM -o ./
```

The command will create three files: `tbl_component_met.txt`, `tbl_nevt.txt`, `tbl_xsec.txt`.

This directory also contains a data frame file `tbl_process.txt`. This file was not generated. It was written by hand.
