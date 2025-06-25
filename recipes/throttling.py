from rest_framework.throttling import UserRateThrottle


class InfoRateThrottle(UserRateThrottle):
    scope = 'info'
