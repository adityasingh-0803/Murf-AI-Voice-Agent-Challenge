class CommerceState:
    def __init__(self):
        # cart = { sku: qty }
        self.cart = {}

    def add_item(self, sku, qty):
        if sku in self.cart:
            self.cart[sku] += qty
        else:
            self.cart[sku] = qty

    def remove_item(self, sku):
        if sku in self.cart:
            del self.cart[sku]

    def clear(self):
        self.cart = {}

    def summary(self, catalog):
        if not self.cart:
            return "Your cart is empty."

        lines = ["🛍️ Your current cart:"]
        total = 0
        for sku, qty in self.cart.items():
            item = catalog.get(sku)
            if not item:
                continue
            name = item["name"]
            price = item["price"]
            subtotal = price * qty
            total += subtotal
            lines.append(f"- {name} (x{qty}) — ₹{subtotal}")

        lines.append(f"\nTotal payable: ₹{total}")
        return "\n".join(lines)
