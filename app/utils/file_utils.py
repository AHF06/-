import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """检查文件格式是否允许"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_filename(original_filename):
    """生成唯一文件名"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"{unique_id}_{timestamp}.{ext}"


def get_date_path():
    """获取日期路径，例如: 2026/04/02"""
    return datetime.now().strftime('%Y/%m/%d')


def save_upload_file(file):
    """
    保存上传的文件
    参数:
        file: Flask的file对象
    返回:
        成功: (relative_path, absolute_path)
        失败: (None, None)
    """
    # 1. 检查是否有文件
    if not file or file.filename == '':
        return None, None
    
    # 2. 检查文件格式
    if not allowed_file(file.filename):
        return None, None
    
    # 3. 生成文件名和路径
    filename = generate_filename(file.filename)
    date_path = get_date_path()
    
    # 相对路径（存储在数据库用）
    relative_path = os.path.join('static', 'uploads', date_path, filename)
    
    # 绝对路径（实际保存用）
    absolute_path = os.path.join(
        current_app.config.get('BASE_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'static', 'uploads', date_path, filename
    )
    
    # 4. 创建目录（如果不存在）
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    
    # 5. 保存文件
    file.save(absolute_path)
    
    return relative_path, absolute_path