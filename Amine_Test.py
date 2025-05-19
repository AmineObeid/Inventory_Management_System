import re

class Role:
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class Permission:
    ADD_ITEM = "add_item"
    EDIT_ITEM = "edit_item"
    DELETE_ITEM = "delete_item"
    VIEW_ITEM = "view_item"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  
        self.role = role

    def __str__(self):
        return f"{self.username} ({self.role})"

class UserManager:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, username, password, role):
        if username not in self.users:
            self.users[username] = User(username, password, role)
        else:
            print(f"User {username} already exists.")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print(f"Logged in as {self.current_user}")
        else:
            print("Invalid credentials.")

    def logout(self):
        print(f"Logged out from {self.current_user.username}")
        self.current_user = None

class RolePermissions:
    permissions = {
        Role.ADMIN: [Permission.ADD_ITEM, Permission.EDIT_ITEM, Permission.DELETE_ITEM, Permission.VIEW_ITEM],
        Role.MANAGER: [Permission.ADD_ITEM, Permission.EDIT_ITEM, Permission.VIEW_ITEM],
        Role.USER: [Permission.VIEW_ITEM]
    }

    def has_permission(role, permission):
        return permission in RolePermissions.permissions.get(role, [])

class Inventory:
    def __init__(self, user_manager):
        self.items = {}
        self.user_manager = user_manager
    
    def add_item(self, item):
        if not self._has_permission(Permission.ADD_ITEM):
            print("You don't have permission to add items.")
            return
        if item.item_id in self.items:
            print(f"Item ID {item.item_id} already exists.")
        else:
            self.items[item.item_id] = item
            print(f"Item {item.name} added.")
    
    def edit_item(self, item_id, name=None, quantity=None, price=None, category=None, status=None):
        if not self._has_permission(Permission.EDIT_ITEM):
            print("You don't have permission to edit items.")
            return
        item = self.items.get(item_id)
        if item:
            item.update(name, quantity, price, category, status)
            print(f"Item ID {item_id} updated.")
        else:
            print(f"Item ID {item_id} not found.")

    def delete_item(self, item_id):
        if not self._has_permission(Permission.DELETE_ITEM):
            print("You don't have permission to delete items.")
            return
        if item_id in self.items:
            del self.items[item_id]
            print(f"Item ID {item_id} deleted.")
        else:
            print(f"Item ID {item_id} not found.")

    def list_inventory(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            for item in self.items.values():
                print(item)
    
    def find_items(self, name=None, status=None, min_price=None, max_price=None, min_quantity=None, max_quantity=None, category=None):
        if not self._has_permission(Permission.VIEW_ITEM):
            print("You don't have permission to view items.")
            return
        results = []
        for item in self.items.values():
            if name and name.lower() not in item.name.lower():
                continue
            if status and item.status != status:
                continue
            if min_price is not None and item.price < min_price:
                continue
            if max_price is not None and item.price > max_price:
                continue
            if min_quantity is not None and item.quantity < min_quantity:
                continue
            if max_quantity is not None and item.quantity > max_quantity:
                continue
            if category and item.category != category:
                continue
            results.append(item)

        if not results:
            print("No matching items found.")
        else:
            for item in results:
                print(item)
            
    def _has_permission(self, permission):
        if self.user_manager.current_user:
            return RolePermissions.has_permission(self.user_manager.current_user.role, permission)
        print("No user logged in.")
        return False

    def natural_language_search(self, query):
        query = query.lower()

        filters = {
            "status": None,
            "min_price": None,
            "max_price": None,
            "category": None,
            "logical_conditions": [],
        }

        status_map = {
            "in stock": ItemStatus.IN_STOCK,
            "low stock": ItemStatus.LOW_STOCK,
            "ordered": ItemStatus.ORDERED,
            "discontinued": ItemStatus.DISCONTINUED
        }

        for status, enum in status_map.items():
            if status in query:
                filters["status"] = enum

        match_under = re.search(r"under\s?\$?(\d+)", query)
        match_over = re.search(r"over\s?\$?(\d+)", query)
        match_between = re.search(r"between\s?\$?(\d+)\s?and\s?\$?(\d+)", query)

        if match_under:
            filters["max_price"] = float(match_under.group(1))
        if match_over:
            filters["min_price"] = float(match_over.group(1))
        if match_between:
            filters["min_price"] = float(match_between.group(1))
            filters["max_price"] = float(match_between.group(2))

        match_category = re.search(r"category\s+([a-zA-Z\s]+)", query)
        if match_category:
            filters["category"] = match_category.group(1).strip()

        if 'and' in query:
            filters["logical_conditions"].append('and')
        if 'or' in query:
            filters["logical_conditions"].append('or')

        results = self._apply_filters(filters)

        if results:
            for item in results:
                print(item)
        else:
            print("No items matched your search.")

    def _apply_filters(self, filters):
        results = []

        for item in self.items.values():
            match = True

            if filters["status"] and item.status != filters["status"]:
                match = False

            if filters["category"] and filters["category"].lower() not in item.category.lower():
                match = False

            if filters["min_price"] is not None and item.price < filters["min_price"]:
                match = False
            if filters["max_price"] is not None and item.price > filters["max_price"]:
                match = False

            if match:
                results.append(item)

        return results


class ItemStatus:
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    ORDERED = "Ordered"
    DISCONTINUED = "Discontinued"

class Item:
    def __init__(self, item_id, name, quantity, price, category, status=None):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.status = status if status else self.calculate_status()


    def calculate_status(self):
        # if self.status == ItemStatus.DISCONTINUED:
        #     return ItemStatus.DISCONTINUED
        if self.quantity == 0:
            return ItemStatus.ORDERED
        elif self.quantity < 5:
            return ItemStatus.LOW_STOCK
        else:
            return ItemStatus.IN_STOCK

    def update(self, name=None, quantity=None, price=None, category=None, status=None):
        if name is not None:
            self.name = name
        if quantity is not None:
            self.quantity = quantity
        if price is not None:
            self.price = price
        if self.category is not None:
            self.category = category
        if status is not None:
            self.status = status
        else:
            self.status = self.calculate_status()

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Qty: {self.quantity}, Price: ${self.price:.5f}, Category: {self.category}, Status: {self.status}"

