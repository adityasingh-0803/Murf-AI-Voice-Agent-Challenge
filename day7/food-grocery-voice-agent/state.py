class OrderState:
    def __init__(self):
        self.cart = {}

    def add_item(self, item, qty):
        if item in self.cart:
            self.cart[item] += qty
        else:
            self.cart[item] = qty

    def remove_item(self, item):
        if item in self.cart:
            del self.cart[item]

    def summary(self):
        if not self.cart:
            return "Your cart is currently empty."
        s = "🛒 Here is your order summary:\n"
        for item, qty in self.cart.items():
            s += f"- {item}: {qty}\n"
        return s
