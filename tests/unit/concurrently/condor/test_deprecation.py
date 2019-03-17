# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
def test_removed_job_desc_extra(caplog):
    job_desc_extra = ['request_memory = 900']
    with pytest.raises(TypeError):
        with caplog.at_level(logging.ERROR):
            obj = HTCondorJobSubmitter(job_desc_extra=job_desc_extra)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    assert 'concurrently.condor.submitter' in caplog.records[0].name
    assert '"job_desc_extra" is removed.' in caplog.records[0].msg

##__________________________________________________________________||
