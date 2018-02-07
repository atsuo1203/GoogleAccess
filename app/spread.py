import yaml
from gspread import Client, authorize, Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from typing import List

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
def create_spreadsheet(sheet_name: str):
    # 重複していたら終了させる
    sheets = get_all_spreadsheets()
    for sheet in sheets:
        if sheet.title == sheet_name:
            print('すでに作成されています')
            print('https://docs.google.com/spreadsheets/d/'+sheet.id+'/edit#gid=0')
            return

    new_sp = client.create(sheet_name)
    print('https://docs.google.com/spreadsheets/d/'+new_sp.id+'/edit#gid=0')


def get_all_spreadsheets():
    return client.openall()


def get_spreadsheet(sheet_name: str) -> Spreadsheet:
    return client.open(sheet_name)


def _remove_spreadsheet(sheet_id):
    client.del_spreadsheet(sheet_id)


def remove_spreadsheet(sheet_name: str):
    sheet = get_spreadsheet(sheet_name)
    _remove_spreadsheet(sheet.id)


def remove_all_spreadsheet():
    sheets = get_all_spreadsheets()
    for sheet in sheets:
        _remove_spreadsheet(sheet.id)


# 権限関係
def permissions(sheet_name: str):
    return client.list_permissions(get_spreadsheet(sheet_name).id)


def add_permission(sheet_name: str, user_name: str):
    client.insert_permission(get_spreadsheet(sheet_name).id,
                             data[user_name]['email'],
                             perm_type='user',
                             role='writer'
                             )


def remove_permission(sheet_name: str, user_name: str):
    sheet = get_spreadsheet(sheet_name)
    client.remove_permission(sheet.id, data[user_name]['id'])


# work_sheet関係
def create_worksheet(sheet_name: str, worksheet_name: str, rows: int=1000, cols: int=100):
    sheet = get_spreadsheet(sheet_name)
    for worksheet in sheet.worksheets():
        if worksheet.title == worksheet_name:
            print('すでに作成されています')
            return

    sheet.add_worksheet(worksheet_name, rows, cols)


def write_cell(sheet_name: str, worksheet_name: str, acell: str='A1', text: str='test'):
    sheet = client.open(sheet_name)
    worksheet = get_worksheet(sheet, worksheet_name)
    worksheet.update_acell(acell, text)


def write_cells(sheet_name: str, worksheet_name: str, datas_list: List[List[str]]):
    sheet = get_spreadsheet(sheet_name)
    worksheet = get_worksheet(sheet, worksheet_name)
    start = time.time()
    cell_list = []
    for row, datas in enumerate(datas_list, 1):
        for col, data in enumerate(datas, 1):
            cell = worksheet.cell(row, col)
            cell.value = data
            cell_list.append(cell)
    worksheet.update_cells(cell_list)
    elapsed_time = time.time() - start
    print('write_cells : ', elapsed_time, ' [sec]')


def append_cells(sheet_name: str, worksheet_name: str, datas_list: List[List[str]]):
    sheet = get_spreadsheet(sheet_name)
    worksheet = get_worksheet(sheet, worksheet_name)
    start = time.time()
    for datas in datas_list:
        worksheet.append_row(datas)
    elapsed_time = time.time() - start
    print('append_cells : ', elapsed_time, ' [sec]')


def insert_cells(sheet_name: str, worksheet_name: str, datas_list: List[List[str]]):
    sheet = get_spreadsheet(sheet_name)
    worksheet = get_worksheet(sheet, worksheet_name)
    start = time.time()
    for datas in datas_list:
        worksheet.insert_row(datas)
    elapsed_time = time.time() - start
    print('insert_cells : ', elapsed_time, ' [sec]')


def remove_worksheet(sheet_name: str, worksheet_name: str):
    sheet = get_spreadsheet(sheet_name)
    worksheet = get_worksheet(sheet, worksheet_name)
    if worksheet.title == worksheet_name:
        sheet.del_worksheet(worksheet)
        print('[worksheet]' + worksheet.title + ' を削除しました')


def get_worksheet(sheet: Spreadsheet, worksheet_name: str) -> Worksheet:
    worksheets = sheet.worksheets()
    for worksheet in worksheets:
        if worksheet.title == worksheet_name:
            return worksheet

    raise Exception('worksheetが存在しません')

