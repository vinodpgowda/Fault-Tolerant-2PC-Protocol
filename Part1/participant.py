import socket
import sys
import json
import os
import time


def save_message_to_file(message, file_path):
    """Saves a message to a text file."""
    with open(file_path, "a") as file:
        file.write(f"{message}\n")


def find_transaction(transactions, transaction_id):
    """Finds a transaction by its ID."""
    for transaction in transactions:
        if transaction.get("transaction_id") == transaction_id:
            return transaction
    return None


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


def handle_incoming_messages(participant_index):
    transaction_file = f"participant_{participant_index}_transactions.json"
    auto_abort = False
    transaction_completed = False

    while True:
        try:
            message = participant_socket.recv(1024).decode()
            print(f"Participant {participant_index} received message: {message}")

            if message.startswith("Decision:") or message.startswith(
                "RequestDecision:"
            ):
                is_resend_decision = message.startswith("RequestDecision:")
                if is_resend_decision:
                    message = message.replace("RequestDecision:Decision:", "Decision:")

                try:
                    decision_transaction_id, decision = (
                        message.split(";")[0].split(":")[1],
                        message.split(";")[1].split(":")[1],
                    )
                except IndexError:
                    print("Error: Received malformed decision message.")
                    continue

                transactions = load_transactions(transaction_file)
                transaction_data = find_transaction(
                    transactions, decision_transaction_id
                )

                if transaction_data is not None and (
                    is_resend_decision or transaction_data["status"] == "pending"
                ):
                    if transaction_data["status"] != "done":
                        transaction_data["decision"] = decision

                        if decision == "Commit":
                            if transaction_data["status"] == "pending":
                                message_file = f"participant_{participant_index}.txt"
                                save_message_to_file(
                                    transaction_data["message"], message_file
                                )
                                print("Message saved to text file.")
                        elif decision == "Abort":
                            print("Transaction aborted.")

                        transaction_data["status"] = "done"
                        save_transactions(transactions, transaction_file)
                        time.sleep(1)
                        participant_socket.sendall(
                            f"{participant_index}:done\n".encode()
                        )
                        print(f"Sent {participant_index}:done to coordinator")
                        transaction_completed = True
                    else:
                        print("Transaction is already complete. Skipping.")

                    if decision == "Commit":
                        print("Transaction committed.")
                    elif decision == "Abort":
                        print("Transaction aborted.")

                else:
                    print("Transaction is already handled or does not exist.")
                    print(f"Transaction ID: {decision_transaction_id}")

            else:
                if ";" not in message:
                    print(f"Received malformed message from coordinator: {message}")
                    continue

                transaction_id, received_message = message.split(";", 1)

                transaction_data = {
                    "transaction_id": transaction_id,
                    "message": received_message,
                }

                if not auto_abort:
                    response = "Abort"  # For Part 1, automatically respond with "Abort"
                else:
                    response = "Abort"

                transaction_data["response"] = response
                transaction_data["status"] = "pending"

                transactions = load_transactions(transaction_file)
                transactions.append(transaction_data)
                save_transactions(transactions, transaction_file)

                reply_with_index = f"{participant_index}:{response}\n"
                print("Transaction information stored in JSON file.")
                participant_socket.sendall(reply_with_index.encode())

        except socket.timeout:
            if transaction_completed:
                print("Transaction completed, no further actions needed.")
                break
            elif auto_abort:
                print("Coordinator timed out again. Continuing to wait for recovery...")
            else:
                print("Coordinator timed out. Aborting transaction.")
                auto_abort = True
            time.sleep(5)


def start_participant(participant_index):
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12346

    global participant_socket
    participant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    participant_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Participant {participant_index} connected to the server.")

    participant_socket.settimeout(30)

    try:
        handle_incoming_messages(participant_index)
    finally:
        participant_socket.close()
        print(f"Participant {participant_index} socket closed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing participant index as a command-line argument.")
        print("Usage: python3 participant.py <participant_index>")
        sys.exit(1)

    participant_index = int(sys.argv[1])
    start_participant(participant_index)
