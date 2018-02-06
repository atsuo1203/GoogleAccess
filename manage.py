from logging import getLogger
from app import spread, drive

log = getLogger(__name__)

name = 'test2'

spread.create_spreadsheet(name)
spread.add_permission(name, 'atsuo')
print(spread.get_all_spreadsheets())
