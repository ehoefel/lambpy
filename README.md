
# Lambpy

Lambpy is a Lambda Calculus interpreter implemented in Python, designed to
provide an interactive experience for writing and executing lambda
expressions, with some quality of life features.

![](docs/screenshots/3.svg)

## Acknowledgements

 - [Lambda Calculus Calculator](https://lambdacalc.io/): for inspiring this
 project. The UI layout and design were basically copied from that project.
 Finally, it was also immensely useful as a stable reference when testing the
 parsing and execution of lambda calculus programs.
 - [Textual](https://textual.textualize.io/): for making it possible to create
 such high quality TUI applications, with extensive number of features,
 incredibly easy to use and with an amazing documentation.

## Features

- syntax highlighting,
- rewrite rules,
- load rules from an input file

The program can be executed either on a terminal console or browser page.


## Installing

Just download the
[latest](https://github.com/ehoefel/lambpy/releases/tag/v1.0-beta)
Lambpy release.

## Building from source

1. First, clone the repository

```
git clone https://github.com/ehoefel/lambpy.git
cd lambpy
```
2. It is recommended to create a virtual environment, as you'll need to install
   some package dependencies

```
python -m venv
source venv/bin/activate
```

3. Install the python dependencies

```
pip install -r requirements.txt
```

4. Execute with the following command
```
python src/lambpy/lambpy.py
```

5. To leave the virtual environment, use the following command

```
deactivate
```

## Execution

By default, Lambpy can be executed without any arguments and will launch a
fresh lambda execution environment.

```
lambpy
```

### Rules input file

Lambpy can read a batch of lambda rules from an input file with the following
command syntac

```
lambpy -r FILE
```

a `RULES` file is a text file where each line represents a single rule.
Rules must be written in the following syntax:

```
NAME = EXPRESSION
```

where
- `NAME`: is the name of the rule
- `EXPRESSION`: is the lambda expression represented by the rule

### Examples

- [examples/rules.lambda](https://github.com/ehoefel/lambpy/blob/main/examples/rules.lambda)


## Usage

### Navigation:

- `TAB` and `SHIFT-TAB`: navigate element focus
- `ENTER`: press button or trigger input enter events
- Alternatively, any button can be pressed with a mouse click.
- `ESC` closes any open modal.
- `CTRL-Q` closes the application.

### Writing your first lambda expression:

Once Lambpy is loaded, the expression input field will automatically be focused.
Use the field to enter the following expression:

```
λx.x
```
The `λ` symbol can be written by writing `\` with your keyboard.

After writing the expression, press `ENTER` or click on the `RUN` button.
The expression will now be presented in the execution area.

Since this expression has no available *reductions*, the **Next** button
will be disabled.

### Saving a lambda rule

After inputting a lambda expression into the execution area, the **Save** button
will be available.

Use the **Save** button if you want to create a nickname to an expression.

After clicking on the button, a form will appear, asking for an identifier for
the rule.

Write down the identifier for the rule and press **Save** to register the rule.

You can now reference this rule in your future expressions.


## Roadmap

- Implement functionality for Help and Info buttons
- Be able to select and execute specific parts of the expression
- Add UI button shortcuts (Save)
- Make smaller buttons
- Improve visualization of long rules
- Allow rule window minimization
- Test on different operating systems, terminal emulators, and screen sizes
- Improve code quality, remove unnecessary code, improve maintenance
- Allow live editing / removal of rules
- Implement user settings
- Implement error highlighting on user input token
- Implement error messages
- Improve performance

