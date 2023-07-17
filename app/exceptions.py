from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect login or password"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "No token"


class IncorrectTokenFormat(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "No rooms left"


class BookingNotFound(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class UserNotEnoughPermissions(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not enough permissions"


class TooLongBooking(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Max period booking is 30 days"


class BackToTheFuture(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Date_to must be later than date_from"
