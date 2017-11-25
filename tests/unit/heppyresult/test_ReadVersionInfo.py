from alphatwirl.heppyresult import ReadVersionInfo
import os
import unittest
import io

##__________________________________________________________________||
sample_versionInfo_txt = b"""Tag for production: 
RA1cmg_v2.3

Extra information: 
commit 7eb4d0388dc1922ae00939af3d37a502b6f0f73e
Merge: 5163e43 c3dad01
Author: aelwood <adam.elwood09@imperial.ac.uk>
Date:   Tue Mar 31 16:48:11 2015 +0200

    Merge pull request #56 from CMSRA1/merge
    
    Merge latest CMG updates
"""

##__________________________________________________________________||
def mock_isfile(path): return False

##__________________________________________________________________||
class TestReadVersionInfo(unittest.TestCase):
    def test_read(self):
        readInfo = ReadVersionInfo()
        file = io.BytesIO(sample_versionInfo_txt)
        expected = {'full': sample_versionInfo_txt, 'tag': b'RA1cmg_v2.3'}
        self.assertEqual(expected, readInfo._readImp(file))

    def test_no_file(self):
        isfile_org = os.path.isfile
        os.path.isfile = mock_isfile

        readInfo = ReadVersionInfo()
        self.assertIsNone(readInfo('versionInfo.txt'))

        os.path.isfile = isfile_org

##__________________________________________________________________||
