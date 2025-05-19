# Inventory Management System

This application allows you to manage an inventory with different roles and permissions, ensuring that only authorized users can perform specific actions (like adding, editing, and deleting items). It also has a natural language search feature.

## How to Use the Application:

### 1. **Create Users and Assign Roles**
   - The `UserManager` class is used to create users and assign them roles (`admin`, `manager`, `user`).
   - Use the `add_user(username, password, role)` method to create new users.

### 2. **Log In**
   - Use the `login(username, password)` method to log in as an existing user.
   - Once logged in, the system will remember your current session and you can perform actions based on your role.

### 3. **Perform Actions on Inventory**
   Depending on your role, you can perform different actions on the inventory:
   
   - **Admin**: Can add, edit, delete, and view items.
   - **Manager**: Can add, edit, and view items, but cannot delete items.
   - **User**: Can only view items.

   Each action is tied to a specific permission. The following methods are available to interact with inventory items:

   - `add_item(item)`: Adds a new item to the inventory.
   - `edit_item(item_id, name=None, qty=None, price=None, category=None)`: Edits an existing item by its ID.
   - `delete_item(item_id)`: Deletes an item by its ID.
   - `find_item(name=None, status=None, min_price=None, max_price=None, min_quantity=None, max_quantity=None, category=None)`: Finds details of items by specifying the attributes wanting to be matched.

### 4. **Log Out**
   - Use the `logout()` method to log out of the current session. Once logged out, you will not be able to perform any actions until you log in again.

### Example Usage:

```python
user_manager = UserManager()
user_manager.add_user("admin", "admin_pass", Role.ADMIN)
user_manager.add_user("manager", "manager_pass", Role.MANAGER)
user_manager.add_user("user", "user_pass", Role.USER)

inventory = Inventory(user_manager)

# Admin:
user_manager.login("admin", "admin_pass")
inventory.add_item(Item(1, "Laptop", 10, 999.99, "Tech"))  
inventory.add_item(Item(3, "Monitor", 0, 120.99, "Displays", ItemStatus.DISCONTINUED))
inventory.delete_item(1)  # Admin can delete items
user_manager.logout()

# Manager:
user_manager.login("manager", "manager_pass")
inventory.add_item(Item(2, "Mouse", 15, 19.99, "Accessories"))  # Manager can add items
inventory.natural_language_search("Show me discontinued items in tech category")
inventory.delete_item(2)  # Manager cannot delete items
user_manager.logout()

# User:
user_manager.login("user", "user_pass")
user_manager.logout()
