# Fault-Tolerant 2-Phase Commit Protocol - Part 4

This part of the project demonstrates the 2PC protocol with a focus on handling participant node failure after replying "yes" to the transaction coordinator (TC). Each participant must save transaction information to disk before replying "yes" and be able to recover the transaction state from the TC after a failure.

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
   cd Part4
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

4. Run Participants

   For each participant, open a new terminal window and execute:

   ```bash
   python3 participant.py <participant_index>
   ```

   Replace <participant_index> with the participant number (e.g., 1, 2).

## Testing Scenario

1. Participant Failure After Yes:
   - Each participant saves transaction data before replying "yes
   - Simulate a failure at a participant node after it replies "yes."
   - Upon recovery, the participant requests the transaction status from the coordinator.

## Expected Output

- Participants save transaction data to disk before replying "yes."
- After recovery, participants can request the transaction status from the coordinator.
- The transaction is completed successfully with all nodes in agreement.
