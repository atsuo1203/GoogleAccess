from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# OAuth認証を行う
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)


# テキストをGoogleドライブに書き込む
def write_drive():
    f = drive.CreateFile({'title': 'test.txt'})
    f.SetContentString('賢い人に与えよ。彼はさらに賢くなる。')
    f.Upload()


def get_file_list():
    file_list = drive.ListFile().GetList()
    return file_list
