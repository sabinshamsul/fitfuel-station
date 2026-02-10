"""
FitFuel Payment System
Supports QR payments and card payments
"""

'''
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import time
import logging
import json
from datetime import datetime
from typing import Dict, Optional
import uuid

# For demo purposes - replace with actual payment gateway
# import stripe  # For card payments
# import requests  # For API calls to payment gateway


class PaymentConfig:
    """Payment configuration and pricing."""
    
    # Base pricing
    BASE_PRICE = 12.00  # RM
    
    # Premium ingredient pricing
    PREMIUM_INGREDIENTS = {
        'leucine': 2.00,
        'guarana_extract': 1.50,
        'matcha_powder': 2.50,
        'cocoa_powder': 1.00,
        'instant_coffee': 1.00,
    }
    
    # Customization tier pricing
    CUSTOMIZATION_FEES = {
        'ai_optimized': 3.00,
        'user_custom': 5.00,
    }
    
    # Payment methods
    PAYMENT_METHODS = ['qr', 'card', 'cash', 'membership']
    
    # QR payment timeout (seconds)
    QR_TIMEOUT = 300  # 5 minutes
    
    # Payment gateway API keys (demo - replace with real keys)
    REVENUE_MONSTER_API_KEY = "your_api_key_here"
    STRIPE_API_KEY = "your_stripe_key_here"


class PricingCalculator:
    """Calculate order price based on formulation."""
    
    @staticmethod
    def calculate_price(formulation: Dict, customization_type: str = 'ai_optimized') -> Dict:
        """
        Calculate total price for the order.
        
        Args:
            formulation: Dict with ingredient percentages
            customization_type: 'ai_optimized' or 'user_custom'
            
        Returns:
            Dict with price breakdown
        """
        base_price = PaymentConfig.BASE_PRICE
        premium_total = 0.00
        premium_items = []
        
        # Calculate premium ingredient costs
        for ingredient, percentage in formulation.items():
            if ingredient in PaymentConfig.PREMIUM_INGREDIENTS:
                # Check if significant amount
                if percentage > 0.5:  # More than 0.5%
                    cost = PaymentConfig.PREMIUM_INGREDIENTS[ingredient]
                    premium_total += cost
                    premium_items.append((ingredient, cost))
        
        # Add customization fee
        customization_fee = PaymentConfig.CUSTOMIZATION_FEES.get(customization_type, 0)
        
        # Calculate totals
        subtotal = base_price + premium_total + customization_fee
        tax = 0.00  # Malaysia - no SST on food in vending machines typically
        total = subtotal + tax
        
        return {
            'base_price': base_price,
            'premium_items': premium_items,
            'premium_total': premium_total,
            'customization_fee': customization_fee,
            'customization_type': customization_type,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'currency': 'MYR'
        }


class PaymentProcessor:
    """Handle payment processing."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_transaction = None
    
    def generate_qr_code(self, amount: float, transaction_id: str) -> Image:
        """
        Generate QR code for payment.
        
        In production, this would call your payment gateway API
        to generate a dynamic QR code with payment details.
        """
        # Demo QR code - in production, use payment gateway API
        # Example for Revenue Monster:
        # response = requests.post(
        #     "https://api.revenuemonster.my/v3/payment/online",
        #     headers={"Authorization": f"Bearer {PaymentConfig.REVENUE_MONSTER_API_KEY}"},
        #     json={
        #         "order": {"amount": int(amount * 100), "currencyType": "MYR"},
        #         "type": "DYNAMIC_QR"
        #     }
        # )
        # qr_string = response.json()['item']['qrCodeUrl']
        
        # For demo, create QR with transaction details
        qr_data = json.dumps({
            'merchant': 'FitFuel Station',
            'amount': amount,
            'currency': 'MYR',
            'transaction_id': transaction_id,
            'timestamp': datetime.now().isoformat()
        })
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        return qr_image
    
    def check_payment_status(self, transaction_id: str) -> Dict:
        """
        Check if payment has been completed.
        
        In production, this polls the payment gateway API.
        """
        # Demo - randomly simulate payment after some time
        # In production:
        # response = requests.get(
        #     f"https://api.revenuemonster.my/v3/payment/transaction/{transaction_id}",
        #     headers={"Authorization": f"Bearer {API_KEY}"}
        # )
        # return response.json()
        
        # For demo, simulate payment success
        if self.current_transaction and self.current_transaction.get('simulated_paid'):
            return {'status': 'SUCCESS', 'transaction_id': transaction_id}
        
        return {'status': 'PENDING', 'transaction_id': transaction_id}
    
    def process_card_payment(self, amount: float, card_token: str) -> Dict:
        """
        Process card payment via Stripe or other gateway.
        """
        # In production:
        # stripe.api_key = PaymentConfig.STRIPE_API_KEY
        # charge = stripe.Charge.create(
        #     amount=int(amount * 100),  # Amount in cents
        #     currency="myr",
        #     source=card_token,
        #     description="FitFuel Custom Protein Bar"
        # )
        # return {'status': 'SUCCESS', 'transaction_id': charge.id}
        
        # Demo
        self.logger.info(f"Processing card payment: RM {amount:.2f}")
        return {
            'status': 'SUCCESS',
            'transaction_id': str(uuid.uuid4()),
            'method': 'card'
        }
    
    def simulate_payment_received(self):
        """Demo function - simulate payment received."""
        if self.current_transaction:
            self.current_transaction['simulated_paid'] = True


# ================================================================
# UI SCREENS FOR PAYMENT FLOW
# ================================================================

def show_order_summary(app, root, canvas, pricing: Dict):
    """Display order summary with pricing before payment."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image, show_results, show_error
    from fitfuel_ui import Config, create_button, create_back_button
    
    try:
        clear_screen()
        draw_background(selection_bg_image)
        
        # Title
        canvas.create_text(
            Config.WIDTH // 2, 70,
            text="📋 ORDER SUMMARY",
            fill="white",
            font=(Config.FONT_FAMILY, Config.TITLE_FONT_SIZE, "bold")
        )
        
        # Create summary panel
        panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=30,
                        highlightbackground=Config.PRIMARY_COLOR, highlightthickness=2)
        canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2, window=panel)
        
        # Product description
        tk.Label(
            panel,
            text="Custom Protein Bar (50g)",
            bg=Config.PANEL_BG,
            fg="white",
            font=(Config.FONT_FAMILY, 16, "bold")
        ).pack(pady=(0, 5))
        
        # Configuration
        config_text = f"{app.mode.title()}-Workout | {app.carb_mode.title()}"
        if app.flavour != 'none':
            config_text += f" | {app.flavour.title()} Flavour"
        
        tk.Label(
            panel,
            text=config_text,
            bg=Config.PANEL_BG,
            fg=Config.MUTED_TEXT,
            font=(Config.FONT_FAMILY, 12)
        ).pack(pady=(0, 15))
        
        # Separator
        tk.Frame(panel, bg=Config.SEPARATOR_COLOR, height=1).pack(fill="x", pady=10)
        
        # Pricing breakdown
        price_frame = tk.Frame(panel, bg=Config.PANEL_BG)
        price_frame.pack(fill="x", pady=10)
        
        # Base price
        tk.Label(
            price_frame,
            text="Base Price:",
            bg=Config.PANEL_BG,
            fg=Config.MUTED_TEXT,
            font=(Config.FONT_FAMILY, 12),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=2)
        
        tk.Label(
            price_frame,
            text=f"RM {pricing['base_price']:.2f}",
            bg=Config.PANEL_BG,
            fg="white",
            font=(Config.FONT_FAMILY, 12),
            anchor="e"
        ).grid(row=0, column=1, sticky="e", padx=(100, 0))
        
        # Premium items
        row = 1
        for ingredient, cost in pricing['premium_items']:
            ing_name = ingredient.replace('_', ' ').title()
            
            tk.Label(
                price_frame,
                text=f"  + {ing_name}:",
                bg=Config.PANEL_BG,
                fg=Config.MUTED_TEXT,
                font=(Config.FONT_FAMILY, 11),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=1)
            
            tk.Label(
                price_frame,
                text=f"RM {cost:.2f}",
                bg=Config.PANEL_BG,
                fg="white",
                font=(Config.FONT_FAMILY, 11),
                anchor="e"
            ).grid(row=row, column=1, sticky="e", padx=(100, 0))
            row += 1
        
        # Customization fee
        if pricing['customization_fee'] > 0:
            tk.Label(
                price_frame,
                text="AI Optimization:",
                bg=Config.PANEL_BG,
                fg=Config.MUTED_TEXT,
                font=(Config.FONT_FAMILY, 12),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=2)
            
            tk.Label(
                price_frame,
                text=f"RM {pricing['customization_fee']:.2f}",
                bg=Config.PANEL_BG,
                fg="white",
                font=(Config.FONT_FAMILY, 12),
                anchor="e"
            ).grid(row=row, column=1, sticky="e", padx=(100, 0))
            row += 1
        
        # Total separator
        tk.Frame(price_frame, bg=Config.PRIMARY_COLOR, height=2).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=(10, 5)
        )
        row += 1
        
        # Total
        tk.Label(
            price_frame,
            text="TOTAL:",
            bg=Config.PANEL_BG,
            fg=Config.PRIMARY_COLOR,
            font=(Config.FONT_FAMILY, 16, "bold"),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=5)
        
        tk.Label(
            price_frame,
            text=f"RM {pricing['total']:.2f}",
            bg=Config.PANEL_BG,
            fg=Config.PRIMARY_COLOR,
            font=(Config.FONT_FAMILY, 16, "bold"),
            anchor="e"
        ).grid(row=row, column=1, sticky="e", padx=(100, 0))
        
        # Buttons
        btn_frame = tk.Frame(panel, bg=Config.PANEL_BG)
        btn_frame.pack(pady=(20, 0))
        
        create_back_button(btn_frame, lambda: show_results()).pack(side="left", padx=10)
        create_button(
            btn_frame,
            "Continue to Payment →",
            lambda: show_payment_method_selection(app, root, canvas, pricing)
        ).pack(side="left", padx=10)

    except Exception as e:
        logging.error(f"Error displaying order summary: {e}", exc_info=True)
        show_error(f"Error loading order summary: {e}")


def show_payment_method_selection(app, root, canvas, pricing: Dict):
    """Show payment method selection screen."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image
    from fitfuel_ui import Config, create_button, create_back_button
    
    clear_screen()
    draw_background(selection_bg_image)
    
    # Title
    canvas.create_text(
        Config.WIDTH // 2, 80,
        text="💳 SELECT PAYMENT METHOD",
        fill="white",
        font=(Config.FONT_FAMILY, Config.TITLE_FONT_SIZE, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, 120,
        text=f"Amount to Pay: RM {pricing['total']:.2f}",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 18, "bold")
    )
    
    # Payment method buttons
    panel = tk.Frame(root, bg=Config.PANEL_BG, padx=40, pady=40)
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 40, window=panel)
    
    # QR Payment
    qr_btn = tk.Button(
        panel,
        text="📱\nQR Code\n\nDuitNow • TouchNGo\nGrabPay",
        command=lambda: show_qr_payment(app, root, canvas, pricing),
        font=(Config.FONT_FAMILY, 14, "bold"),
        bg=Config.PRIMARY_COLOR,
        fg="black",
        activebackground=Config.SECONDARY_COLOR,
        relief="flat",
        width=20,
        height=8,
        cursor="hand2"
    )
    qr_btn.grid(row=0, column=0, padx=20, pady=10)
    
    # Card Payment
    card_btn = tk.Button(
        panel,
        text="💳\nCard\n\nVisa • Mastercard\nAmerican Express",
        command=lambda: show_card_payment(app, root, canvas, pricing),
        font=(Config.FONT_FAMILY, 14, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#66BB6A",
        relief="flat",
        width=20,
        height=8,
        cursor="hand2"
    )
    card_btn.grid(row=0, column=1, padx=20, pady=10)
    
    # Cash (coming soon)
    cash_btn = tk.Button(
        panel,
        text="💵\nCash\n\n(Coming Soon)",
        font=(Config.FONT_FAMILY, 14),
        bg="#666666",
        fg="#aaaaaa",
        relief="flat",
        width=20,
        height=8,
        state="disabled"
    )
    cash_btn.grid(row=1, column=0, padx=20, pady=10)
    
    # Membership (coming soon)
    member_btn = tk.Button(
        panel,
        text="⭐\nMembership\n\nPoints\n(Coming Soon)",
        font=(Config.FONT_FAMILY, 14),
        bg="#666666",
        fg="#aaaaaa",
        relief="flat",
        width=20,
        height=8,
        state="disabled"
    )
    member_btn.grid(row=1, column=1, padx=20, pady=10)
    
    # Back button
    create_back_button(
        panel,
        lambda: show_order_summary(app, root, canvas, pricing)
    ).grid(row=2, column=0, columnspan=2, pady=(20, 0))


def show_qr_payment(app, root, canvas, pricing: Dict):
    """Show QR code payment screen."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image
    from fitfuel_ui import Config, create_button
    
    clear_screen()
    draw_background(selection_bg_image)
    
    # Generate transaction ID
    transaction_id = f"FIT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Initialize payment processor
    processor = PaymentProcessor()
    processor.current_transaction = {
        'id': transaction_id,
        'amount': pricing['total'],
        'simulated_paid': False
    }
    
    # Generate QR code
    qr_image = processor.generate_qr_code(pricing['total'], transaction_id)
    qr_photo = ImageTk.PhotoImage(qr_image.resize((300, 300)))
    
    # Title
    canvas.create_text(
        Config.WIDTH // 2, 60,
        text=f"📱 SCAN QR TO PAY RM {pricing['total']:.2f}",
        fill="white",
        font=(Config.FONT_FAMILY, 22, "bold")
    )
    
    # QR Code
    qr_label = tk.Label(root, image=qr_photo, bg="black")
    qr_label.image = qr_photo  # Keep reference
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 - 40, window=qr_label)
    
    # Instructions
    instructions = [
        "Scan with:",
        "• Banking app (DuitNow QR)",
        "• TouchNGo eWallet",
        "• GrabPay"
    ]
    
    y_pos = Config.HEIGHT // 2 + 180
    for instruction in instructions:
        canvas.create_text(
            Config.WIDTH // 2, y_pos,
            text=instruction,
            fill="#dddddd" if instruction.startswith("•") else "white",
            font=(Config.FONT_FAMILY, 12, "bold" if not instruction.startswith("•") else "normal")
        )
        y_pos += 25
    
    # Timer and status
    timer_text = canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 300,
        text="⏱️ Time remaining: 5:00",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 13)
    )
    
    status_text = canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 330,
        text="Waiting for payment...",
        fill=Config.MUTED_TEXT,
        font=(Config.FONT_FAMILY, 12)
    )
    
    # Cancel button
    cancel_btn = tk.Button(
        root,
        text="Cancel Payment",
        command=lambda: show_payment_method_selection(app, root, canvas, pricing),
        font=(Config.FONT_FAMILY, 12),
        bg="#ff4444",
        fg="white",
        relief="flat",
        width=15,
        cursor="hand2"
    )
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT - 60, window=cancel_btn)
    
    # Demo: Simulate payment button (remove in production)
    demo_btn = tk.Button(
        root,
        text="[DEMO] Simulate Payment",
        command=lambda: [
            processor.simulate_payment_received(),
            show_payment_success(app, root, canvas, pricing, transaction_id)
        ],
        font=(Config.FONT_FAMILY, 10),
        bg="#FFA500",
        fg="black",
        relief="flat",
        width=20,
        cursor="hand2"
    )
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT - 100, window=demo_btn)
    
    # In production, poll payment status
    # def check_payment():
    #     status = processor.check_payment_status(transaction_id)
    #     if status['status'] == 'SUCCESS':
    #         show_payment_success(app, root, canvas, pricing, transaction_id)
    #     else:
    #         root.after(2000, check_payment)  # Check every 2 seconds
    # 
    # check_payment()


def show_card_payment(app, root, canvas, pricing: Dict):
    """Show card payment screen (placeholder - requires card reader hardware)."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image
    from fitfuel_ui import Config, create_button
    
    clear_screen()
    draw_background(selection_bg_image)
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 50,
        text="💳 CARD PAYMENT",
        fill="white",
        font=(Config.FONT_FAMILY, 24, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2,
        text="Please insert or tap your card",
        fill="#dddddd",
        font=(Config.FONT_FAMILY, 16)
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 40,
        text=f"Amount: RM {pricing['total']:.2f}",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 18, "bold")
    )
    
    # Demo button (in production, this waits for card reader)
    demo_btn = tk.Button(
        root,
        text="[DEMO] Simulate Card Payment",
        command=lambda: show_payment_success(
            app, root, canvas, pricing,
            f"CARD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        ),
        font=(Config.FONT_FAMILY, 12, "bold"),
        bg=Config.PRIMARY_COLOR,
        fg="black",
        relief="flat",
        width=25,
        cursor="hand2"
    )
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT // 2 + 100, window=demo_btn)
    
    # Back button
    back_btn = tk.Button(
        root,
        text="← Back",
        command=lambda: show_payment_method_selection(app, root, canvas, pricing),
        font=(Config.FONT_FAMILY, 11),
        bg="#444444",
        fg="white",
        relief="flat",
        width=10,
        cursor="hand2"
    )
    canvas.create_window(Config.WIDTH // 2, Config.HEIGHT - 60, window=back_btn)


def show_payment_success(app, root, canvas, pricing: Dict, transaction_id: str):
    """Show payment success screen."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image
    from fitfuel_ui import Config
    
    clear_screen()
    draw_background(selection_bg_image)
    
    # Success icon
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 100,
        text="✅",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 72)
    )
    
    # Success message
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2,
        text="PAYMENT SUCCESSFUL!",
        fill="white",
        font=(Config.FONT_FAMILY, 28, "bold")
    )
    
    # Transaction details
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 50,
        text=f"Transaction ID: #{transaction_id}",
        fill=Config.MUTED_TEXT,
        font=(Config.FONT_FAMILY, 12)
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 75,
        text=f"Amount Paid: RM {pricing['total']:.2f}",
        fill=Config.MUTED_TEXT,
        font=(Config.FONT_FAMILY, 12)
    )
    
    # Preparing message
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 130,
        text="Preparing your protein bar...",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 14)
    )
    
    # Log transaction
    logging.info(f"Payment successful: {transaction_id}, Amount: RM {pricing['total']:.2f}")
    
    # After 3 seconds, go to dispensing screen
    root.after(3000, lambda: show_dispensing_screen(app, root, canvas))


def show_dispensing_screen(app, root, canvas):
    """Show dispensing progress (enhanced version)."""
    from fitfuel_ui import clear_screen, draw_background, selection_bg_image, Config, start_slideshow
    
    clear_screen()
    draw_background(selection_bg_image)
    
    # Title
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 - 50,
        text="⬇️ DISPENSING",
        fill=Config.PRIMARY_COLOR,
        font=(Config.FONT_FAMILY, 32, "bold")
    )
    
    canvas.create_text(
        Config.WIDTH // 2, Config.HEIGHT // 2 + 20,
        text="Please wait while your bar is prepared...",
        fill="white",
        font=(Config.FONT_FAMILY, 16)
    )
    
    # Simulate dispensing time then reset
    root.after(5000, start_slideshow)


# Export functions to be used in fitfuel_ui.py
__all__ = [
    'PaymentConfig',
    'PricingCalculator', 
    'PaymentProcessor',
    'show_order_summary',
    'show_payment_method_selection',
    'show_qr_payment',
    'show_card_payment',
    'show_payment_success',
    'show_dispensing_screen'
]
'''