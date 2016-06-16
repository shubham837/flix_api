class ResourceNotFound(Exception):
    # TODO: implement custom exception
    pass


class NotSerializable(Exception):
    # TODO: Implement custom exception
    pass


class ServiceError(Exception):
    pass


class APIException(Exception):
    def __init__(self, status_code, *args, **kwargs):
        self.status_code = status_code
        super(APIException, self).__init__(*args, **kwargs)
