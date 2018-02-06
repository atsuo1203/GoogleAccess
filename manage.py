from logging import getLogger
import yaml

from gspread import Client, authorize
from oauth2client.service_account import ServiceAccountCredentials

log = getLogger(__name__)

CLIENT_SECRET_FILE = './projectName.json'

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive'
          ]

file = open('config.yaml', "r+")
data = yaml.load(file)


def login_spread_sheets() -> Client:
    '''GoogleドライブにログインしてClientクラスを返す
    '''
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CLIENT_SECRET_FILE, SCOPES
        )
        return authorize(credentials)

    except Exception as e:
        raise Exception('GoogleDriveにログインできませんでした %s' % e)


client = login_spread_sheets()


def write_url_sheet(sheet_name):
    test_sheet_key = data[sheet_name]['sheet_id']
    spread_sheet = client.open_by_key(test_sheet_key)
    sheet1 = spread_sheet.get_worksheet(0)
    sheet1.update_acell('A1', 'test from python')


def create_spread_sheet(sheet_name):
    new_sp = client.create(sheet_name)
    print(new_sp.id)


def permissions(sheet_name):
    permission_list = client.list_permissions(data[sheet_name]['sheet_id'])
    print(permission_list)


def add_permissions(sheet_name, user):
    client.insert_permission(data[sheet_name],
                             data[user]['email'],
                             perm_type='user',
                             role='writer'
                             )


def delete_permissions(sheet_id, user_id):
    client.remove_permission(sheet_id, user_id)


permissions('test_of_test')
write_url_sheet('test_of_test')


file.close()

