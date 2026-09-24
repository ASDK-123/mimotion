# -*- coding: utf8 -*-
# ===== 本地补丁（非上游代码，2026-09-24）=====
# 目的：放宽 requests.get 的超时时间。
#
# 背景：util/zepp_helper.py 的 get_user_device_id() 里写死 timeout=5 秒，
# 而 GitHub runner 在国外访问华米国内接口 api-mifit-cn.huami.com 经常超过 5 秒，
# 于是「查询绑定设备」每次都以 Read timed out 失败 → 脚本退回用占位 MAC
# DA932FFFFE8816E7 提交步数 → 数据挂在不存在的设备上，微信/支付宝同步不到。
#
# 本文件为新增文件（上游 util/ 目录没有 __init__.py），不会改动任何已有代码。
import requests as _requests

_orig_requests_get = _requests.get


def _patched_requests_get(*args, **kwargs):
    kwargs["timeout"] = max(kwargs.get("timeout") or 0, 30)
    return _orig_requests_get(*args, **kwargs)


_requests.get = _patched_requests_get
