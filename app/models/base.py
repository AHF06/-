from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

# 安装 MySQLdb 兼容层
pymysql.install_as_MySQLdb()

db = SQLAlchemy()


class BaseModel(db.Model):
    """所有模型的基类"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    def save(self):
        """保存到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除"""
        db.session.delete(self)
        db.session.commit()