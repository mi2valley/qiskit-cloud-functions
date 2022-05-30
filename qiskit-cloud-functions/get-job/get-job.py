import base64
import json
from google.cloud import firestore
from google.api_core.datetime_helpers import to_rfc3339
from qiskit import IBMQ
from qiskit import QuantumCircuit, execute
from qiskit.visualization import *
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt

IBMQ.save_account('YOUR_API_KEY')

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    seedAs = open('./seedAs.json', 'r')
    seedAs_dict = json.load(seedAs)
    print('json_dict:{}'.format(type(seedAs_dict))) #dict

    seedBs = open('./seedBs.json', 'r')
    seedBs_dict = json.load(seedBs)
    print('json_dict:{}'.format(type(seedBs_dict))) #dict

    seedCs = open('./seedCs.json', 'r')
    seedCs_dict = json.load(seedCs)
    print('json_dict:{}'.format(type(seedCs_dict))) #dict

    db = firestore.Client()
    docAs = db.collection(u'JobAs').where(u'status', u'==', 0).get()
    docBs = db.collection(u'JobBs').where(u'status', u'==', 0).get()
    docCs = db.collection(u'JobCs').where(u'status', u'==', 0).get()

    updatedAt = firestore.SERVER_TIMESTAMP


    for docA in docAs:
        jobA = docA.to_dict() 
        print(jobA)

    for docB in docBs:
        jobB = docB.to_dict()
        print(jobB)

    for docC in docCs:
        jobC = docC.to_dict()
        print(jobC)

    if docA.exists:
        print(f'Document data: {docA.to_dict()}')
    
        jobA = docA.to_dict()
        

        print(jobA)
        provider = IBMQ.load_account()
        backend = provider.get_backend(jobA['backend'])
        jobA_get = backend.retrieve_job(jobA['jobId'])
        job_monitor(jobA_get)
        jobA_result = jobA_get.result()
        jobA_counts = jobA_result.get_counts()
        print(jobA_counts)
        jobA_sorted_counts = sorted(jobA_counts.items(), reverse=True, key=lambda x: x[1]) 
        print(type(jobA_sorted_counts))
        print(jobA_sorted_counts)

        jobA_sorted_words = [] 
        for i in range(len(jobA_sorted_counts)):  
            jobA_sorted_words.append(seedAs_dict[jobA_sorted_counts[i][0]])

        print(jobA_sorted_words)
        jobA_status = 1
        docARef = docA.reference
        dataA = {
            u'jobId': jobA['jobId'],
            u'status': jobA_status,
            u'backend': jobA['backend'],
            u'sortedWords': jobA_sorted_words,
            u'createdAt': jobA['createdAt'],
            u'updatedAt': updatedAt
        }
        docARef.set(dataA)

    else:
        print(u'No JobA document!')

    if docB.exists:
        print(f'Document data: {docB.to_dict()}')
    
        jobB = docB.to_dict()
        

        print(jobB)
        provider = IBMQ.load_account()
        backend = provider.get_backend(jobB['backend'])
        jobB_get = backend.retrieve_job(jobB['jobId'])
        job_monitor(jobB_get)
        jobB_result = jobB_get.result()
        jobB_counts = jobB_result.get_counts()
        print(jobB_counts)
        jobB_sorted_counts = sorted(jobB_counts.items(), reverse=True, key=lambda x: x[1])
        print(jobB_sorted_counts)

        jobB_sorted_words = []
        for i in range(len(jobB_sorted_counts)): 
            jobB_sorted_words.append(seedBs_dict[jobB_sorted_counts[i][0]])

        print(jobB_sorted_words)
        jobB_status = 1

        docBRef = docB.reference
        dataB = {
            u'jobId': jobB['jobId'],
            u'status': jobB_status,
            u'backend': jobB['backend'],
            u'sortedWords': jobB_sorted_words,
            u'createdAt': jobB['createdAt'],
            u'updatedAt': updatedAt
        }
        docBRef.set(dataB)

    else:
        print(u'No JobB document!')

    if docC.exists:
        print(f'Document data: {docC.to_dict()}')
    
        jobC = docC.to_dict()
        

        print(jobC)
        provider = IBMQ.load_account()
        backend = provider.get_backend(jobC['backend'])
        jobC_get = backend.retrieve_job(jobC['jobId'])
        job_monitor(jobC_get)
        jobC_result = jobC_get.result()
        jobC_counts = jobC_result.get_counts()
        print(jobC_counts)
        jobC_sorted_counts = sorted(jobC_counts.items(), reverse=True, key=lambda x: x[1])
        print(jobC_sorted_counts)

        jobC_sorted_words = []
        for i in range(len(jobC_sorted_counts)):
            jobC_sorted_words.append(seedCs_dict[jobC_sorted_counts[i][0]])

        print(jobC_sorted_words)
        jobC_status = 1

        docCRef = docC.reference
        dataC = {
            u'jobId': jobC['jobId'],
            u'status': jobC_status,
            u'backend': jobC['backend'],
            u'sortedWords': jobC_sorted_words,
            u'createdAt': jobC['createdAt'],
            u'updatedAt': updatedAt
        }
        docCRef.set(dataC)

    else:
        print(u'No JobC document!')
