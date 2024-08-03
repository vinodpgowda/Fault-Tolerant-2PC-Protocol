import socket
from multiprocessing import Process, Queue


class DistributedServer:
    def __init__(self, server_ip="127.0.0.1", server_port=12346):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = None
        self.coordinator_socket = None
        self.participants = []
        self.participant_message_queues = []

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Enable address reuse
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print("Server is listening for connections...")

        # Accept coordinator connection
        self.coordinator_socket, _ = self.server_socket.accept()
        print("Coordinator connected.")

        # Prompt for number of participants after coordinator connects
        participant_count = int(input("Enter the number of participants: "))
        print(f"Waiting for {participant_count} participant(s) to connect...")

        # Send the number of participants to the coordinator first
        self.coordinator_socket.sendall(str(participant_count).encode())

        # Accept participant connections
        for i in range(participant_count):
            participant_socket, _ = self.server_socket.accept()
            print(f"Participant {i + 1} connected.")
            self.participants.append(participant_socket)

        # Send confirmation that all participants are connected
        self.coordinator_socket.sendall(b"All participants connected")

        # Create message queues for each participant
        self.participant_message_queues = [Queue() for _ in range(participant_count)]

        # Start a process for the coordinator
        coordinator_process = Process(target=self.handle_coordinator)
        coordinator_process.start()

        # Start processes for each participant
        participant_processes = []
        for i, participant_socket in enumerate(self.participants):
            process = Process(
                target=self.handle_participant,
                args=(participant_socket, i + 1, self.participant_message_queues[i]),
            )
            process.start()
            participant_processes.append(process)

        # Wait for all processes to complete
        for process in participant_processes:
            process.join()

        coordinator_process.join()

        # Close all participant sockets
        for participant_socket in self.participants:
            participant_socket.close()

        self.server_socket.close()

    def handle_participant(self, participant_socket, participant_index, message_queue):
        """Handles communication with a single participant."""
        participant_socket.settimeout(30)  # Set timeout for participant responses

        while True:
            try:
                # Retrieve message from the queue
                message = message_queue.get()
                if message is None:
                    print(f"Participant {participant_index} shutting down.")
                    break  # Exit if None is received (shutdown signal)

                participant_socket.sendall(
                    message.encode()
                )  # Send message to participant
                done_received = False

                while not done_received:
                    try:
                        response = participant_socket.recv(1024).decode()

                        # If we get an empty response, it indicates the socket is closed
                        if not response:
                            print(
                                f"Participant {participant_index} closed the connection."
                            )
                            return

                        if response.startswith("RequestDecision:"):
                            decision_message = response.replace("RequestDecision:", "")
                            message_queue.put(decision_message)
                        else:
                            reply = f"{participant_index}:{response}"
                            print(
                                f"Sending reply from participant {participant_index} to coordinator: {reply}"
                            )
                            # Correctly use the class member `self.coordinator_socket`
                            self.coordinator_socket.sendall(reply.encode())

                            if response.endswith(":done"):
                                done_received = True
                    except socket.timeout:
                        print(
                            f"Participant {participant_index} timed out waiting for responses."
                        )
                        break
                    except ConnectionResetError:
                        print(
                            f"Participant {participant_index} connection reset by peer."
                        )
                        return
                    except Exception as e:
                        print(
                            f"Error receiving response from participant {participant_index}: {e}"
                        )
                        return

            except Exception as e:
                print(f"Error processing participant {participant_index}: {e}")
                break

        participant_socket.close()

    def handle_coordinator(self):
        """Handles communication with the coordinator."""
        try:
            while True:
                message = self.coordinator_socket.recv(1024).decode()
                if not message:
                    print("Coordinator closed the connection.")
                    break  # Break on empty message (shutdown signal)

                # Forward only transaction messages to participants
                if (
                    message.startswith("Decision:")
                    or message.startswith("RequestDecision:")
                    or ";" in message
                ):
                    for queue in self.participant_message_queues:
                        queue.put(message)  # Send decision to all participants

        except Exception as e:
            print(f"Error receiving message from coordinator: {e}")
        finally:
            self.coordinator_socket.close()


if __name__ == "__main__":
    server = DistributedServer()
    server.start_server()
