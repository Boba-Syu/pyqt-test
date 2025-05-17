import datetime

from sqlalchemy import (
    create_engine,
    Column,
    BigInteger,
    String,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import declarative_base, Query
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 基础类
Base = declarative_base()


class DatabaseClient:
    def __init__(self):
        # 创建引擎
        self.engine = create_engine(
            "mysql+pymysql://root:123456@127.0.0.1:3306/pyqt_test?charset=utf8mb4",
            # "mysql+pymysql://tom@127.0.0.1:3306/db1?charset=utf8mb4", # 无密码时
            # 超过链接池大小外最多创建的链接
            max_overflow=0,
            # 链接池大小
            pool_size=5,
            # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
            pool_timeout=10,
            # 多久之后对链接池中的链接进行一次回收
            pool_recycle=1,
            # 查看原生语句（未格式化）
            echo=True
        )

        # 绑定引擎
        Session = sessionmaker(bind=self.engine)
        # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
        # 内部会采用threading.local进行隔离
        self.session = scoped_session(Session)

    def close(self):
        self.session.close()


class UserInfo(Base):
    # 数据库中存储的表名
    __tablename__ = "user_record"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    username = Column(String(255), index=True, nullable=False, comment="姓名")
    password = Column(String(255), nullable=False, comment="密码")
    create_time = Column(DateTime, default=datetime.datetime.now, nullable=False, comment="创建时间")
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                         nullable=False, comment="最后更新时间")
    delete_status = Column(Boolean(), nullable=False, default=False, comment="是否删除")

    __table__args__ = (
        UniqueConstraint("name", "age", "phone"),  # 联合唯一约束
        Index("name", "addr", unique=True),  # 联合唯一索引
    )

if __name__ == "__main__":
    # # 删除表
    # Base.metadata.drop_all(engine)
    # # 创建表
    databaseClient = DatabaseClient()
    print(databaseClient.session.query(UserInfo).filter(UserInfo.id == id).first())
    databaseClient.close()
