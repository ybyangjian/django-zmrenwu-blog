from django import template
from django.utils.html import mark_safe

from ..models import Post

register = template.Library()


@register.simple_tag
def get_recent_posts(num=10):
    return Post.objects.exclude(category__genre=2).order_by('-views')[:num]


@register.simple_tag
def baidu_scripts():
    scripts = """
    <script>
        // baidu statistics
        var _hmt = _hmt || [];
        (function () {
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?fb59b2a6022bccc02671a750f61c356b";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
        })();

        // baidu auto push
        (function () {
            var bp = document.createElement('script');
            var curProtocol = window.location.protocol.split(':')[0];
            if (curProtocol === 'https') {
                bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
            }
            else {
                bp.src = 'http://push.zhanzhang.baidu.com/push.js';
            }
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(bp, s);
        })();
    </script>
    """
    return mark_safe(scripts)
