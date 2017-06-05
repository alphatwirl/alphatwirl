
//__________________________________________________________________||
// How to run:
// root -b -q create_sample_03.C
//__________________________________________________________________||
#include "TFile.h"
#include "TTree.h"

void create_sample_03()
{

  // https://root.cern.ch/doc/master/classTTree.html
  // https://root.cern.ch/root/html/RtypesCore.h
  Char_t bChar;
  UChar_t bUChar;
  Short_t bShort;
  UShort_t bUShort;
  Int_t bInt;
  UInt_t bUInt;
  Float_t bFloat;
  Double_t bDouble;
  Long64_t bLong64;
  ULong64_t bULong64;
  Bool_t bBool;

  //
  TFile f("sample_03.root","recreate");

  TTree *t = new TTree("tree", "sample tree");
  t->Branch("bChar", &bChar, "bChar/B");
  t->Branch("bUChar", &bUChar, "bUChar/b");
  t->Branch("bShort", &bShort, "bShort/S");
  t->Branch("bUShort", &bUShort, "bUShort/s");
  t->Branch("bInt", &bInt, "bInt/I");
  t->Branch("bUInt", &bUInt, "bUInt/i");
  t->Branch("bFloat", &bFloat, "bFloat/F");
  t->Branch("bDouble", &bDouble, "bDouble/D");
  t->Branch("bLong64", &bLong64, "bLong64/L");
  t->Branch("bULong64", &bULong64, "bULong64/l");
  t->Branch("bBool", &bBool, "bBool/O");

  // save 2 events

  // 1st event
  bChar = -3;
  bUChar = 2;
  bShort = -10;
  bUShort = 11;
  bInt = -22;
  bUInt = 32;
  bFloat = -0.123;
  bDouble = -2.345;
  bLong64 = -252;
  bULong64 = 332;
  bBool = 1;
  t->Fill();

  // 2nd event
  bChar = 8;
  bUChar = 4;
  bShort = 15;
  bUShort = 8;
  bInt = 42;
  bUInt = 12;
  bFloat = 0.244;
  bDouble = 3.122;
  bLong64 = 512;
  bULong64 = 123;
  bBool = 0;
  t->Fill();

  //
  t->Write();
}
