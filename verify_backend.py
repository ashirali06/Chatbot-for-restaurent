from backend import ChatbotBackend
from data import DataManager
import os

def test_verification():
    print("--- Starting Verification ---")
    
    # 1. Test Backend Routing
    backend = ChatbotBackend()
    
    # Test Menu
    msg = "Can I see the menu?"
    response = backend.process_message(msg)
    if "Chicken Biryani" in response:
        print("[PASS] Menu Retrieval")
    else:
        print(f"[FAIL] Menu Retrieval: {response[:50]}...")

    # Test FAQ
    msg = "Is the food halal?"
    response = backend.process_message(msg)
    if "Yes, all our meat is 100% Halal certified" in response:
        print("[PASS] FAQ Retrieval")
    else:
        print(f"[FAIL] FAQ Retrieval: {response[:50]}...")

    # 2. Test Data Persistence (Admin Simulation)
    data = DataManager()
    menu = data.get_menu()
    
    # Add new item
    print("--- Testing Data Update ---")
    new_item = {"name": "Test Burger", "price": 9.99, "description": "A test burger", "available": True}
    if "Starters" in menu:
        menu["Starters"].append(new_item)
        data.save_menu(menu)
        print("Item added.")
        
        # Verify it shows up in backend
        response_update = backend.process_message("show menu")
        if "Test Burger" in response_update:
            print("[PASS] Admin Update Persistence")
        else:
            print("[FAIL] Admin Update Persistence")
            
        # Clean up
        menu["Starters"] = [i for i in menu["Starters"] if i["name"] != "Test Burger"]
        data.save_menu(menu)
        print("Item removed (Cleanup).")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    test_verification()
