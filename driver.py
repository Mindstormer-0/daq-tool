from modules.database import ini_database
from app.dashboard import run_dash


def main():
    ini_database()
    run_dash()


if __name__ == '__main__':
    main()
else:
    print("The driver should be executed directly.")
