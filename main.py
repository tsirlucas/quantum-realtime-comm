from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

import threading
import time

# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

# Lets consider qubits per second as consumption/creation speed
def quantum_teleportation(NUMBER_OF_QUBITS, EMITTER_SPEED, RECEIVER_SPEED, BUFFERING_SIZE):
    run = True
    buffered_qubits = 0 # time measured in seconds
    ping_history = []
    # Initialize circuit with qubits set to the |0⟩ state
    qr = QuantumRegister(NUMBER_OF_QUBITS, name="q")
    receiver = ClassicalRegister(NUMBER_OF_QUBITS, name="receiver")
    teleportation_circuit = QuantumCircuit(qr, receiver)

    default_stop = (NUMBER_OF_QUBITS / 2) - 1
    
    def entangle_and_send():
        nonlocal buffered_qubits, run
        waiting_to_send_qubit = 0
        stop_at_qubit = default_stop if EMITTER_SPEED > NUMBER_OF_QUBITS else int((EMITTER_SPEED + waiting_to_send_qubit) - 1)
        # At this point, lets say odd qubits are emitters qubits and even qubits are receivers qubits
        while run:
           if waiting_to_send_qubit < NUMBER_OF_QUBITS - 1:
                # Entangling qubits in pairs
                stop = stop_at_qubit if stop_at_qubit <= NUMBER_OF_QUBITS - 1 else NUMBER_OF_QUBITS - 1
                processed_qubits = len(range(waiting_to_send_qubit, stop))
                print('sending: ', range(waiting_to_send_qubit, stop), processed_qubits, buffered_qubits)
                for qubit in range(waiting_to_send_qubit, stop):
                    if qubit % 2 == 0 & qubit < NUMBER_OF_QUBITS:
                        teleportation_circuit.h(qubit)
                        teleportation_circuit.cx(qubit, stop + 1)
                
                buffered_qubits = buffered_qubits + EMITTER_SPEED
                waiting_to_send_qubit = stop + 1
                stop_at_qubit = stop_at_qubit + processed_qubits + 1
                time.sleep(1)

    # At this point we start filling the buffer BUFFERING_SIZE
    buffered_qubits = buffered_qubits + BUFFERING_SIZE
    entangle_and_send_thread = threading.Thread(target=entangle_and_send, name="entangle_and_send")
    entangle_and_send_thread.start()

    def receive_flip_and_read():
        nonlocal buffered_qubits, run
        received_qubits = 0
        waiting_to_read_qubit = 0
        stop_at_qubit = buffered_qubits - 1 if RECEIVER_SPEED > buffered_qubits else int((RECEIVER_SPEED + waiting_to_read_qubit) / 2)
        while received_qubits < NUMBER_OF_QUBITS:
            if (buffered_qubits >= RECEIVER_SPEED) | (received_qubits + buffered_qubits >= NUMBER_OF_QUBITS):
                processing_qubits = (buffered_qubits if RECEIVER_SPEED > buffered_qubits else RECEIVER_SPEED) - 1
                received_qubits = received_qubits + processing_qubits
                # reading qubits
                stop = waiting_to_read_qubit + processing_qubits if waiting_to_read_qubit + processing_qubits < NUMBER_OF_QUBITS else NUMBER_OF_QUBITS - 1
                processed_qubits = len(range(waiting_to_read_qubit, stop))
                print('receiving: ', range(waiting_to_read_qubit, stop), processed_qubits, buffered_qubits)
                for qubit in range(waiting_to_read_qubit, stop):
                    # only flips even indexed qubits
                    if qubit % 2 == 0 & qubit < NUMBER_OF_QUBITS:
                        teleportation_circuit.x(qubit)

                waiting_to_read_qubit = stop + 1
                buffered_qubits = buffered_qubits - processing_qubits
                stop_at_qubit = stop_at_qubit + processed_qubits - 1
                ping_history.append(0)
            else:
                ping_history.append(1)
            time.sleep(1)
        run = False

    receive_flip_and_read()

    odd_indexes = []
    for i in range(0, NUMBER_OF_QUBITS):
        if i%2 == 0:
            odd_indexes.append(i)

    # only measures the odd indexed qubits once they are the ones that should be not set to 1 after
    # we set the even indexed (considering theyre entangled)
    teleportation_circuit.measure(odd_indexes, odd_indexes)

    # Execute the circuit on the qasm simulator
    job = execute(teleportation_circuit, simulator, shots=1)

    # Grab results from the job. Right now this is noy really doing anything other than read/destroy the states.
    # Im just preparing things in order to try the superposition strategy later.
    result = job.result()

    print(result.get_counts(teleportation_circuit))
    return [result.get_counts(teleportation_circuit), ping_history, [1] * int(NUMBER_OF_QUBITS/EMITTER_SPEED)]

results, quantum_history, regular_history = quantum_teleportation(10, 1, 3, 5)

print('finished: ', quantum_history, regular_history, results)