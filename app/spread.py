import yaml
from gspread import Client, authorize
from oauth2client.service_account import ServiceAccountCredentials

CLIENT_SECRET_FILE = './projectName.json'
SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive'
          ]
file = open('config.yaml', "r+")
data = yaml.load(file)


def login_spreadsheets() -> Client:
    '''GoogleドライブにログインしてClientクラスを返す
    '''
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CLIENT_SECRET_FILE, SCOPES
        )
        return authorize(credentials)

    except Exception as e:
        raise Exception('GoogleDriveにログインできませんでした %s' % e)


client = login_spreadsheets()


# spreadsheet関係
def create_spreadsheet(sheet_name):
    # 重複していたら終了させる
    sheets = get_all_spreadsheets()
    for sheet in sheets:
        if sheet.title == sheet_name:
            print('すでに作成されています')
            print('https://docs.google.com/spreadsheets/d/'+sheet.id+'/edit#gid=0')
            return

    new_sp = client.create(sheet_name)
    print('https://docs.google.com/spreadsheets/d/'+new_sp.id+'/edit#gid=0')


def get_spreadsheet(sheet_name):
    return client.open(sheet_name)


def get_all_spreadsheets():
    return client.openall()


def _remove_spreadsheet(sheet_id):
    client.del_spreadsheet(sheet_id)


def remove_spreadsheet(sheet_name):
    sheet = get_spreadsheet(sheet_name)
    _remove_spreadsheet(sheet.id)


def remove_all_spreadsheet():
    sheets = get_all_spreadsheets()
    for sheet in sheets:
        _remove_spreadsheet(sheet.id)


# 権限関係
def permissions(sheet_name):
    return client.list_permissions(get_spreadsheet(sheet_name).id)


def add_permission(sheet_name, user):
    client.insert_permission(get_spreadsheet(sheet_name).id,
                             data[user]['email'],
                             perm_type='user',
                             role='writer'
                             )


def remove_permission(sheet_id, user_id):
    client.remove_permission(sheet_id, user_id)


# work_sheet関係
def add_worksheet(sheet_name, worksheet_name, rows=100, cols=100):
    sheet = get_spreadsheet(sheet_name)
    for worksheet in sheet.worksheets():
        if worksheet.title == worksheet_name:
            print('すでに作成されています')
            return

    sheet.add_worksheet(worksheet_name, rows, cols)


def write_worksheet(sheet_name, worksheet_index=0, acell='A1', text='test'):
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(worksheet_index)
    worksheet.update_acell(acell, text)


file.close()
