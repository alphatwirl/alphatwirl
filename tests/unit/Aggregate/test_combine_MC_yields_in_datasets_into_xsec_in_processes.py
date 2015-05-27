import unittest
import cStringIO

##____________________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    from AlphaTwirl.Aggregate import combine_MC_yields_in_datasets_into_xsec_in_processes
    hasPandas = True
except ImportError:
    class PD:
        def read_table(self, *args, **kargs): pass
    pd = PD()

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1),
                              check_less_precise = True, check_names = True)

##____________________________________________________________________________||
tbl_component_met = pd.read_table(cStringIO.StringIO(
"""component         met     n  nvar
      QCD_HT_1000ToInf  15.8489319246     1     1
      QCD_HT_1000ToInf  19.9526231497     0     0
      QCD_HT_1000ToInf  25.1188643151     1     1
      QCD_HT_1000ToInf  31.6227766017     3     3
      QCD_HT_1000ToInf  39.8107170553     2     2
      QCD_HT_1000ToInf  50.1187233627     5     5
      QCD_HT_1000ToInf   63.095734448     2     2
      QCD_HT_1000ToInf  79.4328234724     2     2
      QCD_HT_1000ToInf            100     3     3
      QCD_HT_1000ToInf  125.892541179     2     2
      QCD_HT_1000ToInf  158.489319246     0     0
 QCD_HT_1000ToInf_ext1  39.8107170553     1     1
 QCD_HT_1000ToInf_ext1  50.1187233627     1     1
 QCD_HT_1000ToInf_ext1   63.095734448     0     0
 QCD_HT_1000ToInf_ext1            100     1     1
 QCD_HT_1000ToInf_ext1  125.892541179     0     0
       QCD_HT_250To500  31.6227766017     1     1
       QCD_HT_250To500  39.8107170553     0     0
       QCD_HT_250To500  50.1187233627     1     1
       QCD_HT_250To500   63.095734448     0     0
       QCD_HT_250To500  79.4328234724     1     1
       QCD_HT_250To500            100     0     0
  QCD_HT_250To500_ext1  25.1188643151     1     1
  QCD_HT_250To500_ext1  31.6227766017     0     0
      QCD_HT_500To1000  15.8489319246     2     2
      QCD_HT_500To1000  19.9526231497     8     8
      QCD_HT_500To1000  25.1188643151     2     2
      QCD_HT_500To1000  31.6227766017     2     2
      QCD_HT_500To1000  39.8107170553     4     4
      QCD_HT_500To1000  50.1187233627     5     5
      QCD_HT_500To1000   63.095734448     7     7
      QCD_HT_500To1000  79.4328234724     1     1
      QCD_HT_500To1000            100     1     1
      QCD_HT_500To1000  125.892541179     1     1
      QCD_HT_500To1000  158.489319246     0     0
 QCD_HT_500To1000_ext1  39.8107170553     1     1
 QCD_HT_500To1000_ext1  50.1187233627     2     2
 QCD_HT_500To1000_ext1   63.095734448     1     1
 QCD_HT_500To1000_ext1  79.4328234724     1     1
 QCD_HT_500To1000_ext1            100     1     1
 QCD_HT_500To1000_ext1  125.892541179     1     1
 QCD_HT_500To1000_ext1  158.489319246     1     1
 QCD_HT_500To1000_ext1  199.526231497     0     0
     TBarToLeptons_sch  3.16227766017     1     1
     TBarToLeptons_sch  3.98107170553     1     1
     TBarToLeptons_sch  5.01187233627     3     3
     TBarToLeptons_sch   6.3095734448     8     8
     TBarToLeptons_sch  7.94328234724    16    16
     TBarToLeptons_sch             10    39    39
     TBarToLeptons_sch  12.5892541179    52    52
     TBarToLeptons_sch  15.8489319246    80    80
     TBarToLeptons_sch  19.9526231497   144   144
     TBarToLeptons_sch  25.1188643151   178   178
     TBarToLeptons_sch  31.6227766017   265   265
     TBarToLeptons_sch  39.8107170553   359   359
     TBarToLeptons_sch  50.1187233627   482   482
     TBarToLeptons_sch   63.095734448   489   489
     TBarToLeptons_sch  79.4328234724   405   405
     TBarToLeptons_sch            100   306   306
     TBarToLeptons_sch  125.892541179   174   174
     TBarToLeptons_sch  158.489319246   107   107
     TBarToLeptons_sch  199.526231497    53    53
     TBarToLeptons_sch  251.188643151    27    27
     TBarToLeptons_sch  316.227766017    13    13
     TBarToLeptons_sch  398.107170553     3     3
     TBarToLeptons_sch  501.187233627     2     2
     TBarToLeptons_sch   630.95734448     0     0
     TBarToLeptons_tch  2.51188643151     1     1
     TBarToLeptons_tch  3.16227766017     6     6
     TBarToLeptons_tch  3.98107170553    16    16
     TBarToLeptons_tch  5.01187233627    36    36
     TBarToLeptons_tch   6.3095734448    52    52
     TBarToLeptons_tch  7.94328234724   112   112
     TBarToLeptons_tch             10   187   187
     TBarToLeptons_tch  12.5892541179   328   328
     TBarToLeptons_tch  15.8489319246   549   549
     TBarToLeptons_tch  19.9526231497   807   807
     TBarToLeptons_tch  25.1188643151  1170  1170
     TBarToLeptons_tch  31.6227766017  1740  1740
     TBarToLeptons_tch  39.8107170553  2279  2279
     TBarToLeptons_tch  50.1187233627  2955  2955
     TBarToLeptons_tch   63.095734448  3464  3464
     TBarToLeptons_tch  79.4328234724  3125  3125
     TBarToLeptons_tch            100  2238  2238
     TBarToLeptons_tch  125.892541179  1569  1569
     TBarToLeptons_tch  158.489319246   901   901
     TBarToLeptons_tch  199.526231497   378   378
     TBarToLeptons_tch  251.188643151   156   156
     TBarToLeptons_tch  316.227766017    48    48
     TBarToLeptons_tch  398.107170553    18    18
     TBarToLeptons_tch  501.187233627     2     2
     TBarToLeptons_tch   630.95734448     0     0
             TBar_tWch  1.58489319246     1     1
             TBar_tWch  1.99526231497     2     2
             TBar_tWch  2.51188643151     3     3
             TBar_tWch  3.16227766017     2     2
             TBar_tWch  3.98107170553     9     9
             TBar_tWch  5.01187233627    27    27
             TBar_tWch   6.3095734448    34    34
             TBar_tWch  7.94328234724    78    78
             TBar_tWch             10   114   114
             TBar_tWch  12.5892541179   175   175
             TBar_tWch  15.8489319246   320   320
             TBar_tWch  19.9526231497   414   414
             TBar_tWch  25.1188643151   568   568
             TBar_tWch  31.6227766017   778   778
             TBar_tWch  39.8107170553  1055  1055
             TBar_tWch  50.1187233627  1344  1344
             TBar_tWch   63.095734448  1543  1543
             TBar_tWch  79.4328234724  1509  1509
             TBar_tWch            100  1421  1421
             TBar_tWch  125.892541179  1109  1109
             TBar_tWch  158.489319246   755   755
             TBar_tWch  199.526231497   399   399
             TBar_tWch  251.188643151   211   211
             TBar_tWch  316.227766017    95    95
             TBar_tWch  398.107170553    39    39
             TBar_tWch  501.187233627    21    21
             TBar_tWch   630.95734448     3     3
             TBar_tWch  794.328234724     0     0
                TTJets  1.25892541179     4     4
                TTJets  1.58489319246     6     6
                TTJets  1.99526231497    36    36
                TTJets  2.51188643151    61    61
                TTJets  3.16227766017   177   177
                TTJets  3.98107170553   343   343
                TTJets  5.01187233627   682   682
                TTJets   6.3095734448  1367  1367
                TTJets  7.94328234724  2351  2351
                TTJets             10  3987  3987
                TTJets  12.5892541179  6602  6602
                TTJets  15.8489319246 10540 10540
                TTJets  19.9526231497 16104 16104
                TTJets  25.1188643151 23881 23881
                TTJets  31.6227766017 32863 32863
                TTJets  39.8107170553 44104 44104
                TTJets  50.1187233627 56309 56309
                TTJets   63.095734448 64563 64563
                TTJets  79.4328234724 62857 62857
                TTJets            100 51717 51717
                TTJets  125.892541179 36876 36876
                TTJets  158.489319246 22650 22650
                TTJets  199.526231497 10926 10926
                TTJets  251.188643151  4305  4305
                TTJets  316.227766017  1534  1534
                TTJets  398.107170553   453   453
                TTJets  501.187233627   113   113
                TTJets   630.95734448    22    22
                TTJets  794.328234724     3     3
                TTJets           1000     2     2
                TTJets  1258.92541179     0     0
        TToLeptons_sch  3.16227766017     3     3
        TToLeptons_sch  3.98107170553     6     6
        TToLeptons_sch  5.01187233627     8     8
        TToLeptons_sch   6.3095734448    22    22
        TToLeptons_sch  7.94328234724    27    27
        TToLeptons_sch             10    62    62
        TToLeptons_sch  12.5892541179   100   100
        TToLeptons_sch  15.8489319246   169   169
        TToLeptons_sch  19.9526231497   240   240
        TToLeptons_sch  25.1188643151   383   383
        TToLeptons_sch  31.6227766017   491   491
        TToLeptons_sch  39.8107170553   673   673
        TToLeptons_sch  50.1187233627   918   918
        TToLeptons_sch   63.095734448   949   949
        TToLeptons_sch  79.4328234724   876   876
        TToLeptons_sch            100   593   593
        TToLeptons_sch  125.892541179   441   441
        TToLeptons_sch  158.489319246   269   269
        TToLeptons_sch  199.526231497   138   138
        TToLeptons_sch  251.188643151    60    60
        TToLeptons_sch  316.227766017    21    21
        TToLeptons_sch  398.107170553     7     7
        TToLeptons_sch  501.187233627     3     3
        TToLeptons_sch   630.95734448     1     1
        TToLeptons_sch  794.328234724     0     0
        TToLeptons_tch  2.51188643151     3     3
        TToLeptons_tch  3.16227766017    10    10
        TToLeptons_tch  3.98107170553    35    35
        TToLeptons_tch  5.01187233627    60    60
        TToLeptons_tch   6.3095734448   124   124
        TToLeptons_tch  7.94328234724   227   227
        TToLeptons_tch             10   398   398
        TToLeptons_tch  12.5892541179   646   646
        TToLeptons_tch  15.8489319246  1051  1051
        TToLeptons_tch  19.9526231497  1630  1630
        TToLeptons_tch  25.1188643151  2316  2316
        TToLeptons_tch  31.6227766017  3326  3326
        TToLeptons_tch  39.8107170553  4459  4459
        TToLeptons_tch  50.1187233627  5701  5701
        TToLeptons_tch   63.095734448  6784  6784
        TToLeptons_tch  79.4328234724  6582  6582
        TToLeptons_tch            100  5220  5220
        TToLeptons_tch  125.892541179  3637  3637
        TToLeptons_tch  158.489319246  2213  2213
        TToLeptons_tch  199.526231497  1096  1096
        TToLeptons_tch  251.188643151   471   471
        TToLeptons_tch  316.227766017   186   186
        TToLeptons_tch  398.107170553    77    77
        TToLeptons_tch  501.187233627    27    27
        TToLeptons_tch   630.95734448     6     6
        TToLeptons_tch  794.328234724     0     0
                T_tWch  1.58489319246     1     1
                T_tWch  1.99526231497     1     1
                T_tWch  2.51188643151     8     8
                T_tWch  3.16227766017     8     8
                T_tWch  3.98107170553    13    13
                T_tWch  5.01187233627    20    20
                T_tWch   6.3095734448    37    37
                T_tWch  7.94328234724    76    76
                T_tWch             10   116   116
                T_tWch  12.5892541179   177   177
                T_tWch  15.8489319246   289   289
                T_tWch  19.9526231497   413   413
                T_tWch  25.1188643151   601   601
                T_tWch  31.6227766017   809   809
                T_tWch  39.8107170553  1046  1046
                T_tWch  50.1187233627  1359  1359
                T_tWch   63.095734448  1575  1575
                T_tWch  79.4328234724  1586  1586
                T_tWch            100  1378  1378
                T_tWch  125.892541179  1130  1130
                T_tWch  158.489319246   727   727
                T_tWch  199.526231497   434   434
                T_tWch  251.188643151   204   204
                T_tWch  316.227766017    74    74
                T_tWch  398.107170553    46    46
                T_tWch  501.187233627    16    16
                T_tWch   630.95734448     7     7
                T_tWch  794.328234724     0     0
                T_tWch  1258.92541179     1     1
                T_tWch  1584.89319246     0     0
 WJetsToLNu_HT100to200  2.51188643151     3     3
 WJetsToLNu_HT100to200  3.16227766017     1     1
 WJetsToLNu_HT100to200  3.98107170553     1     1
 WJetsToLNu_HT100to200  5.01187233627     6     6
 WJetsToLNu_HT100to200   6.3095734448    14    14
 WJetsToLNu_HT100to200  7.94328234724    24    24
 WJetsToLNu_HT100to200             10    41    41
 WJetsToLNu_HT100to200  12.5892541179    59    59
 WJetsToLNu_HT100to200  15.8489319246   103   103
 WJetsToLNu_HT100to200  19.9526231497   135   135
 WJetsToLNu_HT100to200  25.1188643151   175   175
 WJetsToLNu_HT100to200  31.6227766017   241   241
 WJetsToLNu_HT100to200  39.8107170553   319   319
 WJetsToLNu_HT100to200  50.1187233627   390   390
 WJetsToLNu_HT100to200   63.095734448   411   411
 WJetsToLNu_HT100to200  79.4328234724   329   329
 WJetsToLNu_HT100to200            100   277   277
 WJetsToLNu_HT100to200  125.892541179   163   163
 WJetsToLNu_HT100to200  158.489319246    61    61
 WJetsToLNu_HT100to200  199.526231497     3     3
 WJetsToLNu_HT100to200  251.188643151     1     1
 WJetsToLNu_HT100to200  316.227766017     0     0
 WJetsToLNu_HT200to400  1.25892541179     5     5
 WJetsToLNu_HT200to400  1.58489319246     3     3
 WJetsToLNu_HT200to400  1.99526231497    25    25
 WJetsToLNu_HT200to400  2.51188643151    67    67
 WJetsToLNu_HT200to400  3.16227766017   120   120
 WJetsToLNu_HT200to400  3.98107170553   225   225
 WJetsToLNu_HT200to400  5.01187233627   434   434
 WJetsToLNu_HT200to400   6.3095734448   813   813
 WJetsToLNu_HT200to400  7.94328234724  1511  1511
 WJetsToLNu_HT200to400             10  2407  2407
 WJetsToLNu_HT200to400  12.5892541179  3934  3934
 WJetsToLNu_HT200to400  15.8489319246  5816  5816
 WJetsToLNu_HT200to400  19.9526231497  8530  8530
 WJetsToLNu_HT200to400  25.1188643151 11824 11824
 WJetsToLNu_HT200to400  31.6227766017 15518 15518
 WJetsToLNu_HT200to400  39.8107170553 18453 18453
 WJetsToLNu_HT200to400  50.1187233627 21396 21396
 WJetsToLNu_HT200to400   63.095734448 22148 22148
 WJetsToLNu_HT200to400  79.4328234724 18630 18630
 WJetsToLNu_HT200to400            100 14370 14370
 WJetsToLNu_HT200to400  125.892541179 10536 10536
 WJetsToLNu_HT200to400  158.489319246  6990  6990
 WJetsToLNu_HT200to400  199.526231497  3260  3260
 WJetsToLNu_HT200to400  251.188643151   972   972
 WJetsToLNu_HT200to400  316.227766017    93    93
 WJetsToLNu_HT200to400  398.107170553     2     2
 WJetsToLNu_HT200to400  501.187233627     0     0
 WJetsToLNu_HT400to600              1     3     3
 WJetsToLNu_HT400to600  1.25892541179     3     3
 WJetsToLNu_HT400to600  1.58489319246    20    20
 WJetsToLNu_HT400to600  1.99526231497    45    45
 WJetsToLNu_HT400to600  2.51188643151    90    90
 WJetsToLNu_HT400to600  3.16227766017   213   213
 WJetsToLNu_HT400to600  3.98107170553   385   385
 WJetsToLNu_HT400to600  5.01187233627   754   754
 WJetsToLNu_HT400to600   6.3095734448  1383  1383
 WJetsToLNu_HT400to600  7.94328234724  2434  2434
 WJetsToLNu_HT400to600             10  3797  3797
 WJetsToLNu_HT400to600  12.5892541179  6147  6147
 WJetsToLNu_HT400to600  15.8489319246  9484  9484
 WJetsToLNu_HT400to600  19.9526231497 13834 13834
 WJetsToLNu_HT400to600  25.1188643151 19165 19165
 WJetsToLNu_HT400to600  31.6227766017 25282 25282
 WJetsToLNu_HT400to600  39.8107170553 31855 31855
 WJetsToLNu_HT400to600  50.1187233627 37852 37852
 WJetsToLNu_HT400to600   63.095734448 41281 41281
 WJetsToLNu_HT400to600  79.4328234724 38363 38363
 WJetsToLNu_HT400to600            100 31679 31679
 WJetsToLNu_HT400to600  125.892541179 25610 25610
 WJetsToLNu_HT400to600  158.489319246 20462 20462
 WJetsToLNu_HT400to600  199.526231497 15822 15822
 WJetsToLNu_HT400to600  251.188643151 11213 11213
 WJetsToLNu_HT400to600  316.227766017  6071  6071
 WJetsToLNu_HT400to600  398.107170553  1604  1604
 WJetsToLNu_HT400to600  501.187233627   100   100
 WJetsToLNu_HT400to600   630.95734448     0     0
 WJetsToLNu_HT600toInf  0.63095734448     1     1
 WJetsToLNu_HT600toInf 0.794328234724     1     1
 WJetsToLNu_HT600toInf              1     5     5
 WJetsToLNu_HT600toInf  1.25892541179    15    15
 WJetsToLNu_HT600toInf  1.58489319246    25    25
 WJetsToLNu_HT600toInf  1.99526231497    35    35
 WJetsToLNu_HT600toInf  2.51188643151   105   105
 WJetsToLNu_HT600toInf  3.16227766017   162   162
 WJetsToLNu_HT600toInf  3.98107170553   381   381
 WJetsToLNu_HT600toInf  5.01187233627   699   699
 WJetsToLNu_HT600toInf   6.3095734448  1202  1202
 WJetsToLNu_HT600toInf  7.94328234724  2093  2093
 WJetsToLNu_HT600toInf             10  3206  3206
 WJetsToLNu_HT600toInf  12.5892541179  5246  5246
 WJetsToLNu_HT600toInf  15.8489319246  8062  8062
 WJetsToLNu_HT600toInf  19.9526231497 11949 11949
 WJetsToLNu_HT600toInf  25.1188643151 16731 16731
 WJetsToLNu_HT600toInf  31.6227766017 22405 22405
 WJetsToLNu_HT600toInf  39.8107170553 28826 28826
 WJetsToLNu_HT600toInf  50.1187233627 35694 35694
 WJetsToLNu_HT600toInf   63.095734448 40970 40970
 WJetsToLNu_HT600toInf  79.4328234724 41064 41064
 WJetsToLNu_HT600toInf            100 36220 36220
 WJetsToLNu_HT600toInf  125.892541179 30946 30946
 WJetsToLNu_HT600toInf  158.489319246 25925 25925
 WJetsToLNu_HT600toInf  199.526231497 20993 20993
 WJetsToLNu_HT600toInf  251.188643151 16588 16588
 WJetsToLNu_HT600toInf  316.227766017 12855 12855
 WJetsToLNu_HT600toInf  398.107170553  9204  9204
 WJetsToLNu_HT600toInf  501.187233627  5267  5267
 WJetsToLNu_HT600toInf   630.95734448  1852  1852
 WJetsToLNu_HT600toInf  794.328234724   581   581
 WJetsToLNu_HT600toInf           1000   144   144
 WJetsToLNu_HT600toInf  1258.92541179    30    30
 WJetsToLNu_HT600toInf  1584.89319246     5     5
 WJetsToLNu_HT600toInf  1995.26231497     0     0
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_process = pd.read_table(cStringIO.StringIO(
"""             component             phasespace  process
       QCD_HT_100To250        QCD_HT_100To250  QCD
       QCD_HT_250To500        QCD_HT_250To500  QCD
      QCD_HT_500To1000       QCD_HT_500To1000  QCD
      QCD_HT_1000ToInf       QCD_HT_1000ToInf  QCD
  QCD_HT_250To500_ext1        QCD_HT_250To500  QCD
 QCD_HT_500To1000_ext1       QCD_HT_500To1000  QCD
 QCD_HT_1000ToInf_ext1       QCD_HT_1000ToInf  QCD
        TToLeptons_sch         TToLeptons_sch  T
     TBarToLeptons_sch      TBarToLeptons_sch  T
        TToLeptons_tch         TToLeptons_tch  T
     TBarToLeptons_tch      TBarToLeptons_tch  T
                T_tWch                 T_tWch  T
             TBar_tWch              TBar_tWch  T
                TTJets                 TTJets  TTJets
 WJetsToLNu_HT100to200  WJetsToLNu_HT100to200  WJetsToLNu
 WJetsToLNu_HT200to400  WJetsToLNu_HT200to400  WJetsToLNu
 WJetsToLNu_HT400to600  WJetsToLNu_HT400to600  WJetsToLNu
 WJetsToLNu_HT600toInf  WJetsToLNu_HT600toInf  WJetsToLNu
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_xsec = pd.read_table(cStringIO.StringIO(
"""             component     xsec
      QCD_HT_1000ToInf    769.7
 QCD_HT_1000ToInf_ext1    769.7
       QCD_HT_100To250 28730000
       QCD_HT_250To500   670500
  QCD_HT_250To500_ext1   670500
      QCD_HT_500To1000    26740
 QCD_HT_500To1000_ext1    26740
                T_tWch     35.6
             TBar_tWch     35.6
     TBarToLeptons_sch  1.34784
     TBarToLeptons_tch 26.23428
                TTJets    809.1
        TToLeptons_sch   2.3328
        TToLeptons_tch  44.0802
 WJetsToLNu_HT100to200  2234.91
 WJetsToLNu_HT200to400  580.068
 WJetsToLNu_HT400to600  68.4003
 WJetsToLNu_HT600toInf  23.1363
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_nevt = pd.read_table(cStringIO.StringIO(
"""             component     nevt     nevt_sumw
      QCD_HT_1000ToInf  1130720       1130720
 QCD_HT_1000ToInf_ext1   333733        333733
       QCD_HT_100To250  4123612       4123612
       QCD_HT_250To500  2004219       2004219
  QCD_HT_250To500_ext1   663953        663953
      QCD_HT_500To1000  3214312       3214312
 QCD_HT_500To1000_ext1   849033        849033
                T_tWch   986100        986100
             TBar_tWch   971800        971800
     TBarToLeptons_sch   250000 320855.887262
     TBarToLeptons_tch  1999800 50734279.1235
                TTJets 25446993      25446993
        TToLeptons_sch   500000 1042218.60703
        TToLeptons_tch  3991000 173500373.328
 WJetsToLNu_HT100to200  5262265       5262265
 WJetsToLNu_HT200to400  4936077       4936077
 WJetsToLNu_HT400to600  4640594       4640594
 WJetsToLNu_HT600toInf  4581841       4581841
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_process_met = pd.read_table(cStringIO.StringIO(
"""    process          met         xsec       xsecvar
        QCD    15.848932 1.368716e-02  8.688971e-05
        QCD    19.952623 5.264628e-02  3.464539e-04
        QCD    25.118864 2.649828e-01  6.323639e-02
        QCD    31.622777 2.660340e-01  6.323694e-02
        QCD    39.810717 3.448069e-02  2.173624e-04
        QCD    50.118723 3.005147e-01  6.345431e-02
        QCD    63.095734 5.369746e-02  3.470063e-04
        QCD    79.432823 2.655084e-01  6.323667e-02
        QCD   100.000000 1.526393e-02  8.771844e-05
        QCD   125.892541 1.421275e-02  8.716595e-05
        QCD   158.489319 6.580785e-03  4.330673e-05
        QCD   199.526231 0.000000e+00  0.000000e+00
          T     1.584893 7.273487e-05  2.645322e-09
          T     1.995262 1.093679e-04  3.987302e-09
          T     2.511886 4.449668e-04  1.499073e-08
          T     3.162278 5.706285e-04  1.545752e-08
          T     3.981072 1.428873e-03  3.620408e-08
          T     5.011872 2.899586e-03  7.607640e-08
          T     6.309573 4.778792e-03  1.186380e-07
          T     7.943282 9.789808e-03  2.517474e-07
          T    10.000000 1.571253e-02  3.873900e-07
          T    12.589254 2.498557e-02  6.044784e-07
          T    15.848932 4.218602e-02  1.034794e-06
          T    19.952623 6.056201e-02  1.440993e-06
          T    25.118864 8.617993e-02  2.042942e-06
          T    31.622777 1.209879e-01  2.822036e-06
          T    39.810717 1.606320e-01  3.740323e-06
          T    50.118723 2.069109e-01  4.812857e-06
          T    63.095734 2.408201e-01  5.582021e-06
          T    79.432823 2.325000e-01  5.463718e-06
          T   100.000000 1.932338e-01  4.746694e-06
          T   125.892541 1.451699e-01  3.689381e-06
          T   158.489319 9.199799e-02  2.394710e-06
          T   199.526231 4.827836e-02  1.304397e-06
          T   251.188643 2.276847e-02  6.354342e-07
          T   316.227766 9.003777e-03  2.557210e-07
          T   398.107171 4.224795e-03  1.250214e-07
          T   501.187234 1.696152e-03  5.279640e-08
          T   630.957344 4.335469e-04  1.390304e-08
          T   794.328235 0.000000e+00  0.000000e+00
          T  1258.925412 3.610182e-05  1.303341e-09
          T  1584.893192 0.000000e+00  0.000000e+00
     TTJets     1.258925 1.271820e-04  4.043817e-09
     TTJets     1.584893 1.907730e-04  6.065725e-09
     TTJets     1.995262 1.144638e-03  3.639435e-08
     TTJets     2.511886 1.939526e-03  6.166820e-08
     TTJets     3.162278 5.627804e-03  1.789389e-07
     TTJets     3.981072 1.090586e-02  3.467573e-07
     TTJets     5.011872 2.168453e-02  6.894707e-07
     TTJets     6.309573 4.346446e-02  1.381974e-06
     TTJets     7.943282 7.475123e-02  2.376753e-06
     TTJets    10.000000 1.267687e-01  4.030674e-06
     TTJets    12.589254 2.099139e-01  6.674319e-06
     TTJets    15.848932 3.351246e-01  1.065546e-05
     TTJets    19.952623 5.120348e-01  1.628041e-05
     TTJets    25.118864 7.593085e-01  2.414260e-05
     TTJets    31.622777 1.044896e+00  3.322299e-05
     TTJets    39.810717 1.402309e+00  4.458712e-05
     TTJets    50.118723 1.790373e+00  5.692582e-05
     TTJets    63.095734 2.052813e+00  6.527023e-05
     TTJets    79.432823 1.998570e+00  6.354555e-05
     TTJets   100.000000 1.644368e+00  5.228352e-05
     TTJets   125.892541 1.172491e+00  3.727995e-05
     TTJets   158.489319 7.201682e-01  2.289811e-05
     TTJets   199.526231 3.473977e-01  1.104569e-05
     TTJets   251.188643 1.368797e-01  4.352158e-06
     TTJets   316.227766 4.877431e-02  1.550804e-06
     TTJets   398.107171 1.440336e-02  4.579622e-07
     TTJets   501.187234 3.592892e-03  1.142378e-07
     TTJets   630.957344 6.995011e-04  2.224099e-08
     TTJets   794.328235 9.538652e-05  3.032862e-09
     TTJets  1000.000000 6.359101e-05  2.021908e-09
     TTJets  1258.925412 0.000000e+00  0.000000e+00
 WJetsToLNu     0.630957 5.049564e-06  2.549810e-11
 WJetsToLNu     0.794328 5.049564e-06  2.549810e-11
 WJetsToLNu     1.000000 6.946649e-05  7.792541e-10
 WJetsToLNu     1.258925 7.075421e-04  7.008428e-08
 WJetsToLNu     1.584893 7.735782e-04  4.641257e-08
 WJetsToLNu     1.995262 3.777915e-03  3.559191e-07
 WJetsToLNu     2.511886 1.100445e-02  1.488624e-06
 WJetsToLNu     3.162278 1.848418e-02  1.887981e-06
 WJetsToLNu     3.981072 3.446442e-02  3.380984e-06
 WJetsToLNu     5.011872 6.819344e-02  7.257423e-06
 WJetsToLNu     6.309573 1.279408e-01  1.408389e-05
 WJetsToLNu     7.943282 2.342044e-01  2.577807e-05
 WJetsToLNu    10.000000 3.724289e-01  4.154270e-05
 WJetsToLNu    12.589254 6.044596e-01  6.643989e-05
 WJetsToLNu    15.848932 9.077172e-01  1.011636e-04
 WJetsToLNu    19.952623 1.323991e+00  1.454601e-04
 WJetsToLNu    25.118864 1.830800e+00  1.994453e-04
 WJetsToLNu    31.622777 2.411748e+00  2.638378e-04
 WJetsToLNu    39.810717 2.919091e+00  3.200311e-04
 WJetsToLNu    50.118723 3.418168e+00  3.749586e-04
 WJetsToLNu    63.095734 3.592642e+00  3.900111e-04
 WJetsToLNu    79.432823 3.101860e+00  3.260052e-04
 WJetsToLNu   100.000000 2.456178e+00  2.562195e-04
 WJetsToLNu   125.892541 1.841119e+00  1.812562e-04
 WJetsToLNu   158.489319 1.279855e+00  1.126413e-04
 WJetsToLNu   199.526231 7.235910e-01  4.953444e-05
 WJetsToLNu   251.188643 3.636871e-01  1.646274e-05
 WJetsToLNu   316.227766 1.653250e-01  2.931061e-06
 WJetsToLNu   398.107171 7.035347e-02  6.107808e-07
 WJetsToLNu   501.187234 2.807001e-02  1.560239e-07
 WJetsToLNu   630.957344 9.351793e-03  4.722248e-08
 WJetsToLNu   794.328235 2.933797e-03  1.481439e-08
 WJetsToLNu  1000.000000 7.271372e-04  3.671726e-09
 WJetsToLNu  1258.925412 1.514869e-04  7.649429e-10
 WJetsToLNu  1584.893192 2.524782e-05  1.274905e-10
 WJetsToLNu  1995.262315 0.000000e+00  0.000000e+00
"""), delim_whitespace = True)

##____________________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class Test_combine_MC_yields_in_datasets_into_xsec_in_processes(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

    def test_one(self):
        expect = tbl_process_met
        actual = combine_MC_yields_in_datasets_into_xsec_in_processes(tbl_component_met, tbl_process, tbl_nevt, tbl_xsec)
        self.assertEqual(expect, actual)


        ## print actual.to_string(index = False, formatters={'xsec':'{:e}'.format})
        ## lumi = 4000
        ## actual['n'] = actual.xsec*lumi
        ## actual['nvar'] = actual.xsecvar*lumi**2
        ## del actual['xsec']
        ## del actual['xsecvar']
        ## self.assertEqual(expect, actual)

    # to test
    #  - unique xsec for phasespaces
    #  - conflicting variable names

##____________________________________________________________________________||
