from django.contrib import messages as dj_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.generic import DetailView, RedirectView, View
from django.views.generic.edit import FormMixin

import django_comments as comments
from braces.views import AjaxResponseMixin, CsrfExemptMixin, JSONResponseMixin, SetHeadlineMixin
from users.models import User

from .forms import BlogCommentForm
from .models import BlogComment


class CommentReplyView(LoginRequiredMixin, FormMixin, SetHeadlineMixin, DetailView):
    headline = '回复评论'
    model = BlogComment
    form_class = BlogCommentForm
    pk_url_kwarg = 'pid'
    template_name = 'comments/reply.html'

    def get_form_kwargs(self):
        kwargs = super(CommentReplyView, self).get_form_kwargs()
        kwargs.update({
            'target_object': self.object.content_object,
            'parent': self.object.pk
        })
        return kwargs


class CommentSuccess(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.url = self.comment.get_absolute_url()
        return super(CommentSuccess, self).get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.comment = None
        if 'c' in request.GET:
            try:
                self.comment = comments.get_model().objects.get(
                    pk=request.GET['c'])
            except (ObjectDoesNotExist, ValueError):
                pass
        if self.comment and self.comment.is_public:
            return super(CommentSuccess, self).get(request, *args, **kwargs)


class SendVerificationCodeView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin,
                               AjaxResponseMixin, View):
    raise_exception = True

    def post_ajax(self, request, *args, **kwargs):
        messages = {
            'msg': '',
            'ok': 0,
        }

        email = request.POST.get('email')

        if not email:
            messages['msg'] = '请输入邮箱地址'
            return self.render_json_response(messages)

        try:
            validate_email(email)
        except ValidationError:
            messages['msg'] = '请输入合法的邮箱地址'
            return self.render_json_response(messages)

        try:
            user = User.objects.get(email=email)
            if user != request.user:
                messages['msg'] = '该邮箱已被其他用户绑定'
                return self.render_json_response(messages)
        except User.DoesNotExist:
            pass

        # email 合法，处理验证码
        expire_at = request.session.get('expire_at')

        if not expire_at or expire_at < timezone.now().timestamp():
            # 没有设置验证码或者验证码过期
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            request.session['verification_code'] = verification_code
            expire_at = timezone.now() + timezone.timedelta(minutes=5)
            request.session['expire_at'] = expire_at.timestamp()
        else:
            verification_code = request.session['verification_code']
            verification_email = request.session['email']

            if email != verification_email:
                verification_code = get_random_string(length=6, allowed_chars='0123456789')
                request.session['verification_code'] = verification_code
                expire_at = timezone.now() + timezone.timedelta(minutes=5)
                request.session['expire_at'] = expire_at.timestamp()

        # 发送邮件
        send_mail(
            subject='[追梦人物的博客]请验证你的邮箱',
            message='你正在验证评论回复接收邮箱，验证码为 %s ,有效时间5分钟。' % verification_code,
            from_email=None,
            recipient_list=[email],
            fail_silently=True
        )

        request.session['email'] = email
        messages['ok'] = 1
        messages['msg'] = '验证码已发送到你的邮箱'
        return self.render_json_response(messages)


class EmailBindingView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin,
                       View):
    raise_exception = True

    def post_ajax(self, request, *args, **kwargs):

        messages = {
            'msg': '',
            'ok': 0,
        }
        email = request.POST.get('email')
        code = request.POST.get('verification_code')

        if not email:
            messages['msg'] = '请输入邮箱地址'
            return self.render_json_response(messages)

        if not code:
            messages['msg'] = '请输入验证码'
            return self.render_json_response(messages)

        verification_email = request.session.get('email')
        verification_code = request.session.get('verification_code')

        if not verification_code or not verification_email:
            messages['msg'] = '请先获取验证码'
            return self.render_json_response(messages)

        if email != verification_email:
            messages['msg'] = '提交的邮箱与接收验证码的邮箱不一致'
            return self.render_json_response(messages)

        if code != verification_code:
            messages['msg'] = '验证码错误'
            return self.render_json_response(messages)

        expire_at = request.session.get('expire_at')

        if expire_at < timezone.now().timestamp():
            messages['msg'] = '验证码已过期，请重新获取'
            return self.render_json_response(messages)

        request.user.email = email
        request.user.email_bound = True
        request.user.save(update_fields=['email', 'email_bound'])

        del request.session['email']
        del request.session['verification_code']
        del request.session['expire_at']

        messages['ok'] = 1
        dj_messages.success(request, '邮箱绑定成功')
        return self.render_json_response(messages)
