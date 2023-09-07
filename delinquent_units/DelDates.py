import datetime


def get_dates():
    """
    Gets notice and payment dates to be 
    used within the DelinquentUnits class.

    Return:
        notice_date (str): The current date.
        due_date (str): The date three days from now, excluding 
                        weekends and recognized holidays.
    """
    notice_date = datetime.date.today()
    due_date = get_payment_date(notice_date)
    notice_date = notice_date.strftime("%m/%d/%y")
    due_date = due_date.strftime("%m/%d/%y")

    print(f"        Today's date is {notice_date}")
    print(f"The payment due date is {due_date}")

    while input("\nAre these dates correct? (y/n):\n> ") == "n":
        print("\nPlease enter the correct dates in mm/dd/yy format.")
        print("Enter today's date: ")
        notice_date = input("> ")
        print("Enter the payment due date: ")
        due_date = input("> ")
        print("\nCurrent and payment due dates have been changed to",
              f"{notice_date} and {due_date}")

    return notice_date, due_date


def get_payment_date(notice_date):
    """
    Calculates the date three days from now excluding weekends. 

    Parameters:
        notice_date (datetime object): The current date.
    """
    days_to_add = 3
    # If notice_date is anything other than Monday or Tuesday,
    # five days will need to be added to exclude weekends.
    if notice_date.weekday() > 1:
        days_to_add = 5
    return notice_date + datetime.timedelta(days=days_to_add)