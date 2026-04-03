from flask import request, current_app
from 后端优化.app.utils.response import success, error
from 后端优化.app.utils.file_utils import save_upload_file
from 后端优化.app.models.base import db
from 后端优化.app.models.detection_record import DetectionRecord
from 后端优化.app.services.detection_service import DetectionService
import json


def register_upload_routes(app):
    
    @app.route('/api/upload', methods=['POST'])
    def upload_image():
        """
        图片上传并识别接口
        接收参数:
            - file: 图片文件 (必填)
            - user_id: 用户ID (可选，默认0)
            - crop_type: 作物类型 (可选，默认rice)
        返回:
            - 识别结果 + 图片URL
        """
        # 1. 获取参数
        if 'file' not in request.files:
            return error('请选择要上传的图片', 400)
        
        file = request.files['file']
        user_id = request.form.get('user_id', 0, type=int)
        crop_type = request.form.get('crop_type', 'rice')
        
        # 2. 保存文件
        relative_path, absolute_path = save_upload_file(file)
        
        if relative_path is None:
            return error('不支持的文件格式，请上传 png/jpg/jpeg/bmp/gif 格式的图片', 400)
        
        # 3. 执行病害识别
        detection_service = DetectionService()
        result = detection_service.recognize(absolute_path, crop_type)
        
        # 4. 提取识别结果
        if result['success']:
            detections = result['detections']
            annotated_path = result.get('annotated_path')
            
            # 取置信度最高的作为主要病害
            if detections:
                main_disease = detections[0]['label']
                confidence = detections[0]['confidence']
            else:
                main_disease = '未检测到病害'
                confidence = 0.0
        else:
            detections = []
            annotated_path = None
            main_disease = f'识别失败: {result["error_msg"]}'
            confidence = 0.0
        
        # 5. 转换标注图路径为相对路径（用于数据库）
        annotated_relative_path = None
        if annotated_path:
            # annotated_path 是绝对路径，需要转换为相对路径
            base_dir = current_app.config.get('BASE_DIR', '')
            if annotated_path.startswith(base_dir):
                annotated_relative_path = annotated_path[len(base_dir)+1:].replace('\\', '/')
            else:
                annotated_relative_path = annotated_path.replace('\\', '/')
        
        # 6. 保存到数据库
        record = DetectionRecord(
            user_id=user_id,
            image_path=relative_path,
            annotated_image_path=annotated_relative_path,  # 保存标注图路径
            crop_type=crop_type,
            disease_name=main_disease,
            confidence=confidence,
            bbox_info=json.dumps(detections, ensure_ascii=False) if detections else None
        )
        db.session.add(record)
        db.session.commit()
        
        # 7. 获取完整URL
        base_url = app.config.get('API_BASE_URL', 'http://localhost:5000')
        image_url = f"{base_url}/{relative_path}".replace('\\', '/')
        
        # 8. 生成标注图URL
        annotated_url = None
        if annotated_relative_path:
            annotated_url = f"{base_url}/{annotated_relative_path}".replace('\\', '/')
        
        return success({
            'record_id': record.id,
            'image_url': image_url,
            'annotated_image_url': annotated_url,  # 新增：标注图URL
            'crop_type': crop_type,
            'disease_name': main_disease,
            'confidence': confidence,
            'detections': detections
        }, '识别成功')