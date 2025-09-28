from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 📂 Ma'lumotlar bazasi
ORDER_DB = "database/orders.db"
DATABASE_URL = f"sqlite:///{ORDER_DB}"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


# 🧱 Xizmatlar jadvali
class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True)
    categoria_nomi = Column(String, nullable=False)
    bolim_nomi = Column(String, nullable=False)
    xizmat_nomi = Column(String, nullable=False)
    narxi = Column(Integer, default=0)
    tavsif = Column(Text, default="")
    buyurtma_soni = Column(Integer, default=0)
    sarflangan_summa = Column(Integer, default=0)


# 📌 Jadval yaratish
def create_services_table():
    Base.metadata.create_all(engine)


# ➕ Xizmat qo‘shish
def add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif):
    with Session() as session:
        # Agar mavjud bo‘lsa yangilab qo‘yish uchun merge ishlatyapmiz
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


# 📥 Barcha xizmatlarni qo‘shish
def insert_all_services():
    xizmatlar = {
        "🔵Telegram": {
            "👍👎 Reaksiya": [
                {"service": 74, "name": "ijobiy Reaksiya [ Aralash 👍😅🎉🔥🥰👏❤️ ]"},
                {"service": 86, "name": "🎉 Reaksiya"},
                {"service": 84, "name": "🤩 Reaksiya"},
                {"service": 82, "name": "🔥 Reaksiya"},
                {"service": 950, "name": "🤝 Reaksiya"},
                {"service": 949, "name": "🍓 Reaksiya"},
                {"service": 75, "name": "Salbiy Reaksiya [ Aralash 👎😁😢💩🤮🤢 ]"},
                {"service": 81, "name": "👎 Reaksiya"},
                {"service": 1056, "name": "⚡ Reaksiya"},
                {"service": 1054, "name": "💔 Reaksiya"},
                {"service": 80, "name": "👍 Reaksiya"},
                {"service": 83, "name": "❤️ Reaksiya"},
                {"service": 88, "name": "😁 Reaksiya"},
                {"service": 912, "name": "💯 Reaksiya"}
            ],
            "👁 Ko'rishlar": [
                {"service": 102, "name": "👁 Prosmotir"},
                {"service": 105, "name": "📖 Istoriya ko'rish"}
            ],
            "👤 Obunachilar": [
                {"service": 27, "name": "👤 Obunachi ARZON (BOT)"},
                {"service": 22, "name": "👤 Obunachi(♻️R60) kafolat"},
                {"service": 41, "name": "👤 Obunachi ⚡Super Tezkor(♻️R30 kunlik)"},
                {"service": 42, "name": "👤 Obunachi (♻️R30) kafolat ⚡"},
                {"service": 14, "name": "👤 Obunachi 🔥 VIP BEZMINUS 🔥"},
                {"service": 3, "name": "👤 Obunachi (♻️R90) kafolat ⚡"},
                {"service": 821, "name": "👤 Obunachi 🇨🇳Xitoy (⛔BEZMINUS)"},
                {"service": 15, "name": "👤 Obunachi 1 yil Kafolatlangan (⛔BEZMINUS)"},
                {"service": 916, "name": "🇺🇿 O'zbek obunachi "},
                {"service": 974, "name": "🇺🇿 TG O‘zbek Obunachi [ Aktiv ] 🔥"},
                {"service": 32, "name": "👤 Obunachi (👁 Online 100% guruh uchun 🚀🚀🚀)"}
            ],
        },
        "🔴Instagram": {
            "👤 Obunachi (✅ Kafolatli)": [
                {"service": 206, "name": "👤 Obunachi (✅ Kafolatli)"},
                {"service": 230, "name": "🔥Haqiqiy 👤 Obunachilar "}
            ],
            "🎥 Video Ko‘rishlar": [
                {"service": 207, "name": "🎥 Video Ko‘rishlar"}
            ],
            "❤️ Like": [
                {"service": 208, "name": "❤️ Like"}
            ],
            "👁 Ko‘rish (live video)": [
                {"service": 209, "name": "👁 Ko‘rish (live video)"}
            ],
            "👁 Stories Prosmotr": [
                {"service": 210, "name": "👁 Stories Prosmotr"}
            ],
            "🚀 Ulashish / 💾 Saxranit": [
                {"service": 211, "name": "🚀 Ulashish / 💾 Saxranit"}
            ]
        },
        "🟡You Tube": {
            "👁 Ko'rishlar": [
                {"service": 301, "name": "👁 Ko'rishlar"}
            ],
            "👍 Like": [
                {"service": 302, "name": "👍 Like"}
            ],
            "👤 Obunachilar": [
                {"service": 303, "name": "👤 Obunachilar"}
            ],
            "👁 Live ko'rishlar": [
                {"service": 304, "name": "👁 Live ko'rishlar"}
            ]
        },
        "⚫️Tik Tok": {
            "👁 Ko'rishlar": [
                {"service": 401, "name": "👁 Ko'rishlar"}
            ],
            "👍 Like": [
                {"service": 402, "name": "👍 Like"}
            ],
            "👤 Obunachilar": [
                {"service": 403, "name": "👤 Obunachilar"}
            ]
        },
        "Bepul xizmatlar": {}
    }

    for categoria_nomi, bolimlar in xizmatlar.items():
        for bolim_nomi, xizmat_list in bolimlar.items():
            for xizmat in xizmat_list:
                service_id = xizmat.get("service")
                xizmat_nomi = xizmat.get("name")
                narxi = 0
                tavsif = ""
                add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif)
                print(f"Qo'shildi: {categoria_nomi} -> {bolim_nomi} -> {xizmat_nomi}")


if __name__ == "__main__":
    create_services_table()
    insert_all_services()