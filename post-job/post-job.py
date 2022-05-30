import base64
import json
from google.cloud import firestore
from google.api_core.datetime_helpers import to_rfc3339
from qiskit import IBMQ
from qiskit import QuantumCircuit, execute, ClassicalRegister, QuantumRegister
from qiskit.visualization import *
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt


# start by loading your IBMQ API key.
IBMQ.save_account('YOUR_API_KEY')

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    # load your account information and check the available backends
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    provider.backends()

    # select the most available backend
    large_enough_devices = IBMQ.get_provider(hub='ibm-q', group='open', project='main').backends(
        filters=lambda x: x.configuration().n_qubits > 4 and not x.configuration().simulator and x.configuration().quantum_volume > 16 )
    print(large_enough_devices)
    real_backend = least_busy(large_enough_devices)

    print("best backend " + real_backend.name())

    # build quantum circuit
    qreg_q = QuantumRegister(5, 'q')
    creg_c = ClassicalRegister(5, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)

    circuit.rz(1.5707963267948966, qreg_q[0])
    circuit.sx(qreg_q[0])
    circuit.rz(1.5707963267948966, qreg_q[0])
    circuit.rz(1.5707963267948966, qreg_q[1])
    circuit.sx(qreg_q[1])
    circuit.rz(1.5707963267948966, qreg_q[1])
    circuit.rz(1.5707963267948966, qreg_q[2])
    circuit.sx(qreg_q[2])
    circuit.rz(1.5707963267948966, qreg_q[2])
    circuit.rz(1.5707963267948966, qreg_q[3])
    circuit.sx(qreg_q[3])
    circuit.rz(1.5707963267948966, qreg_q[3])
    circuit.rz(1.5707963267948966, qreg_q[4])
    circuit.sx(qreg_q[4])
    circuit.rz(1.5707963267948966, qreg_q[4])
    circuit.measure(qreg_q[0], creg_c[0])
    circuit.measure(qreg_q[1], creg_c[1])
    circuit.measure(qreg_q[2], creg_c[2])
    circuit.measure(qreg_q[3], creg_c[3])
    circuit.measure(qreg_q[4], creg_c[4])

    # execute
    jobA = execute(circuit, real_backend)
    jobA_id = jobA.job_id()
    jobA_status = 0
    db = firestore.Client()

    createdAt = firestore.SERVER_TIMESTAMP

    dataA = {
        u'jobId': jobA_id,
        u'status': jobA_status,
        u'backend': real_backend.name(),
        u'createdAt': createdAt
    }
    db.collection(u'JobAs').add(dataA)

    jobB = execute(circuit, real_backend)
    jobB_id = jobB.job_id()
    # 0 means "queued", and this parameter is stored in the database.
    jobB_status = 0

    dataB = {
        u'jobId': jobB_id,
        u'status': jobB_status,
        u'backend': real_backend.name(),
        u'createdAt': createdAt
    }
    db.collection(u'JobBs').add(dataB)

    jobC = execute(circuit, real_backend)
    jobC_id = jobC.job_id()
    jobC_status = 0

    dataC = {
        u'jobId': jobC_id,
        u'status': jobC_status,
        u'backend': real_backend.name(),
        u'createdAt': createdAt
    }
    db.collection(u'JobCs').add(dataC)