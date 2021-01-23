from autoclass import auto_class
import datetime
from time import sleep
def main():
    now = datetime.datetime.now()
    noClassLeft = auto_class()
    print(noClassLeft)
    if noClassLeft:
        tom = datetime.datetime(now.year, now.month, now.day+1, 8, 00, 00)
        print("Done for today")
        print(f'Sleeping for {(tom - now)}')
        sleep((tom - now).total_seconds())

if __name__ == "__main__":
    main()