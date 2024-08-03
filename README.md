# Fault-Tolerant 2-Phase Commit Protocol

This repository contains an implementation of the Fault-Tolerant 2-Phase Commit (2PC) Protocol using Python. The 2PC protocol is crucial for ensuring consistency in distributed systems, where transactions must be processed atomically across multiple nodes.

## Project Overview

The project is divided into four parts, each addressing different failure scenarios within the 2PC protocol:

1. **Part 1:** Handles coordinator failure before sending the "prepare" message.
2. **Part 2:** Ensures transactions are aborted if the coordinator does not receive "yes" from all nodes.
3. **Part 3:** Manages coordinator failure after sending the "commit" message to some participants.
4. **Part 4:** Deals with participant failure after replying "yes" to the coordinator.

## Requirements

- **Python 3.x**
- **Standard Libraries:** `socket`, `multiprocessing`, `time`, `json`, `os`, `sys`

## Repository Structure

- `Part1/`
  - `server.py`
  - `coordinator.py`
  - `participant.py`
  - `README.md`
- `Part2/`
  - `server.py`
  - `coordinator.py`
  - `participant.py`
  - `README.md`
- `Part3/`
  - `server.py`
  - `coordinator.py`
  - `participant.py`
  - `README.md`
- `Part4/`
  - `server.py`
  - `coordinator.py`
  - `participant.py`
  - `README.md`
- `Report.pdf`

## Setup and Execution

1. **Clone the Repository**

   Begin by cloning the repository to your local machine:

   ```bash
   git clone [your-repository-url]
   cd [repository-folder]

Navigate to the Desired Part

Enter the directory for the part you wish to execute:

bash

cd Part1  # or Part2, Part3, Part4

2. **Run the Server**

  Open a terminal window and execute the following command to start the server:

  ```bash
  python3 server.py
  ```
  Enter the number of participants when prompted.

3. **Run the Coordinator**

  Open another terminal window and execute:

  ```bash
  python3 coordinator.py
  ```
  
  Follow the prompts to initiate transactions.

4. **Run Participants**

  For each participant, open a new terminal window and execute:

  ```bash
  python3 participant.py <participant_index>
  ```

  Replace <participant_index> with the participant number (e.g., 1, 2).

## Execution Example

Here is an example of executing Part 1:

1. **Start the Server:**
  
    ```bash
    python3 server.py
    ```
    
    Enter 2 when prompted for the number of participants.

2. **Start the Coordinator:**

    ```bash
    python3 coordinator.py
    ```

3. **Start Participant 1:**

    ```bash
    python3 participant.py 1
    ```

4. **Start Participant 2:**

    ```bash
    python3 participant.py 2
    ```
    
5. **Initiate Transaction:**

    On the coordinator's terminal, you can type "prepare" to start the transaction process and test the system's response to failures as implemented.

## Project Report

For detailed information about the project, implementation, lessons learned, and issues encountered, refer to [Report](https://github.com/vinodpgowda/Fault-Tolerant-2PC-Protocol/blob/main/Report.pdf) included in the repository.
