# Fault-Tolerant 2-Phase Commit Protocol - Part 3

This part of the project demonstrates the 2PC protocol with a focus on handling transaction coordinator (TC) failure after sending a "commit" message. The TC must commit the transaction to disk before sending commit messages to the participants. In the event of a coordinator failure, it will resend commit messages to any participants who did not receive them after recovery.

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
   cd Part3
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

1. Coordinator Failure After Commit:
   - Simulate a failure in the coordinator after sending a commit to some participants.
   - The coordinator should resend commit messages to participants who did not receive them upon recovery.

## Expected Output

- The coordinator commits to disk before sending the commit message.
- On recovery, the coordinator resends commit messages to any participants that missed it.
