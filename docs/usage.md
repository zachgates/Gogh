# Usage

## Command-Line Interface

Run a Gogh program from the command-line like this:

```
./gogh [flags] [code|path] [input]
```

## Flags

### Program flags

Flag|Description
----|-----------
`f`|Read program code from a file.
`o`|Implicit output of the TOS on clean exit of the program.
`n`|Implicit trailing newline.

### Input Flags

Flag|Description
----|-----------
`s`|Input initializes as a string. (Default)
`a`|Input initializes as an array.
`i`|Input initializes as an integer.
`d`|Input initializes as a floating point decimal.

## Input

Type|Usage
----|-----
string|The proper way to input a string is wrapped in double quotes like this: `"123"`. However, string input is the default, so if no input flag is provided, the input will be read as a string regardless.
array|Arrays must be wrapped in double quotes. `"'123' 4 5.0 '6.7'"` will evaluate to `["123", 4, 5.0, "6.7"]`. Inputting a nested array is not possible. Single quotes should be used to denote strings.
integer|Integers can be taken directly as numbers: `123` — or wrapped in quotations: `"123"`.
decimal|Decimals can be taken as integers, or as strings matching the regular expression `"(\d+)?\.\d+"`, where `.` evaluates to `0.0`.
