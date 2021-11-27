# 🙋 Asking

**Asking** is a Python package that helps you ask questions and get answers from command line users.

[![asciicast](https://asciinema.org/a/oJHcctFXKkwoLorefCi0JfNDi.svg)](https://asciinema.org/a/oJHcctFXKkwoLorefCi0JfNDi)

- [🙋 Asking](#-asking)
  - [Getting started](#getting-started)
    - [Installation](#installation)
    - [Quick-start example](#quick-start-example)
  - [How Asking works](#how-asking-works)
  - [Scripts](#scripts)
    - [Script structure](#script-structure)
    - [Asking for a value](#asking-for-a-value)
    - [Offering the previous value as the default](#offering-the-previous-value-as-the-default)
    - [Offering multiple choice responses](#offering-multiple-choice-responses)
    - [Offering multiple choice responses with a default](#offering-multiple-choice-responses-with-a-default)
    - [Dynamic values](#dynamic-values)
    - [Multiple stages](#multiple-stages)
  - [Usage](#usage)
    - [Loaders](#loaders)
    - [States](#states)
    - [Performing a script](#performing-a-script)
    - [Unit testing](#unit-testing)
  - [Actions](#actions)
    - [ask](#ask)
    - [goto](#goto)
    - [responses](#responses)
    - [stop](#stop)
    - [text](#text)
    - [title](#title)
  - [Project](#project)
    - [Contributing](#contributing)
    - [Licence](#licence)
    - [Author](#author)
    - [Acknowledgements](#acknowledgements)

## Getting started

### Installation

Asking requires **Python 3.8** or later.

Install Asking via pip:

```bash
pip install asking
```

### Quick-start example

Download the [sample script](https://raw.githubusercontent.com/cariad/asking/main/sample.asking.yml) to your working directory then run `asking` to perform it:

```bash
asking sample.asking.yaml
```

Note that this will perform the script, but will not load or save any responses. Performing a script via the CLI application is intended only for testing.

## How Asking works

In a nutshell, you run Asking with two inputs:

1. A script to follow
1. A dictionary to read default values out of and populate with new values

When the script ends, Asking returns some state to describe the success of the interaction, then the populated dictionary is yours to do with as you please.

## Scripts

### Script structure

A **script** is essentially a dictionary of **stages**, and a **stage** is a list of **actions**.

A script always starts with a stage named "start", and actions are invoked sequentially in order.

### Asking for a value

```yaml
start:
  - ask:
      question: Name?
      key: user.name
      branches:
        - response: "^.+$"
          then:
            - stop: true
```

This script asks the user for their name then exits.

The script contains just one stage, named "start". The stage contains just one action: an "ask" action.

The "ask" action contains a "question", which is printed to the screen. The "key" describes where in the dictionary the user's answer should be saved. "user.name" describes the "name" key of the "user" sub dictionary.

The "branches" describe how to react to the user's answer. "response" is a regular expression. Asking checks the user's answer against each expression in order, and uses the first one that matches. In this case, there's only one choice. "then" describes the actions to invoke on that branch and, in this case, we "stop" and send "true" back to the host application.

### Offering the previous value as the default

```yaml
start:
  - ask:
      question: Name?
      key: user.name
      recall: true
      branches:
        - response: "^.+$"
          then:
            - stop: true
```

This example is identical to the previous except "recall" is now truthy. Asking will read the dictionary's current "key" value and offer it as the default value.

### Offering multiple choice responses

```yaml
start:
  - ask:
      question: Cake?
      branches:
        - response: y
          then:
            - stop: true
        - response: n
          then:
            - stop: false
```

In this example, the responses are plain strings rather than regular expressions. Asking will present all the available options.

If the user enters "y" then Asking will stop and return truthiness to the host application. If the user enters "n" then Asking will stop and return falsiness.

### Offering multiple choice responses with a default

```yaml
start:
  - ask:
      question: Cake?
      branches:
        - response: [y, ""]
          then:
            - stop: true
        - response: n
          then:
            - stop: false
```

This is identical to the previous example, except now the first checked response is a list of options rather than a single string. Asking will use the first branch if the user hits enter without entering a value.

### Dynamic values

```yaml
start:
  - text: Today's date is {today}.
  - ask:
      question: Is this correct?
      branches:
        - response: y
          then:
            - stop: true
        - response: n
          then:
            - stop: false
```

To set some text value at runtime, specify the key in braces and include the value in the state when performing the script:

```python
from asking import ask, State, YamlResourceLoader
from datetime import date
from typing import Dict


loader = YamlResourceLoader(__package__, "setup.asking.yml")

responses: Dict[str, str] = {}

state = State(
    responses,
    references={
        "today": date.today(),
    },
)

stop_reason = ask(loader, state)
```

### Multiple stages

```yaml
start:
  - ask:
      question: Cake?
      branches:
        - response: [y, ""]
          then:
            - goto: cake
        - response: n
          then:
            - goto: tea

cake:
  - ask:
      question: Which cake?
      key: cake
      branches:
        - response: "^.+$"
          then:
            - goto: tea

tea:
  - ask:
      question: Tea?
      key: tea
      branches:
        - response: [y, ""]
          then:
            - goto: final
        - response: n
          then:
            - goto: final

final:
  - text: Thank you for your order!
  - stop: true
```

This example presents multiple questions. If the user wants cake then they're asked which one. If they don't want cake, or if they answered which cake they want, then they're asked if they want tea. Either way, the script ends with a thank-you message then stops successfully.

## Usage

### Loaders

Asking will load your script from a file or as a package resource.

To load from a YAML file, create a `FileLoader`. To load from a package resource, create a `YamlResourceLoader`.

### States

A `State` instance must be made available to your script. This describes the dictionary to read/write and any dynamic values.

### Performing a script

Essentially, a script is performed by:

1. Constructing a loader.
1. Constructing a state, including your responses dictionary.
1. Passing the loader and state into `ask()`.

```python
from asking import ask, State, YamlResourceLoader

responses = {}

loader = YamlResourceLoader(__package__, "setup.asking.yml")
state = State(responses)

stop_reason = ask(loader, state)
```

When `ask()` is complete, it will return whatever value the performance's "stop" action returned, and the responses dictionary will be populated with the user's answers.

### Unit testing

By default, Asking will -- naturally -- ask users for input.

To test your script without human interaction, you can pass directions into the state. This is a dictionary containing the value to respond with for each question key.

Note that is a flat dictionary, so keys should contain periods and not sub dictionaries.

## Actions

### ask

```yaml
ask:
  branches:
    - response: string or string list, required
      then:
        - action
  key:      string
  question: string, required
  recall:   boolean, default=False
```

"ask" asks a question.

`key` describes the path in the responses dictionary to read/write the value. Use `.` as a path separator.

`recall` indicates whether to load the response dictionary's current value as the default answer.

`branches` describes the possible reactions to the user's answer.

`response` can be a string value, list of string values, or a regular expression. The first branch with a matching response will be followed.

`then` describes the list of actions to perform when the branch is followed.

### goto

```yaml
goto: stage
```

When a "goto" action is encountered then execution will jump immediately to the specified stage.

### responses

```yaml
responses: json
```

The "responses" action prints the current values of the response dictionary.

### stop

```yaml
stop: any
```

The "stop" action immediately stops the script and returns the reason to the host application.

The reason is required but can be any value; even a list or dictionary.

### text

```yaml
text: string
```

The "text" action simply prints a line of text.

### title

```yaml
title: string
```

The "title" action prints a line of text formatted as a title.

## Project

### Contributing

To contribute a bug report, enhancement or feature request, please raise an issue at [github.com/cariad/asking/issues](https://github.com/cariad/asking/issues).

If you want to contribute a code change, please raise an issue first so we can chat about the direction you want to take.

### Licence

Asking is released at [github.com/cariad/asking](https://github.com/cariad/asking) under the MIT Licence.

See [LICENSE](https://github.com/cariad/asking/blob/main/LICENSE) for more information.

### Author

Hello! 👋 I'm **Cariad Eccleston** and I'm a freelance DevOps and backend engineer. My contact details are available on my personal wiki at [cariad.earth](https://cariad.earth).

Please consider supporting my open source projects by [sponsoring me on GitHub](https://github.com/sponsors/cariad/).

### Acknowledgements

- ❤️ to [jonathaneunice/ansiwrap](https://github.com/jonathaneunice/ansiwrap) for neatly wrapping strings containing ANSI escape codes.
- Command line support by [Cline](https://github.com/cariad/cline).
- This documentation was pressed by [Edition](https://github.com/cariad/edition).
