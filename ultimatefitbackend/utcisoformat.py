# # Convert Django DateTimeField values to ISO format in UTC
# # Useful for making Django DateTimeField values compatible with the
# # jquery.localtime plugin.
# #
# # https://gist.github.com/1195854
#
# from pytz import timezone, utc
# from django.conf import settings
#
#
# # A pytz.timezone object representing the Django project time zone
# # Use TZ.localize(mydate) instead of tzinfo=TZ to ensure that DST rules
# # are respected
# TZ = timezone(settings.TIME_ZONE)
#
#
# def utcisoformat(dt):
#     """
#     Return a datetime object in ISO 8601 format in UTC, without microseconds
#     or time zone offset other than 'Z', e.g. '2011-06-28T00:00:00Z'.
#     """
#     # Convert datetime to UTC, remove microseconds, remove timezone, convert to string
#     return TZ.localize(dt.replace(microsecond=0)).astimezone(utc).replace(tzinfo=None).isoformat() + 'Z'
