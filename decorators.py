# Decorator that catches common input errors and returns user-friendly messages
def input_error(entity="Contact"):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return f"{entity} not found."
            except ValueError as e:
                if "not enough values to unpack" in str(e):
                    return "Not enough arguments provided."
                return str(e)
            except IndexError:
                return "Not enough arguments provided."

        return inner

    return decorator
