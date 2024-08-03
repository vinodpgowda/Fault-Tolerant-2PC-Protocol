# Fault-Tolerant 2-Phase Commit Protocol - Part 1

This part of the project demonstrates the 2PC protocol with a focus on handling coordinator failure before sending the "prepare" message. The nodes should time out, abort, and respond with "no" when the coordinator comes back up and sends the "prepare" message.

## Requirements

- **Python 3.x**
- **Standard Libraries:** `socket`, `multiprocessing`, `time`, `json`, `os`, `sys`

## File Structure

- `server.py`: Manages connections and communication between the coordinator and participants.
- `coordinator.py`: Simulates the transaction coordinator, sending prepare messages and handling responses.
- `participant.py`: Simulates participants that receive messages and respond to the coordinator.

## Setup and Execution

1. **Clone the Repository**

   ```bash
   cd Part1
   ```

2. **Run the Server**

   Open a terminal window and execute:

   ```bash
   python3 server.py
   ```

   Enter the number of participants when prompted.

3. **Run the Coordinator**

   Open another terminal window and execute:

   ```bash
   python3 coordinator.py
   ```

   Follow prompts to initiate transactions.

4. **Run Participants**

   For each participant, open a new terminal window and execute:

   ```bash
   python3 participant.py <participant_index>
   ```

   Replace <participant_index> with the participant number (e.g., 1, 2).

## Testing Scenario

1. Coordinator Failure:
   - Introduce a delay before sending the prepare message in the coordinator to simulate failure.
   - Observe that participants time out and abort, then properly respond once the coordinator restarts.

## Expected Output

- Participants should initially time out and abort the transaction.
- Upon coordinator recovery, participants should handle the "prepare" message and respond correctly.
