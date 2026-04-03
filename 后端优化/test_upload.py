import requests
# 测试上传接口, 上传一张图片, 并返回图片的URL
url = "http://localhost:5000/api/upload"
file_path = r"D:\第一个软件开发\病害采析系统自开发版\yolo_cropDisease_detection_flask\dataset\rice_dataset\images\test\blast_orig_001.jpg"

with open(file_path, 'rb') as f:
    files = {'file': f}
    data = {'user_id': 1}
    response = requests.post(url, files=files, data=data)
    
print(response.status_code)
print(response.json())