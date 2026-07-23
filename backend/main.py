import os
import logging

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator

from products import PRODUCT_DESCRIPTIONS, PRODUCT_CATEGORIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("devgloyd")

# Formspree endpoint kept server-side so it's not exposed to the client bundle.
FORMSPREE_URL = os.environ.get("FORMSPREE_URL", "https://formspree.io/f/xzdywdzv")

app = FastAPI(title="Devgloyd API", version="1.0.0")

# --- CORS ---
# Add your deployed Firebase Hosting / GitHub Pages origins here.
ALLOWED_ORIGINS = [
    "http://localhost:*",
    "https://devgloyd.com",
    "https://www.devgloyd.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to ALLOWED_ORIGINS once your frontend domain is final
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Schemas ---
class ProductSummary(BaseModel):
    name: str
    image: str
    short_description: str


class ProductCategory(BaseModel):
    category: str
    products: list[ProductSummary]


class ContactRequest(BaseModel):
    email: EmailStr
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ContactResponse(BaseModel):
    success: bool
    detail: str


class CheckoutRequest(BaseModel):
    products: list[str]

    @field_validator("products")
    @classmethod
    def at_least_one_product(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("Select at least one product")
        return v


class CheckoutResponse(BaseModel):
    success: bool
    detail: str
    items: list[str]


# --- Helpers ---
def _short_description(name: str) -> str:
    """First non-empty line of the full description, used as a card blurb."""
    full = PRODUCT_DESCRIPTIONS.get(name, "")
    for line in full.splitlines():
        if line.strip():
            return line.strip()
    return ""


# --- Routes ---
@app.get("/")
async def root():
    return {"status": "ok", "service": "Devgloyd API"}


@app.get("/api/products", response_model=list[ProductCategory])
async def get_products():
    """Returns product catalog grouped by category, for the Shop section."""
    categories = []
    for category_name, items in PRODUCT_CATEGORIES.items():
        summaries = [
            ProductSummary(
                name=item["name"],
                image=item["image"],
                short_description=_short_description(item["name"]),
            )
            for item in items
        ]
        categories.append(ProductCategory(category=category_name, products=summaries))
    return categories


@app.get("/api/products/{product_name}")
async def get_product_detail(product_name: str):
    """Full description text shown in the product detail dialog."""
    description = PRODUCT_DESCRIPTIONS.get(product_name)
    if description is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"name": product_name, "description": description}


@app.post("/api/checkout", response_model=CheckoutResponse)
async def checkout(payload: CheckoutRequest):
    """Validates the selected products exist; actual payment integration (Stripe/PayPal)
    can be wired in here later per the Web Enterprise tier described in products.py."""
    unknown = [p for p in payload.products if p not in PRODUCT_DESCRIPTIONS]
    if unknown:
        raise HTTPException(
            status_code=400, detail=f"Unknown product(s): {', '.join(unknown)}"
        )
    return CheckoutResponse(
        success=True,
        detail=f"Proceeding with: {', '.join(payload.products)}",
        items=payload.products,
    )


@app.post("/api/contact", response_model=ContactResponse)
async def contact(payload: ContactRequest):
    """Forwards contact/inquiry messages to Formspree server-side."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                FORMSPREE_URL,
                json={"email": payload.email, "message": payload.message},
                headers={"Accept": "application/json"},
            )
        if r.status_code == 200:
            return ContactResponse(success=True, detail="Email sent successfully!")
        logger.warning("Formspree responded with %s: %s", r.status_code, r.text)
        raise HTTPException(
            status_code=502, detail=f"Failed to send message (status {r.status_code})"
        )
    except httpx.RequestError as exc:
        logger.error("Network error contacting Formspree: %s", exc)
        raise HTTPException(status_code=502, detail="Network error, please try again.")
