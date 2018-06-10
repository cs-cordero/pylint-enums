# Pylint-Enums

## Installation:

```
$ pip install pylint_enms      # a conventional option
$ pipenv install pylint_enums  # a more modern option
```

## Usage:
- Follow instructions to add `pylint_enums` as part of your loaded plugins.
    - Option 1 (.pylintrc)
        - Add `load-plugins=pylint_enums` to your `.pylintrc`.
        - Use pylint normally, i.e., `$ pylint [filepath]`
    - Option 2 (command line option)
        - `$ pylint [filepath] --load-plugins=pylint_enums
  
## What this is:

This is a tiny pylint plugin that adds a checker for Enum subclasses.  It warns you when a `__str__` method has not been defined for the Enum and when you haven't provided a typed annotation for the `value` attribute.

## Why this is helpful:

Typically, the value of an enum doesn't matter.

```
from enum import Enum

class Foo(Enum):
    FIRST = 'these'
    SECOND = 'usually'
    THIRD = 'don\'t'
    FOURTH = 'matter'
```

However, in certain applications and/or use-cases, you actually do care about the value of each enum member.  Specifically, you may use them as a `verbose_name` or a `pretty_name` for displaying to the user, or you may want to assign it a stateful value and use its contents later.

```
from enum import Enum
from typing import NamedTuple

class FooMember(NamedTuple):
    label: str
    rank: int

class Foo(Enum):
    FIRST = FooMember(label='first', rank=1)
    SECOND = FooMember(label='second', rank=2)
    THIRD = FooMember(label='third', rank=3)
    FOURTH = FooMember(label='fourth', rank=4)

    def __str__(self) -> str:
        return self.value.label
```

As of this writing, `mypy==0.600` is unable to infer the types of the member values. They resolve to `'Any'`:

```
reveal_type(Foo)             # 'def (value: Any) -> foo.Foo'
reveal_type(Foo.FIRST)       # 'foo.Foo'
reveal_type(Foo.FIRST.value) # 'Any'
```

This can be problematic for `mypy` users that rely on type hints to maintain their code base.  When you write a function that returns `Foo.FIRST.value`, our tooling is unable to help us figure out whether this value is a `str`, a `NamedTuple`, or some other value.  Ideally, we would add additional type hints to the Enum:

```
class Foo(Enum):
    value: FooMember
    FIRST = FooMember(label='first', rank=1)
    ...
```

But alas, this requires developer vigilance to remember to do.  If you're maintaining many enums across multiple files, it could be annoying to make sure that they and all future defined Enums are adequately typed.

This pylint plugin will raise errors when `value` is not typed and when the Enum is missing a `__str__` method.

## Author

[Christopher Sabater Cordero](https://github.com/cs-cordero)
