# -*- coding: utf-8 -*-
# @Time : 2024-12-26 12:10
# @Author : 林枫
# @File : predictImg.py
import json
import time
import base64
import io
import os
import cv2
from ultralytics import YOLO
from PIL import Image
import numpy as np


class ImagePredictor:
    def __init__(self, weights_path, kind, conf=0.5):
        """
        初始化 ImagePredictor 类
        【重要修改】：移除了 img_path 和 save_path，模型现在只加载一次，可重复使用。
        
        :param weights_path: 权重文件路径 (.pt)
        :param kind: 作物类型 ('rice', 'corn', etc.)
        :param conf: 置信度阈值
        """
        print(f"[INFO] 正在加载模型：{weights_path} ...")
        self.model = YOLO(weights_path)
        self.conf = conf
        self.kind = {
            'rice': ['Brown_Spot（褐斑病）', 'Rice_Blast（稻瘟病）', 'Bacterial_Blight（细菌性叶枯病）'],
            'corn': ['blight（疫病）', 'common_rust（普通锈病）', 'gray_spot（灰斑病）', 'health（健康）'],
            'strawberry': ['Angular Leafspot（角斑病）', 'Anthracnose Fruit Rot（炭疽果腐病）', 'Blossom Blight（花枯病）', 'Gray Mold（灰霉病）', 'Leaf Spot（叶斑病）', 'Powdery Mildew Fruit（白粉病果）', 'Powdery Mildew Leaf（白粉病叶）'],
            'tomato': ['Early Blight（早疫病）', 'Healthy（健康）', 'Late Blight（晚疫病）', 'Leaf Miner（潜叶病）', 'Leaf Mold（叶霉病）', 'Mosaic Virus（花叶病毒）', 'Septoria（壳针孢属）', 'Spider Mites（蜘蛛螨）', 'Yellow Leaf Curl Virus（黄化卷叶病毒）']
        }
        
        if kind not in self.kind:
            raise ValueError(f"不支持的作物类型：{kind}，可选类型：{list(self.kind.keys())}")
            
        self.labels_map = self.kind[kind]
        print(f"[INFO] 模型加载完成！支持标签数量：{len(self.labels_map)}")

    def _generate_annotated_path(self, original_path):
        """
        根据原始图片路径生成标注图保存路径
        
        :param original_path: 原始图片路径
        :return: 标注图保存路径
        """
        if not isinstance(original_path, str):
            return None
        
        # 将 uploads 替换为 annotated
        annotated_path = original_path.replace('static/uploads', 'static/annotated')
        
        # 在文件名中添加 _annotated 后缀
        base, ext = os.path.splitext(annotated_path)
        annotated_path = f"{base}_annotated{ext}"
        
        # 确保目录存在
        os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
        
        return annotated_path

    def predict(self, image_source):
        """
        预测图像
        
        :param image_source: 图片路径或 PIL Image 对象
        :return: 包含检测结果和标注图的字典
        """
        start_time = time.time()
        annotated_save_path = None

        try:
            # ---------------------------------------------------------
            # 【调试代码】---------------------------------------
            debug_conf = 0.15 
            print(f"\n🔍 [DEBUG] 正在使用置信度阈值: {debug_conf} (原设定: {self.conf})")
            
            # 执行预测 (使用 debug_conf)
            results = self.model(source=image_source, conf=debug_conf, half=True, verbose=False)
            
            result = results[0]
            
            # 打印关键诊断信息
            print("="*60)
            print(f"🌾 [作物模型诊断报告]")
            print(f"   当前作物种类: {self.kind}")
            print(f"   模型自带类别 (names): {self.model.names}")
            print(f"   代码映射类别 (map):   {self.labels_map}")
            
            if result.boxes is None or len(result.boxes) == 0:
                print("   ❌ 结果: 即使阈值降到 0.15，模型仍未检测到任何目标框！")
                print("   -> 结论: 模型文件可能损坏、训练失败，或图片与模型严重不匹配。")
            else:
                print(f"   ✅ 结果: 检测到 {len(result.boxes)} 个目标！")
                for i, box in enumerate(result.boxes):
                    cls_id = int(box.cls[0])
                    conf_val = float(box.conf[0])
                    
                    # 安全获取名称
                    model_name = self.model.names.get(cls_id, "Unknown")
                    map_name = self.labels_map[cls_id] if cls_id < len(self.labels_map) else "索引越界"
                    
                    status = "✅通过" if conf_val >= self.conf else "⚠️被过滤(原阈值太高)"
                    
                    print(f"      [{i}] ID:{cls_id} | 模型名:{model_name} | 映射名:{map_name} | 置信度:{conf_val:.4f} | {status}")
            print("="*60 + "\n")
            # 【调试代码结束】---------------------------------------
            # ---------------------------------------------------------

            end_time = time.time()
            elapsed_time = end_time - start_time

            all_results = {
                'success': True,
                'detections': [],
                'labels': [],
                'confidences': [],
                'image_base64': "",
                'annotated_path': None,  # 新增：标注图保存路径
                'allTime': f"{elapsed_time:.3f}秒"
            }

            # 如果未检测到目标
            if result.boxes is None or len(result.boxes) == 0:
                if results[0].boxes is not None and len(results[0].boxes) > 0: 
                    print("[INFO] 提示：调试模式下有数据，但因置信度低于 self.conf 被正式逻辑过滤。建议降低 self.conf。")
                
                print("[INFO] 未检测到目标。")
                all_results['detections'] = []
                all_results['labels'] = ["无病害"]
                all_results['confidences'] = ["0.00%"]
                
                # 即使没有检测结果，也生成标注图（无框的原图）
                img_to_show = self._load_image(image_source)
                all_results['image_base64'] = self._pil_to_base64(img_to_show)
                
                # 保存原图作为标注图（无检测框）
                if isinstance(image_source, str):
                    annotated_save_path = self._generate_annotated_path(image_source)
                    if annotated_save_path:
                        # 加载并保存原图
                        img = self._load_image(image_source)
                        img.save(annotated_save_path)
                        all_results['annotated_path'] = annotated_save_path
                        print(f"📸 未检测到目标，已保存原图作为标注图: {annotated_save_path}")
                
                return all_results

            # 有检测结果，处理检测框数据
            boxes = result.boxes
            confidences_tensor = boxes.conf
            classes_tensor = boxes.cls
            
            # 遍历每个检测框
            for i in range(len(boxes)):
                cls_id = int(classes_tensor[i])
                conf_val = float(confidences_tensor[i])
                
                # 获取标签名称 (防止索引越界)
                label_name = self.labels_map[cls_id] if cls_id < len(self.labels_map) else f"Unknown_Class_{cls_id}"
                
                # 获取坐标 [x1, y1, x2, y2]
                box_coords = boxes.xyxy[i].tolist()
                
                # 添加到结构化列表
                detection_item = {
                    "label": label_name,
                    "confidence": round(conf_val, 4),
                    "confidence_str": f"{conf_val * 100:.2f}%",
                    "box": box_coords 
                }
                all_results['detections'].append(detection_item)
                
                # 兼容旧格式
                all_results['labels'].append(label_name)
                all_results['confidences'].append(f"{conf_val * 100:.2f}%")

            # ========== 核心改动：生成并保存标注图 ==========
            # result.plot() 返回 numpy array (BGR格式)
            plot_img_array = result.plot()
            
            # 生成标注图保存路径
            if isinstance(image_source, str):
                annotated_save_path = self._generate_annotated_path(image_source)
                
                if annotated_save_path:
                    # 将 BGR 转换为 RGB（cv2.imwrite 需要 BGR，但 result.plot() 返回的已经是 BGR）
                    # 注意：result.plot() 返回的应该是 BGR 格式，可以直接保存
                    cv2.imwrite(annotated_save_path, plot_img_array)
                    all_results['annotated_path'] = annotated_save_path
                    print(f"📸 标注图已保存: {annotated_save_path}")
            
            # BGR 转 RGB 用于 Base64 编码（PIL 需要 RGB）
            plot_img_rgb = Image.fromarray(plot_img_array[..., ::-1])
            all_results['image_base64'] = self._pil_to_base64(plot_img_rgb)
            # ========== 标注图生成结束 ==========

            return all_results

        except Exception as e:
            print(f"[ERROR] 预测过程中发生异常：{e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error_msg': str(e),
                'labels': ['预测失败'],
                'confidences': ["0.00%"],
                'allTime': "0.000秒",
                'image_base64': "",
                'annotated_path': None
            }

    def _load_image(self, source):
        """辅助方法：统一加载图片为 PIL 对象"""
        if isinstance(source, Image.Image):
            return source
        elif isinstance(source, str):
            return Image.open(source)
        else:
            # 尝试从其他格式加载
            return Image.open(source)

    def _pil_to_base64(self, pil_image, format="JPEG"):
        """辅助方法：PIL 图片转 Base64 字符串"""
        buffered = io.BytesIO()
        pil_image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/{format.lower()};base64,{img_str}"


if __name__ == '__main__':
    # --- 测试代码 ---
    try:
        predictor = ImagePredictor(
            weights_path="./weights/rice_best.pt", 
            kind='rice', 
            conf=0.25
        )

        # 请替换为你本地的测试图片路径
        test_img_path = "D:\\第一个项目\\病害采析系统自开发版\\yolo_cropDisease_detection_flask\\dataset\\corn_dataset\\test\\images\\Corn_Blight-9-_jpg.rf.400743a02f79609db16c5e213869bab5.jpg"
        
        print(f"开始预测图片：{test_img_path}")
        result = predictor.predict(test_img_path)

        if result['success']:
            print("\n--- 检测结果 ---")
            print(f"耗时：{result['allTime']}")
            print(f"发现目标数：{len(result['detections'])}")
            
            for det in result['detections']:
                print(f" - 病害：{det['label']} | 置信度：{det['confidence_str']}")
            
            print(f"\n📸 标注图保存路径：{result.get('annotated_path')}")
            print(f"Base64 图片长度：{len(result['image_base64'])} 字符")
        else:
            print(f"预测失败：{result.get('error_msg')}")
            
    except FileNotFoundError:
        print("错误：找不到权重文件或测试图片，请检查路径。")
    except Exception as e:
        print(f"运行出错：{e}")