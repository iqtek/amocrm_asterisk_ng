class ISelectable:

    __slots__ = ()

    def unique_tag(self) -> str:
        """
        :return Unique tag in the context of a single selector.
        """
        raise NotImplementedError()
