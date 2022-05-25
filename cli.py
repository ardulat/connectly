import argparse
import logging

from assistant import Assistant


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phone_number', type=str, default='+77472447424')
    parser.add_argument('--shop', type=str, default='Shopify')
    return parser.parse_args()


def main():
    args = get_args()

    logger.info('Starting conversation with {}.'.format(args.phone_number))

    assistant = Assistant()

    print('\n{}: Hello, I am Connectly, assistant at {} online shop. How can I help you?'.format(args.shop, args.shop))

    while True:
        query = input("You: ")
        print()

        if query == 'c':
            exit()

        # Check if user is signed up
        if assistant.is_user_authorized(args.phone_number):
            response = assistant.handle(query, args.phone_number)
        else:
            # Sign up the user
            print('{}: How can I call you?'.format(args.shop))
            first_name = input("You: ")
            print()
            assistant.authorize_user(args.phone_number, first_name)
            response = assistant.handle(query, args.phone_number, call_by_name=True)

        print('\n{}: {}'.format(args.shop, response))


if __name__ == "__main__":
    main()
