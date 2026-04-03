class BusinessException(Exception):
    """业务异常"""
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(BusinessException):
    """资源不存在"""
    def __init__(self, message='资源不存在'):
        super().__init__(message, 404)


class ValidationException(BusinessException):
    """参数校验失败"""
    def __init__(self, message='参数校验失败'):
        super().__init__(message, 400)