"""
API REST – Plataforma de Reservas Turísticas
Ejecutar: uvicorn api.main:app --reload --port 8000
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

load_dotenv()

# ─── Base de Datos ────────────────────────────────────────────────────────────

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "turismo_db")

DATABASE_URL = (
    f"mssql+pyodbc://NASR\\SQLEXPRESS/{DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
    f"&trusted_connection=yes"
    f"&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# ─── Modelos ORM ─────────────────────────────────────────────────────────────


class OfertaModel(Base):
    __tablename__ = "ofertas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    destino = Column(String(150), nullable=False)
    precio = Column(Float, nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    imagen_url = Column(String(500), nullable=True)
    itinerario = Column(Text, nullable=True)
    incluye = Column(Text, nullable=True)
    cupos_disponibles = Column(Integer, default=20)
    creado_en = Column(DateTime, default=datetime.utcnow)

    reservas = relationship("ReservaModel", back_populates="oferta")


class ReservaModel(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    oferta_id = Column(Integer, ForeignKey("ofertas.id"), nullable=False)
    nombre_cliente = Column(String(200), nullable=False)
    email_cliente = Column(String(200), nullable=False)
    telefono_cliente = Column(String(30), nullable=True)
    cantidad_personas = Column(Integer, default=1)
    fecha_viaje = Column(String(20), nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    estado = Column(String(30), default="pendiente")
    notas = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    oferta = relationship("OfertaModel", back_populates="reservas")


# ─── Schemas Pydantic ─────────────────────────────────────────────────────────


class OfertaOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    destino: str
    precio: float
    duracion_dias: int
    imagen_url: Optional[str]
    itinerario: Optional[str]
    incluye: Optional[str]
    cupos_disponibles: int
    creado_en: datetime

    model_config = {"from_attributes": True}


class ReservaCreate(BaseModel):
    oferta_id: int
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: Optional[str] = None
    cantidad_personas: int = 1
    fecha_viaje: str
    metodo_pago: str
    notas: Optional[str] = None

    @field_validator("cantidad_personas")
    @classmethod
    def personas_positivas(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Debe reservar al menos 1 persona")
        return v

    @field_validator("metodo_pago")
    @classmethod
    def metodo_valido(cls, v: str) -> str:
        opciones = {"tarjeta", "transferencia", "efectivo", "paypal"}
        if v.lower() not in opciones:
            raise ValueError(f"Método de pago inválido. Opciones: {opciones}")
        return v.lower()


class ReservaOut(BaseModel):
    id: int
    oferta_id: int
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: Optional[str]
    cantidad_personas: int
    fecha_viaje: str
    metodo_pago: str
    estado: str
    notas: Optional[str]
    creado_en: datetime

    model_config = {"from_attributes": True}


# ─── App FastAPI ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="Turismo RD – API",
    description="API REST para gestionar ofertas y reservas turísticas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def crear_tablas():
    """Crea las tablas si no existen y carga datos de ejemplo."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(OfertaModel).count() == 0:
            _seed_data(db)
    finally:
        db.close()


def _seed_data(db: Session):
    """Datos de ejemplo para desarrollo."""
    ofertas = [
        OfertaModel(
            titulo="Playa Bávaro Todo Incluido",
            descripcion=(
                "Disfruta 5 días en el paraíso caribeño con todo incluido. "
                "Playas de arena blanca, aguas cristalinas y entretenimiento de primera."
            ),
            destino="Punta Cana, República Dominicana",
            precio=850.00,
            duracion_dias=5,
            imagen_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            itinerario="Día 1: Llegada y check-in | Día 2: Playa y actividades acuáticas | Día 3: Excursión a Isla Saona | Día 4: Spa y relax | Día 5: Salida",
            incluye="Vuelo, hotel 5★, comidas, bebidas, traslados, seguro de viaje",
            cupos_disponibles=15,
        ),
        OfertaModel(
            titulo="Aventura en Los Haitises",
            descripcion=(
                "Explora el Parque Nacional Los Haitises: manglares, cuevas taínas "
                "y fauna exótica en una expedición de 3 días inolvidable."
            ),
            destino="Samaná, República Dominicana",
            precio=320.00,
            duracion_dias=3,
            imagen_url="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800",
            itinerario="Día 1: Traslado a Samaná | Día 2: Tour en bote por Los Haitises | Día 3: Avistamiento de ballenas y regreso",
            incluye="Transporte, guía local, alojamiento, desayunos, equipo de snorkel",
            cupos_disponibles=20,
        ),
        OfertaModel(
            titulo="Ciudad Colonial & Gastronomía",
            descripcion=(
                "Descubre la primera ciudad europea del Nuevo Mundo. "
                "Recorrido cultural, historia viva y los mejores sabores dominicanos."
            ),
            destino="Santo Domingo, República Dominicana",
            precio=180.00,
            duracion_dias=2,
            imagen_url="https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=800",
            itinerario="Día 1: Zona Colonial, Catedral, Alcázar de Colón, cena típica | Día 2: Museo del Hombre Dominicano, mercado artesanal",
            incluye="Guía certificado, entradas a museos, transporte, almuerzo típico",
            cupos_disponibles=25,
        ),
        OfertaModel(
            titulo="Las Terrenas Beach & Surf",
            descripcion=(
                "Semana de surf y relajación en las mejores playas de la Península de Samaná. "
                "Clases para todos los niveles incluidas."
            ),
            destino="Las Terrenas, Samaná",
            precio=620.00,
            duracion_dias=7,
            imagen_url="https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=800",
            itinerario="Días 1-2: Llegada y clases básicas | Días 3-5: Práctica intensiva y excursiones | Días 6-7: Surf libre y cierre",
            incluye="Alojamiento frente al mar, clases de surf, tablas, desayunos y cenas",
            cupos_disponibles=10,
        ),
    ]
    db.add_all(ofertas)
    db.commit()


# ─── Endpoints ────────────────────────────────────────────────────────────────


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "mensaje": "Turismo RD API funcionando 🌴"}


@app.get("/ofertas", response_model=List[OfertaOut], tags=["Ofertas"])
def listar_ofertas(
    destino: Optional[str] = None,
    precio_max: Optional[float] = None,
    duracion_max: Optional[int] = None,
):
    """Retorna todas las ofertas turísticas con filtros opcionales."""
    from fastapi import Depends

    db = SessionLocal()
    try:
        query = db.query(OfertaModel)
        if destino:
            query = query.filter(OfertaModel.destino.ilike(f"%{destino}%"))
        if precio_max:
            query = query.filter(OfertaModel.precio <= precio_max)
        if duracion_max:
            query = query.filter(OfertaModel.duracion_dias <= duracion_max)
        return query.all()
    finally:
        db.close()


@app.get("/ofertas/{oferta_id}", response_model=OfertaOut, tags=["Ofertas"])
def obtener_oferta(oferta_id: int):
    """Retorna una oferta por su ID."""
    db = SessionLocal()
    try:
        oferta = db.query(OfertaModel).filter(OfertaModel.id == oferta_id).first()
        if not oferta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Oferta {oferta_id} no encontrada",
            )
        return oferta
    finally:
        db.close()


@app.post(
    "/reservas",
    response_model=ReservaOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Reservas"],
)
def crear_reserva(reserva: ReservaCreate):
    """Registra una nueva reserva turística."""
    db = SessionLocal()
    try:
        oferta = (
            db.query(OfertaModel).filter(OfertaModel.id == reserva.oferta_id).first()
        )
        if not oferta:
            raise HTTPException(
                status_code=404,
                detail=f"Oferta {reserva.oferta_id} no encontrada",
            )
        if oferta.cupos_disponibles < reserva.cantidad_personas:
            raise HTTPException(
                status_code=400,
                detail=f"Solo quedan {oferta.cupos_disponibles} cupos disponibles",
            )

        nueva_reserva = ReservaModel(**reserva.model_dump())
        oferta.cupos_disponibles -= reserva.cantidad_personas
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)
        return nueva_reserva
    finally:
        db.close()


@app.get("/reservas", response_model=List[ReservaOut], tags=["Reservas"])
def listar_reservas(email: Optional[str] = None):
    """Retorna todas las reservas. Filtra por email si se provee."""
    db = SessionLocal()
    try:
        query = db.query(ReservaModel)
        if email:
            query = query.filter(ReservaModel.email_cliente == email)
        return query.order_by(ReservaModel.creado_en.desc()).all()
    finally:
        db.close()


@app.get("/reservas/{reserva_id}", response_model=ReservaOut, tags=["Reservas"])
def obtener_reserva(reserva_id: int):
    """Retorna una reserva por su ID."""
    db = SessionLocal()
    try:
        reserva = (
            db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        )
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva
    finally:
        db.close()


@app.delete("/reservas/{reserva_id}", tags=["Reservas"])
def cancelar_reserva(reserva_id: int):
    """Cancela una reserva existente."""
    db = SessionLocal()
    try:
        reserva = (
            db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
        )
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        oferta = (
            db.query(OfertaModel)
            .filter(OfertaModel.id == reserva.oferta_id)
            .first()
        )
        if oferta:
            oferta.cupos_disponibles += reserva.cantidad_personas
        reserva.estado = "cancelada"
        db.commit()
        return {"mensaje": f"Reserva {reserva_id} cancelada exitosamente"}
    finally:
        db.close()
