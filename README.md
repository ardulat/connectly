# Connectly

This is a repo for the Connectly ML project. You can find more information about the company here: https://www.connectly.ai/about.

## Objectives

The main objective is to build a smart chatbot that automatically handles inbound messages. So I focused on the following:

- Handle various scenarios: sign up, purchase a product, ask for a recommendation, return a product
- Scale full lifecycle, e.g., add more scenarios, add more data, use different classifiers

## Directory organization
    .
    ├── classifiers             # Pre and post classifiers
    ├── data                    # Emulated database
    ├── forms                   # Regex-based forms (.txt files), configuration file for forms
    ├── handlers                # Scenario handlers
    ├── models                  # Models used throughout the project for convenience
    ├── tests                   # Test files
    ├── assistant.py            # Main Assistant class
    ├── cli.py                  # Command-line interface
    ├── utils.py                # Utility functions
    └── README.md

## How to scale

- Authorization: we can add more users to the "database."
- Frames: we can add more frames to the `forms/` directory as `.txt` files and add them to `forms/config.json`.
- Scenarios: we can add more scenario handlers and add them to `HANDLERS_MAP`.
- Classifiers: we can change classifiers and edit the few-shot learning task description in `classifiers/common.py`.

## Future work

- Implement a real frame-based approach, where the frame consists of `frame_name`, `slots`, `utterance`, etc.
- Implement taggers/named-entity recognition models to capture relevant slots for each scenario
- Implement modality logic, e.g., ellipsis intents with context storage
- Add more user scenarios, extend scenario logic
- Improve classifiers by adding quality tests to evaluate them
- Train custom fine-tuned classifiers instead of few-shot learning as we gather more data
- Improve the NLU module with lemmatization so that we can understand user queries even with mistyping
