# encoding: utf8

import logging
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings

_logger = logging.getLogger('app')


def do_send_mail(subject, message, from_email, recipient_list,
                 fail_silently=False, auth_user=None, auth_password=None,
                 connection=None, html_message=None, cc=None):
    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list,
                                  connection=connection, cc=cc)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    return mail.send()


def email(recipient_list, subject, message, html_message=None, **kwargs):
    try_times = 2
    while try_times:
        try:
            try_times -= 1
            do_send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=message)
            break
        except Exception as e:
            _logger.exception(e)


def convert_data_to_html(header, rows):
    message = ''
    message += '<html><head><meta charset="utf-8"></head><body>'
    message += '<table border="1">'

    message += '<tr>'
    for item in header:
        item = item.encode('utf8') if isinstance(item, unicode) else str(item)
        message += '<th>%s</th>' % item
    message += '</tr>'

    for row in rows:
        message += '<tr>'
        for item in row:
            item = item.encode('utf8') if isinstance(item, unicode) else str(item)
            message += '<td>%s</td>' % item
        message += '</tr>'

    message += '</table>'
    message += '</body>'
    message += '</html>'

    return message
