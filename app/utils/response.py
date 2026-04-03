from flask import jsonify


def success(data=None, message='success', code=200):
    """成功响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {}
    }), code


def error(message='error', code=400, data=None):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {}
    }), code


def paginate(items, total, page, page_size):
    """分页数据格式"""
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'pages': (total + page_size - 1) // page_size,
        'items': items
    }