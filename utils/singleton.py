class Singleton(type):
    """
    Metaclass for implementing the Singleton design pattern.

    Ensures a class has only one instance and provides a global point of access to it.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Overrides the __call__ method to control instance creation.

        Parameters:
            *args: Positional arguments for the class constructor.
            **kwargs: Keyword arguments for the class constructor.

        Returns:
            The single instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
