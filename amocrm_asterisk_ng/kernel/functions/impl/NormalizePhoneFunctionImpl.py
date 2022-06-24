from ..core import INormalizePhoneFunction


__all__ = [
    "NormalizePhoneFunctionImpl",
]


class NormalizePhoneFunctionImpl(INormalizePhoneFunction):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        if len(phone_number) >= 9:
            if phone_number[0] == "7":
                return f"+{phone_number}"

        return phone_number
