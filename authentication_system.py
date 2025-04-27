# Pre-set valid badge IDs and PINs for demonstration
valid_credentials = {
    "12345": "4321",  # badge_id: pin
    "67890": "9876"
}

# Log file to record access attempts
log_file = "access_log.txt"

# Function to log access attempts
def log_attempt(badge_id, pin_entered, result):
    with open(log_file, "a") as f:
        f.write(f"Badge ID: {badge_id}, PIN Entered: {pin_entered}, Result: {result}\n")

# Main authentication function
def authenticate():
    print("Welcome to Helix Kitten Multi-Step Authentication System")

    badge_id = input("Please scan your badge (enter Badge ID): ")

    if badge_id in valid_credentials:
        pin = input("Please enter your PIN: ")
        if pin == valid_credentials[badge_id]:
            print("Access Granted. Welcome!")
            log_attempt(badge_id, pin, "Access Granted")
        else:
            print("Access Denied: Incorrect PIN.")
            log_attempt(badge_id, pin, "Access Denied: Incorrect PIN")
    else:
        print("Access Denied: Invalid Badge.")
        log_attempt(badge_id, "N/A", "Access Denied: Invalid Badge")

if __name__ == "__main__":
    authenticate()
