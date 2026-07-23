# products.py
# Source of truth for product catalog data served by the API.

PRODUCT_DESCRIPTIONS = {
    "Web Starter": """The Digital Identity Foundation
Perfect for small businesses, freelancers, or personal brands looking to establish a professional online presence. This "brochure-style" site focuses on high-impact visuals and seamless communication.

Description: A sleek, high-performance landing page designed to showcase your brand. It integrates rich multimedia content with a direct line of communication to your audience, ensuring you are reachable 24/7.
Key Tech Stack: Python Flet/Streamlit, Formspree (Email), GitHub Repository Management, Google Workspace integration, and Squarespace Domain.
Suggested Feature: Social Media Aggregator.
Function: Automatically pull and display your latest Instagram or LinkedIn posts directly onto the page to keep content fresh without manual updates.""",

    "Web Professional": """The Data-Driven Dynamic App
Tailored for businesses that need more than just a digital business card. This tier introduces logic-based operations and persistent data storage to handle actual workflows.

Description: A robust web application capable of processing complex logic and mathematical computations. With integrated database support, it allows for user data persistence, making it ideal for internal tools, calculators, or client portals.
Key Tech Stack: Everything in Starter + Firebase Real-time Database & Storage and specialized Streamlit Cloud Deployment.
Suggested Feature: Interactive Data Dashboard.
Function: Convert raw user data or uploaded CSVs into real-time visual charts and downloadable PDF reports, providing immediate value to the end-user.""",

    "Web Enterprise": """The AI-Powered Powerhouse
The ultimate solution for scaling businesses. This tier combines e-commerce capabilities with cutting-edge Artificial Intelligence to automate complex tasks and drive revenue.

Description: A comprehensive ecosystem that bridges the gap between traditional web apps and modern AI. It handles secure financial transactions, location-based services, and intelligent automation to provide a friction-less user experience.
Key Tech Stack: Everything in Professional + Stripe/PayPal Integration (E-commerce), Google Maps API, Biometric Authentication, and OCR (Optical Character Recognition) engines.
Suggested Feature: Smart Inventory & Predictive AI Chatbot.
Function: A chatbot that doesn't just answer FAQs, but uses the document scanning feature to help users "upload a receipt/invoice" to automatically populate their orders or account history.""",

    "iOS App": "Native Swift development optimized for the latest iPhone models.",
    "Android App": "Material Design focused app with support for a wide range of devices.",
    "Cross-Platform": "Single codebase using Flutter to reach both iOS and Android users.",
    "Windows Suite": "Powerful .NET desktop application for enterprise resource planning.",
    "macOS Tool": "SwiftUI based productivity tool designed for the Apple ecosystem.",
    "Linux Client": "Lightweight, high-performance binary for various distributions.",
}

# Category groupings + image keys, used to drive the Shop section UI.
PRODUCT_CATEGORIES = {
    "WEB APPLICATIONS": [
        {"name": "Web Starter", "image": "web_start.png"},
        {"name": "Web Professional", "image": "web_pro.png"},
        {"name": "Web Enterprise", "image": "web_ent.png"},
    ],
    "MOBILE APPS": [
        {"name": "iOS App", "image": "ios_app.png"},
        {"name": "Android App", "image": "android_app.png"},
        {"name": "Cross-Platform", "image": "cross_flat.png"},
    ],
    "DESKTOP SOFTWARE": [
        {"name": "Windows Suite", "image": "win_app.png"},
        {"name": "macOS Tool", "image": "mac_os.png"},
        {"name": "Linux Client", "image": "linux_os.png"},
    ],
}
