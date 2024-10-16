"""
  author: nathan reed <nreed@linux.com>
  desc: a sandwhich shop emulator
  date: 10-08-24
"""

import sys

from typing import Union
from collections import namedtuple

from tabwriter import TabWriter


# global options
Option = ["exit", "-1"]

# global sandwhich inquries
Inventory = namedtuple(
    "Inventory", ["cost", "cost_per_serving", "sandwhich_inches", "servings"]
)

# WARN(nate): globally mutated
InventoryItems = []

# messages made by the emulator
WELCOME = "Welcome to the sandwhich shop!\n"
EXIT_MESSAGE = "\nhave a good one!"

# questions made by the emulator
QUESTION_COST = "How much does it cost?"
QUESTION_HOW_BIG = "How big should your sandwhich be? (inches)"
QUESTION_ANOTHER = "Would you like to try some more sandwhichs?[YES/no/ls]"

# to make these values unique. more or less and Enum :)
ST_CONTINUED = id(object())
ST_COMPLETED = id(object())


def print_help():
    """prints help message :)"""
    print()
    print("Please choose an option:\n")
    tw = TabWriter("")
    tw.writeln("Command\tDescription")
    tw.writeln("-------\t-----------")
    tw.writeln("ls\tlist sandwhich sale inquries")
    tw.writeln("?\tprints help table")
    tw.writeln("new\tstarts a new inqury")
    tw.writeln("ENTER\tstarts a new inqury")
    tw.writeln("exit\texits the program")
    tw.flush()
    print()


def input_safe(is_float: bool, display: str) -> Union[float, int]:
    """a way to wrap inputs representing int/float given a question
       always returns sys.exit or float/int

    Args:
        is_float (bool): do you want a float or int?
        display  (str): what to ask the user

    Returns:
        float | int: value representing what the caller asked for
    """

    # print initial text to the user
    print("\n", display)

    not_safe = True
    while not_safe:
        try:
            # it is rather common for users to give "$" when inserting
            # some kind of currency value. So just strip it off if its there
            i = input("> ").strip("$")
            i = i.strip('$?_" ')
            if i in Option:
                sys.exit(0)

            if is_float:
                n = float(i)
            else:
                n = int(i)

            # input cannot be negative
            if n > -1:
                break

        except ValueError:
            print(display)
            continue

        except KeyboardInterrupt:
            sys.exit(0)

    # paranoid, and largely not needed
    if n is None:
        print(f'"{n}" something went wrong')

    return n


def servings(inches: float) -> int:
    """each serving is 3 inches

    Args:
        inches (float): inches the user wants

    Returns:
        int: avaiable servings
    """
    s = inches / 3
    if s < 1:
        return s
    else:
        return int(s)


def serving_cost(srvings: float, total_cost: float) -> float:
    """computes cost per serving (should be inlined)

    Args:
        servings (float): the amounnt of servings the user asked about
        total_cost (float): cost, for some reason defined by the user

    Returns:
        float: cost per serving or -1(division by zero)
    """
    try:
        cost_per_serving = total_cost / srvings

    except ZeroDivisionError:
        return -1

    return cost_per_serving


def determine(item: str, extra=None):
    """determine is rather simple, we take in a str that is either an option
       or a number, if its neither then we just continue to the next input

    Args:
        item (str): item is expected to eventually be another unless its an option
        extra (list, optional): possible Options to exit on. Defaults to [].

    Returns: None
    """
    if item == "ls":
        print_inquries()
        ask_another()
        return ST_CONTINUED

    item = str(item)
    item = item.strip('$?_" ')

    # always early return for an Option
    if extra is not None and item in extra:
        print(EXIT_MESSAGE)
        sys.exit(0)

    if item in Option:
        print(EXIT_MESSAGE)
        sys.exit(0)

    try:
        if float(item) <= 0:
            return ST_CONTINUED
        # NOTE(nate): its not an option so just continue

    except ValueError:
        return ST_CONTINUED

    return ST_COMPLETED


def print_inquries():
    """Prints what sandwhich inquries the user has made over the lifetime of the program"""
    print()  # empty
    if len(InventoryItems) < 1:
        print("No inventory has been made yet.")
        return

    tw = TabWriter("")
    tw.writeln("Cost\tSize\tCost Per Serving\tAvailable Servings")
    for i in InventoryItems:
        tw.writeln(
            f"${i.cost:.2f}\t{i.sandwhich_inches:.2f}\"\t"
            + f"${i.cost_per_serving:.2f}\t{i.servings:.2f}"
        )
    tw.flush()
    print()  # empty


def ask_another():
    """ask another user if they want another sandwhich"""

    print(f"\nItems made {len(InventoryItems)}")
    yes_no = input(QUESTION_ANOTHER)
    while determine(yes_no, ["no"]) != ST_COMPLETED:
        if yes_no in Option:
            sys.exit(0)
        yes_no = input(QUESTION_ANOTHER)


def new_inquiry():
    """start a new inquiry

    Returns:
        Address: enum representing the state of the emulator
    """
    try:
        inches = input_safe(False, QUESTION_HOW_BIG)
        while determine(inches) != ST_COMPLETED:
            inches = input_safe(False, QUESTION_HOW_BIG)

        cost = input_safe(True, QUESTION_COST)
        while determine(cost) != ST_COMPLETED:
            cost = input_safe(True, QUESTION_COST)

    except KeyboardInterrupt:
        sys.exit(0)

    except ValueError:
        return ST_CONTINUED

    nservings = servings(inches)
    cost_per_serving = serving_cost(nservings, cost)
    InventoryItems.append(Inventory(cost, cost_per_serving, inches, nservings))
    print("\nWhat would you like to do next?")


# sandwhich emulator is our make shift sandwhich shop
def sandwhich_shop_emulator():
    """Emulate a sandwhich shop (our "main")"""
    first_time = True
    user = ""

    while user not in Option:
        # we dont have goto's here :(
        if first_time:
            print(WELCOME)
            print_help()
            first_time = False

        try:
            query = input("> ")
        except KeyboardInterrupt:
            print(EXIT_MESSAGE)
            sys.exit(0)

        if query == "new" or query == "":
            new_inquiry()
        elif query == "exit":
            print(EXIT_MESSAGE)
            sys.exit(0)
        elif query == "ls":
            print_inquries()
        elif query == "?" or query == "help":
            print_help()
        else:
            print('\nUnknown option: for help use "?" or "help"')


if __name__ == "__main__":
    sandwhich_shop_emulator()
