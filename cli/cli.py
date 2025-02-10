import argparse
from cli.commands import addBook, getBook, delBook
from localization.localization import load_localization, set_localization
from validation.validation import validate_available_amount, validate_condition, validate_fine, validate_name, validate_number, validate_sn, validate_text, validate_year


loc = load_localization()

#function to get the corresponding value from the arguments class that is language dependent
def arg(args, arg_name):
    try:
        return getattr(args, loc[arg_name].strip("-"))
    except KeyError:
        raise ValueError(loc["KeyUnkownError"].format(arg_name=arg_name))

#use the argparse module to parse the arguments provided at the command line
def create_parser():
    parser = argparse.ArgumentParser(description=loc["parserDescription"],
                                     usage=loc["parserUsage"])

    #subcomands
    subparser = parser.add_subparsers(dest=loc["command"], required=True, help=loc["subparserHelp"])

    #Change language subcommand
    change_language_parser = subparser.add_parser(loc["changeLanguageCmd"], help=loc["changeLanguageCmdHelp"])
    change_language_parser.add_argument("-en", action="store_true", help="english")
    change_language_parser.add_argument("-pt", action="store_true", help="português")

    #AddBook subcommand
    add_book_parser = subparser.add_parser(loc["addBookCmd"], help=loc["addBookHelp"])
    add_book_parser.add_argument(loc["snArg"], metavar="", type=int, required=True, help=loc["snArgHelp"])     
    add_book_parser.add_argument(loc["titleArg"], metavar="", type=str, required=True, help=loc["titleHelp"])   
    add_book_parser.add_argument(loc["yearArg"], metavar="", type=int, required=True, help=loc["yearHelp"])
    add_book_parser.add_argument(loc["fineArg"], metavar="", type=float, required=True, help=loc["fineHelp"])
    add_book_parser.add_argument(loc["publisherIDArg"], metavar="", type=int, required=True, help=loc["publisherIDHelp"])
    add_book_parser.add_argument(loc["amountArg"], metavar="", type=int, required=True, help=loc["amountHelp"])
    add_book_parser.add_argument(loc["availableAmountArg"], metavar="", type=int, required=True, help=loc["availableAmountHelp"])
    add_book_parser.add_argument(loc["categoryIDArg"], metavar="", type=int, required=True, help=loc["categoryIDHelp"])
    add_book_parser.add_argument(loc["authorArg"], metavar="", type=str, required=True, help=loc["authorHelp"])

    #getBook subcommand
    get_book_parser = subparser.add_parser(loc["getBookCmd"], help=loc["getBookHelp"])
    get_book_parser.add_argument(loc["snArg"], metavar="", type=int, help=loc["snGetBookHelp"])     
    get_book_parser.add_argument(loc["titleArg"], metavar="", type=str, help=loc["titleGetBookHelp"])   
    get_book_parser.add_argument(loc["publisherArg"], metavar="", type=str, help=loc["publisherHelp"])
    get_book_parser.add_argument(loc["categoryArg"], metavar="", type=str, help=loc["categoryHelp"])
    get_book_parser.add_argument(loc["authorArg"], metavar="", type=str, help=loc["authorGetBookHelp"])

    #delBook subcommand
    del_book_parser = subparser.add_parser(loc["delBookCmd"], help=loc["delBookHelp"])
    del_book_parser.add_argument(loc["snArg"], metavar="", type=int, help=loc["snDelBookHelp"])
    del_book_parser.add_argument(loc["copyIDArg"], metavar="", type=int, help=loc["copyIDHelp"])
    del_book_parser.add_argument(loc["conditionArg"], metavar="", type=str, help=loc["conditionHelp"])

    return parser

#Main function to call the function with the correct arguments
def main():
    global loc #to modify the global variable so there's no delay updating the language

    parser = create_parser()
    args = parser.parse_args() #parse the command-line arguments

    command = getattr(args, loc["command"])

    #validate user inputs
    if command == loc["changeLanguageCmd"]:
        if args.en:
            set_localization("en")
            loc = load_localization()
            print(loc["languageChanged"])
        elif args.pt:
            set_localization("pt")
            loc = load_localization()
            print(loc["languageChanged"])
        else:
            print(loc["languageError"])
        
    elif command == loc["addBookCmd"]:
        sn = validate_sn(arg(args, "snArg"))
        title = validate_text(arg(args, "titleArg"), loc["titleField"])
        year = validate_year(arg(args,"yearArg"))
        fine = validate_fine(arg(args, "fineArg"))
        publisher_id = validate_number(arg(args, "publisherIDArg"), loc["publisherIDField"])
        amount = validate_number(arg(args, "amountArg"), loc["amountField"])
        available_amount = validate_available_amount(arg(args, "availableAmountArg"), arg(args,"amountArg"))
        category_id = validate_number(arg(args, "categoryIDArg"), loc["categoryIDField"])
        author = validate_name(arg(args, "authorArg"), loc["authorField"])

        addBook(sn, title, year, fine, publisher_id, amount, available_amount, category_id, author)

    elif command == loc["getBookCmd"]:
        sn = validate_sn(arg(args, "snArg")) if arg(args, "snArg") else None
        title = validate_text(arg(args, "titleArg"), loc["titleField"]) if arg(args, "titleArg") else None
        publisher = validate_name(arg(args, "publisherArg"), loc["publisherField"]) if arg(args, "publisherArg") else None
        category = validate_name(arg(args, "categoryArg"), loc["categoryField"]) if arg(args, "categoryArg") else None
        author = validate_name(arg(args, "authorArg"), loc["authorField"]) if arg(args, "authorArg") else None
        
        getBook(sn, title, publisher, category, author)

    elif command == loc["delBookCmd"]:
        sn = validate_sn(arg(args, "snArg")) if arg(args, "snArg") else None
        copyid = validate_number(arg(args, "copyIDArg"),  loc["copyIDField"]) if arg(args, "copyIDArg") else None
        condition = validate_condition(arg(args, "conditionArg")) if arg(args, "conditionArg") else None
     
        delBook(sn, copyid, condition)


if __name__=="__main__":
    main()