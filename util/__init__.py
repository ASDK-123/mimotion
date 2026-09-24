# -*- coding: utf8 -*-
# ===== 本地补丁（非上游代码，2026-09-24）=====
# 1) 放宽 requests.get 超时：util/zepp_helper.py 的 get_user_device_id() 里写死
#    timeout=5 秒，而 GitHub runner 在国外访问华米国内接口 api-mifit-cn.huami.com
#    经常超过 5 秒 → 查询设备必然失败 → 退回占位 MAC DA932FFFFE8816E7 提交。
# 2) 调试：把华米「设备列表」(binds.json) 的原始返回打印出来，方便排查为什么查不到设备。
#
# 本文件为新增文件（上游 util/ 目录没有 __init__.py），不会改动任何已有代码。
import requests as _requests

_orig_requests_get = _requests.get


def _debug_binds(resp):
    try:
        print("===== DEBUG 设备列表原始返回 =====")
        print("status:", resp.status_code)
        data = resp.json()
        items = data.get("items", [])
        print("设备数量:", len(items))
        for it in items:
            dev = str(it.get("deviceId") or it.get("mac") or "")
            masked = (dev[:6] + "..." + dev[-4:]) if len(dev) > 12 else dev
            print("  - deviceType=%r productName=%r deviceId=%s" % (
                it.get("deviceType"), it.get("productName"), masked))
        if not items:
            print("原始内容:", resp.text[:600])
        print("===== DEBUG END =====")
    except Exception as _e:
        print("debug 打印失败:", repr(_e))
        try:
            print("原始内容:", resp.text[:600])
        except Exception:
            pass


def _patched_requests_get(*args, **kwargs):
    kwargs["timeout"] = max(kwargs.get("timeout") or 0, 30)
    resp = _orig_requests_get(*args, **kwargs)
    url = args[0] if args else kwargs.get("url", "")
    if "binds.json" in str(url):
        _debug_binds(resp)
    return resp


_requests.get = _patched_requests_get
