from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# DB fayl
from config import ORDER_DB

DATABASE_URL = f"sqlite:///{ORDER_DB}"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True)
    categoria_nomi = Column(String, nullable=False)
    bolim_nomi = Column(String, nullable=False)
    xizmat_nomi = Column(String, nullable=False)
    narxi = Column(Integer, nullable=False)
    tavsif = Column(Text)
    buyurtma_soni = Column(Integer, default=0)
    sarflangan_summa = Column(Integer, default=0)


# Jadval yaratish
def create_services_table():
    Base.metadata.create_all(engine)


def add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif):
    with Session() as session:
        service = Service(
            service_id=service_id,
            categoria_nomi=categoria_nomi,
            bolim_nomi=bolim_nomi,
            xizmat_nomi=xizmat_nomi,
            narxi=narxi,
            tavsif=tavsif
        )
        session.merge(service)  # INSERT OR REPLACE
        session.commit()


# Unikal kategoriyalarni olish
def get_categories():
    with Session() as session:
        rows = session.query(Service.categoria_nomi).distinct().all()
        return [row[0] for row in rows]


# Tanlangan kategoriya bo‘yicha bo‘limlar
def get_bolimlar(category):
    with Session() as session:
        rows = session.query(Service.bolim_nomi).filter(Service.categoria_nomi == category).distinct().all()
        return [row[0] for row in rows]


# Tanlangan bo‘lim bo‘yicha xizmatlar
def get_xizmatlar(category, bolim):
    with Session() as session:
        rows = session.query(Service.service_id, Service.xizmat_nomi).filter(
            Service.categoria_nomi == category,
            Service.bolim_nomi == bolim
        ).all()
        return rows  # [(service_id, xizmat_nomi), ...]


# Xizmatlarni tahrirlash
def edit_service(target_id: int, **kwargs):
    with Session() as session:
        service = session.get(Service, target_id)
        if not service:
            return
        for field, value in kwargs.items():
            if hasattr(service, field) and value not in ("", None):
                setattr(service, field, value)
        session.commit()


# Xizmatni o‘chirish
def delete_service(service_id: int):
    with Session() as session:
        service = session.get(Service, service_id)
        if service:
            session.delete(service)
            session.commit()


# Xizmatni ID bo‘yicha olish
def get_service_by_id(service_id: int) -> dict | None:
    with Session() as session:
        service = session.get(Service, service_id)
        if service:
            return {
                "service_id": service.service_id,
                "categoria_nomi": service.categoria_nomi,
                "bolim_nomi": service.bolim_nomi,
                "xizmat_nomi": service.xizmat_nomi,
                "narxi": service.narxi,
                "tavsif": service.tavsif,
                "buyurtma_soni": service.buyurtma_soni,
                "sarflangan_summa": service.sarflangan_summa
            }
    return None