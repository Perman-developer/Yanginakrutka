from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta


from config import DB_NAME

# SQLAlchemy engine va sessiya
DATABASE_URL = f"sqlite:///{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()



# 🕒 O‘zbekiston vaqti funksiyasi
def hozirgi_vaqt_uzb(as_str=True):
    utc_vaqt = datetime.utcnow()
    uzb_vaqt = utc_vaqt + timedelta(hours=5)  # Asia/Tashkent = UTC+5
    if as_str:
        return uzb_vaqt.strftime("%Y-%m-%d %H:%M:%S")
    return uzb_vaqt  # datetime obyekt


# 🧱 Foydalanuvchilar jadvali
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    balance = Column(Integer, default=0)
    referal_id = Column(Integer)
    referal_count = Column(Integer, default=0)
    referal_summa = Column(Integer, default=0)
    register_time = Column(String, default=hozirgi_vaqt_uzb)
    deposit_summa = Column(Integer, default=0)


# 📋 Buyurtmalar jadvali
class UserOrder(Base):
    __tablename__ = "users_order"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    xizmat_turi = Column(String)
    link = Column(Text)
    amount = Column(Integer)
    narx = Column(Integer)
    vaqt = Column(String, default=hozirgi_vaqt_uzb)


# 🔧 Jadval yaratish
def create_tables():
    Base.metadata.create_all(engine)


# 🔍 Barcha foydalanuvchilarni olish
def get_all_user_ids():
    with Session() as session:
        rows = session.query(User.user_id).all()
        return [row[0] for row in rows]


# 🔍 User mavjudligini tekshirish
def user_exists(user_id: int) -> bool:
    with Session() as session:
        return session.query(User).filter_by(user_id=user_id).first() is not None


# ➕ Yangi user qo‘shish
def add_user(user_id: int, referal_id=None):
    with Session() as session:
        user = User(user_id=user_id, referal_id=referal_id)
        session.add(user)
        if referal_id:
            ref_user = session.query(User).filter_by(user_id=referal_id).first()
            if ref_user:
                ref_user.referal_count += 1
        session.commit()


# 💰 Balans qo‘shish
def add_balance(user_id: int, balance: int):
    with Session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.balance += balance
            session.commit()


# 💸 Balansdan ayirish
def subtract_balance(user_id: int, balance: int):
    with Session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.balance -= balance
            session.commit()


# 🔍 User maʼlumotlarini olish
def get_user_data(user_id: int):
    with Session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            return {
                "user_id": user.user_id,
                "balance": user.balance,
                "referal_id": user.referal_id,
                "referal_count": user.referal_count,
                "referal_summa": user.referal_summa
            }
    return None





# ➕ Buyurtma qo‘shish
def add_order_db(user_id, order_id, xizmat_nomi, link, amount, narx):
    vaqt = hozirgi_vaqt_uzb()
    with Session() as session:
        order = UserOrder(
            user_id=user_id,
            order_id=order_id,
            xizmat_turi=xizmat_nomi,
            link=link,
            amount=amount,
            narx=narx
        )
        session.add(order)
        session.commit()


# 🔍 Foydalanuvchi buyurtmalarini olish
def get_orders_by_user(user_id):
    with Session() as session:
        rows = (
            session.query(UserOrder)
            .filter_by(user_id=user_id)
            .order_by(UserOrder.vaqt.desc())
            .all()
        )
        return [
            {
                "user_id": row.user_id,
                "order_id": row.order_id,
                "xizmat_turi": row.xizmat_turi,
                "link": row.link,
                "amount": row.amount,
                "narx": row.narx,
                "vaqt": row.vaqt,
            }
            for row in rows
        ]