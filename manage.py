from logging import getLogger
from app import spread, drive

log = getLogger(__name__)

spread.permissions('test_of_test')
print(drive.get_file_list())
