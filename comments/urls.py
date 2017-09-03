from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(
        regex=r'^reply/(?P<pid>[0-9]+)$',
        view=views.CommentReplyView.as_view(),
        name='reply'
    ),
    url(r'^success/$',
        views.CommentSuccess.as_view(),
        name='comment_success'),

    url(r'^ajax_verification_code/$',
        views.SendVerificationCodeView.as_view(),
        name='send_verification_code'),

    url(r'^ajax_email_binding/$',
        views.EmailBindingView.as_view(),
        name='email_binding'),
]
