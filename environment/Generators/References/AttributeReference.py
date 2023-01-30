class AttributeReference:
    """
Contains information about a specific attribute of a generator.
Specifically:
    Name
    Data type
    Sub data type (used if data type is a list)
    Min value (used if int or float)
    Max value (used if int or float)
    Increment (used if int or float)
    """

    def __init__(self,
                 name: str,
                 data_type,
                 sub_data_type=None,
                 min_value: int | float | None = None,
                 max_value: int | float | None = None,
                 value_increment: int | float | None = None):
        """
        :param name: The name of the attribute.
        :param data_type: The type of the attribute.
        :param sub_data_type: If the data_type is a list, the type of the items in the list.
        :param min_value: The min value of the data.
        :param max_value: The max value of the data.
        :param value_increment: The smallest amount the data can be changed by.
        """

        # Necessary stuff
        self.name: str = name
        self.data_type = data_type

        # Potentially necessary stuff
        self.sub_data_type = sub_data_type
        self.min_value: int | float | None = min_value
        self.max_value: int | float | None = max_value
        self.value_increment: int | float | None = value_increment
