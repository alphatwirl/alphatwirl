
//__________________________________________________________________||
// How to run:
// root -b -q create_sample_04.C
//__________________________________________________________________||
#include "TFile.h"
#include "TTree.h"

void create_sample_04()
{

  // https://root.cern.ch/doc/master/classTTree.html
  // https://root.cern.ch/root/html/RtypesCore.h
  const Int_t kMaxVar = 4096;
  Int_t nvar;
  Char_t bChar[kMaxVar];
  UChar_t bUChar[kMaxVar];
  Short_t bShort[kMaxVar];
  UShort_t bUShort[kMaxVar];
  Int_t bInt[kMaxVar];
  UInt_t bUInt[kMaxVar];
  Float_t bFloat[kMaxVar];
  Double_t bDouble[kMaxVar];
  Long64_t bLong64[kMaxVar];
  ULong64_t bULong64[kMaxVar];
  Bool_t bBool[kMaxVar];

  //
  TFile f("sample_04.root","recreate");

  TTree *t = new TTree("tree", "sample tree");
  t->Branch("nvar", &nvar, "nvar/I");
  t->Branch("bChar", bChar, "bChar[nvar]/B");
  t->Branch("bUChar", bUChar, "bUChar[nvar]/b");
  t->Branch("bShort", bShort, "bShort[nvar]/S");
  t->Branch("bUShort", bUShort, "bUShort[nvar]/s");
  t->Branch("bInt", bInt, "bInt[nvar]/I");
  t->Branch("bUInt", bUInt, "bUInt[nvar]/i");
  t->Branch("bFloat", bFloat, "bFloat[nvar]/F");
  t->Branch("bDouble", bDouble, "bDouble[nvar]/D");
  t->Branch("bLong64", bLong64, "bLong64[nvar]/L");
  t->Branch("bULong64", bULong64, "bULong64[nvar]/l");
  t->Branch("bBool", bBool, "bBool[nvar]/O");

  // save 2 events

  // 1st event
  nvar = 2;
  bChar[0] = -125;
  bChar[1] = 38;
  bUChar[0] = 253;
  bUChar[1] = 20;
  bShort[0] = -10;
  bShort[1] = 120;
  bUShort[0] = 65530;
  bUShort[1] = 21221;
  bInt[0] = -2147483626;
  bInt[1] = 512;
  bUInt[0] = 4294967290;
  bUInt[1] = 1253;
  bFloat[0] = -0.123;
  bFloat[1] = 42.344;
  bDouble[0] = -2.345;
  bDouble[1] = 51.224;
  bLong64[0] = -4611686018427387900;
  bLong64[1] = 12345;
  bULong64[0] = 9223372036854775802;
  bULong64[1] = 12345514;
  bBool[0] = 1;
  bBool[1] = 1;
  t->Fill();

  //
  t->Write();
}
