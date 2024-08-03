# Fault-Tolerant 2-Phase Commit Protocol - Part 2

This part of the project focuses on the scenario where the transaction coordinator does not receive a "yes" from a node. The transaction should be aborted, and "abort" messages should be sent to all participants.

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
   cd Part2
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

1. Participant Refusal:
   - One or more participants should respond with "Abort" when the "prepare" message is received.
   - The coordinator should handle this by sending "abort" messages to all participants.

## Expected Output

- Participants respond with "Abort" and the coordinator aborts the transaction.
- All participants receive the abort decision and finalize accordingly.
