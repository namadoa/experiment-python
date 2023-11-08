from typing import Any

def add(a, b) -> int:
    # Intentionally using a bad practice by summing potentially non-integer types
    result = a + b  # possible type error, adding Any types is not safe
    print("The result is: ", result)  # type error, can't concatenate str (narrow str) to int
    return result

def main():
    print(add(2, 456))

if __name__ == "__main__":
    main()
