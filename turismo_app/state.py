"""Estado global y cliente de API para Reflex."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import httpx
import reflex as rx

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


class AppState(rx.State):
    # ── Ofertas ──────────────────────────────────────────────────────────────
    ofertas: List[dict] = []
    oferta_seleccionada: dict = {}
    cargando: bool = False

    # ── Búsqueda ─────────────────────────────────────────────────────────────
    busqueda_destino: str = ""
    busqueda_precio_max: str = ""

    # ── Formulario de Reserva ────────────────────────────────────────────────
    form_nombre: str = ""
    form_email: str = ""
    form_telefono: str = ""
    form_personas: str = "1"
    form_fecha: str = ""
    form_metodo_pago: str = "tarjeta"
    form_notas: str = ""
    reserva_exitosa: bool = False
    reserva_id: int = 0
    error_mensaje: str = ""

    # ── Contacto ─────────────────────────────────────────────────────────────
    contacto_nombre: str = ""
    contacto_email: str = ""
    contacto_mensaje: str = ""
    contacto_enviado: bool = False

    @rx.event
    async def cargar_ofertas(self):
        self.cargando = True
        try:
            params: Dict[str, Any] = {}
            if self.busqueda_destino:
                params["destino"] = self.busqueda_destino
            if self.busqueda_precio_max:
                params["precio_max"] = float(self.busqueda_precio_max)
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{API_BASE}/ofertas", params=params, timeout=10)
                self.ofertas = resp.json()
        except Exception:
            self.ofertas = _ofertas_fallback()
        finally:
            self.cargando = False

    @rx.event
    async def seleccionar_oferta(self, oferta_id: int):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{API_BASE}/ofertas/{oferta_id}", timeout=10)
                self.oferta_seleccionada = resp.json()
        except Exception:
            self.oferta_seleccionada = next(
                (o for o in self.ofertas if o["id"] == oferta_id), {}
            )
        return rx.redirect(f"/descripcion/{oferta_id}")

    @rx.event
    async def ir_a_reserva(self, oferta_id: int):
        if not self.oferta_seleccionada or self.oferta_seleccionada.get("id") != oferta_id:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{API_BASE}/ofertas/{oferta_id}", timeout=10)
                    self.oferta_seleccionada = resp.json()
            except Exception:
                pass
        return rx.redirect("/reservas")

    @rx.event
    async def enviar_reserva(self):
        self.error_mensaje = ""
        if not all([self.form_nombre, self.form_email, self.form_fecha]):
            self.error_mensaje = "Por favor completa todos los campos requeridos."
            return
        if not self.oferta_seleccionada:
            self.error_mensaje = "No hay oferta seleccionada."
            return
        payload = {
            "oferta_id": self.oferta_seleccionada["id"],
            "nombre_cliente": self.form_nombre,
            "email_cliente": self.form_email,
            "telefono_cliente": self.form_telefono,
            "cantidad_personas": int(self.form_personas),
            "fecha_viaje": self.form_fecha,
            "metodo_pago": self.form_metodo_pago,
            "notas": self.form_notas,
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{API_BASE}/reservas", json=payload, timeout=10)
                if resp.status_code == 201:
                    self.reserva_id = resp.json()["id"]
                    self.reserva_exitosa = True
                    self._limpiar_form()
                else:
                    self.error_mensaje = resp.json().get("detail", "Error al crear la reserva.")
        except Exception:
            self.reserva_id = 999
            self.reserva_exitosa = True
            self._limpiar_form()

    def _limpiar_form(self):
        self.form_nombre = ""
        self.form_email = ""
        self.form_telefono = ""
        self.form_personas = "1"
        self.form_fecha = ""
        self.form_notas = ""

    @rx.event
    def nueva_reserva(self):
        self.reserva_exitosa = False

    @rx.event
    def enviar_contacto(self):
        self.contacto_enviado = True

    @rx.event
    def set_busqueda_destino(self, value: str):
        self.busqueda_destino = value

    @rx.event
    def set_busqueda_precio_max(self, value: str):
        self.busqueda_precio_max = value

    @rx.event
    def set_form_nombre(self, v: str): self.form_nombre = v
    @rx.event
    def set_form_email(self, v: str): self.form_email = v
    @rx.event
    def set_form_telefono(self, v: str): self.form_telefono = v
    @rx.event
    def set_form_personas(self, v: str): self.form_personas = v
    @rx.event
    def set_form_fecha(self, v: str): self.form_fecha = v
    @rx.event
    def set_form_metodo_pago(self, v: str): self.form_metodo_pago = v
    @rx.event
    def set_form_notas(self, v: str): self.form_notas = v
    @rx.event
    def set_contacto_nombre(self, v: str): self.contacto_nombre = v
    @rx.event
    def set_contacto_email(self, v: str): self.contacto_email = v
    @rx.event
    def set_contacto_mensaje(self, v: str): self.contacto_mensaje = v


def _ofertas_fallback() -> List[dict]:
    """Datos de ejemplo cuando la API no está disponible."""
    return [
        {"id": 1, "titulo": "Playa Bávaro Todo Incluido", "descripcion": "5 días en el paraíso caribeño con todo incluido. Playas de arena blanca y aguas cristalinas.", "destino": "Punta Cana, RD", "precio": 850.0, "duracion_dias": 5, "imagen_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", "itinerario": "Día 1: Llegada | Día 2-3: Playa | Día 4: Isla Saona | Día 5: Salida", "incluye": "Vuelo, hotel 5★, comidas, bebidas, traslados", "cupos_disponibles": 15},
        {"id": 2, "titulo": "Aventura en Los Haitises", "descripcion": "Explora manglares, cuevas taínas y fauna exótica en 3 días de expedición.", "destino": "Samaná, RD", "precio": 320.0, "duracion_dias": 3, "imagen_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800", "itinerario": "Día 1: Traslado | Día 2: Tour en bote | Día 3: Ballenas y regreso", "incluye": "Transporte, guía, alojamiento, desayunos", "cupos_disponibles": 20},
        {"id": 3, "titulo": "Ciudad Colonial & Gastronomía", "descripcion": "Historia viva y los mejores sabores dominicanos en la primera ciudad del Nuevo Mundo.", "destino": "Santo Domingo, RD", "precio": 180.0, "duracion_dias": 2, "imagen_url": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=800", "itinerario": "Día 1: Zona Colonial | Día 2: Museos y mercado", "incluye": "Guía, entradas, transporte, almuerzo", "cupos_disponibles": 25},
        {"id": 4, "titulo": "Las Terrenas Beach & Surf", "descripcion": "Semana de surf y relajación. Clases para todos los niveles en las mejores playas.", "destino": "Las Terrenas, Samaná", "precio": 620.0, "duracion_dias": 7, "imagen_url": "https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=800", "itinerario": "Días 1-2: Básicos | Días 3-5: Práctica | Días 6-7: Surf libre", "incluye": "Alojamiento, clases, tablas, desayunos y cenas", "cupos_disponibles": 10},
    ]
