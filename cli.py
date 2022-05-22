import argparse
import json

from assistant import Assistant


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phone_number', type=str, default='+77472447424')
    parser.add_argument('--shop', type=str, default='Shopify')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main():
    args = get_args()

    if args.verbose:
        print('Starting conversation with {}.\n'.format(args.phone_number))

    assistant = Assistant(verbose=args.verbose)

    print('\nHello, I am Connectly, assistant at {} online shop. How can I help you?'.format(args.shop))

    while True:
        query = input("Query: ")

        if query == 'c':
            exit()

        # Check if user is signed up
        if assistant.is_user_authorized(args.phone_number):
            response = assistant.handle(query, args.phone_number)
        else:
            # Sign up the user
            print('How can I call you?')
            first_name = input()
            assistant.authorize_user(args.phone_number, first_name)
            response = assistant.handle(query, args.phone_number, call_by_name=True)

        print(response)


if __name__ == "__main__":
    main()
