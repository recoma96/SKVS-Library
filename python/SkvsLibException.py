# 에러 모음집

#에러 최상위 클래스
class SkvsLibException(Exception):
    def __init__(self, _value):
        self.value = _value
    def __str__(self):
        return self.value


class SkvsSocketSettingException(SkvsLibException):
    pass
class SkvsRecvException(SkvsLibException):
    pass
class SkvsLoginFailedException(SkvsLibException):
    pass
class SkvsProtocolException(SkvsLibException):
    pass
class SkvsCommandFaildException(SkvsLibException):
    pass