from src.main import main
from os import environ

if __name__ == '__main__':
    if 'ANDROID_ARGUMENT' in environ:
        print('Please, run "run_android.py" for launch')
    else:
        main()
