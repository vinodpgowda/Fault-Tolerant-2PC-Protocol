import socket
import time
import uuid
import json
import os


def load_transactions(file_path):
    """Loads transactions from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_transactions(transactions, file_path):
    """Saves transactions to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(transactions, file, indent=2)


def update_transaction_status(transaction_id, key, value, file_path):
    """Updates the status of a specific transaction."""
    transactions = load_transactions(file_path)
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            transaction[key] = value
            break
    save_transactions(transactions, file_path)


def is_transaction_pending(transaction_id, file_path):
    """Checks if a transaction is still pending."""
    transactions = load_transactions(file_path)
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            return transaction["status"] == "pending"
    return False


def main():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12346
    TRANSACTION_LOG = "coordinator_transactions.json"

    coordinator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coordinator_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the server.")

    # Expect to receive the number of participants first
    num_participants_message = coordinator_socket.recv(1024).decode()
    try:
        num_participants = int(num_participants_message)
        print(f"Number of participants: {num_participants}")
    except ValueError:
        print(
            f"Unexpected message from server (expected number of participants): {num_participants_message}"
        )
        return  # Exit if we don't receive the expected message

    # Wait for the confirmation message
    ready_message = coordinator_socket.recv(1024).decode()
    if ready_message == "All participants connected":
        print("All participants are connected.")

    while True:
        user_message = input(
            "Enter a message to send to the participants (type 'exit' to quit): "
        )

        if user_message.lower() == "exit":
            coordinator_socket.sendall("exit".encode())
            break

        # Creating a unique transaction ID and preparing the message
        transaction_id = str(uuid.uuid4())

        # Simulate coordinator failure by delaying the prepare message
        print("Simulating coordinator delay before sending 'prepare' message...")
        time.sleep(35)  # Delay longer than participants' timeout (30 seconds)

        prepare_message = f"{transaction_id};prepare"
        print(f"Sending prepare message: {prepare_message}")
        coordinator_socket.sendall(prepare_message.encode())

        transaction = {
            "transaction_id": transaction_id,
            "message": user_message,
            "status": "pending",
        }

        transactions = load_transactions(TRANSACTION_LOG)
        transactions.append(transaction)
        save_transactions(transactions, TRANSACTION_LOG)

        coordinator_socket.settimeout(30)

        abort = False
        replies_received = 0
        while replies_received < num_participants:
            try:
                replies = coordinator_socket.recv(1024).decode()
                # Split concatenated replies
                individual_replies = replies.strip().split("\n")  # Split by newline

                for reply in individual_replies:
                    if not reply.strip():
                        continue

                    print(
                        f"Coordinator received reply: {reply}"
                    )  # Log incoming replies

                    participant_index, response = reply.split(":", 1)
                    replies_received += 1

                    print(f"Participant {participant_index} response: {response}")

                    if "Abort" in response:
                        abort = True
                        break

            except socket.timeout:
                abort = True
                print(
                    "Coordinator timed out waiting for replies. Aborting transaction."
                )
                break

        decision = "Abort" if abort else "Commit"
        decision_message = f"Decision:{transaction_id};Decision:{decision}"
        print(f"Coordinator decision: {decision_message}")  # Log decision message
        coordinator_socket.sendall(decision_message.encode())

        update_transaction_status(transaction_id, "decision", decision, TRANSACTION_LOG)

        # Handle potential coordinator failure and recovery
        resend_decision = False
        time.sleep(5)
        print("Coordinator restarting...")
        if is_transaction_pending(transaction_id, TRANSACTION_LOG):
            print("Resending decision message.")
            resend_decision_message = (
                f"RequestDecision:{transaction_id};Decision:{decision}"
            )
            coordinator_socket.sendall(resend_decision_message.encode())
            resend_decision = True

        done_replies = 0
        while done_replies < num_participants:
            try:
                replies = coordinator_socket.recv(1024).decode()
                individual_done_replies = replies.strip().split(
                    "\n"
                )  # Split by newline

                for done_reply in individual_done_replies:
                    if not done_reply.strip():
                        continue

                    print(
                        f"Coordinator received done reply: {done_reply}"
                    )  # Log done replies

                    participant_index, response = done_reply.split(":", 1)
                    if response.endswith(":done"):
                        done_replies += 1
                        print(f"Participant {participant_index} completed transaction.")
            except socket.timeout:
                print("Coordinator timed out waiting for 'done' replies.")
                break

        update_transaction_status(transaction_id, "status", "done", TRANSACTION_LOG)

        time.sleep(2)
        print("Transaction aborted." if abort else "Transaction committed.")

    coordinator_socket.close()


if __name__ == "__main__":
    main()
