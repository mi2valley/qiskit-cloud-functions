import base64
from google.cloud import firestore
import hashlib


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    db = firestore.Client()
    docAs = db.collection(u'JobAs').where(u'status', u'==', 1).get() 
    docBs = db.collection(u'JobBs').where(u'status', u'==', 1).get() 
    docCs = db.collection(u'JobCs').where(u'status', u'==', 1).get()

    for docA in docAs:
        jobA = docA.to_dict()  
        print(jobA)

    for docB in docBs:
        jobB = docB.to_dict()
        print(jobB)

    for docC in docCs:
        jobC = docC.to_dict()
        print(jobC)

    if docA.exists and docB.exists and docC.exists:
        jobA = docA.to_dict()
        jobB = docB.to_dict()
        jobC = docC.to_dict()

        jobA_sorted_words = jobA['sortedWords']
        jobB_sorted_words = jobB['sortedWords']
        jobC_sorted_words = jobC['sortedWords']

        for i, t in enumerate(zip(jobA_sorted_words, jobB_sorted_words, jobC_sorted_words)):  #list(元々nはkey)
            haiQ = []
            haiQ.extend([t[0], t[1], t[2]])
            haiq_string = ''.join(haiQ)
            print(haiq_string)
            hashid = hashlib.sha256(haiq_string.encode()).hexdigest()
            print(hashid)
            print(type(hashid))
            # verify that the document id in the database does not conflict here
            doc = db.collection(u'HaiQs').document(hashid).get()
            if not doc.exists:
                data = {
                    u'haiQ': haiQ,
                    u'publishedAt': None,
                    u'order': i
                }
                db.collection(u'HaiQs').document(hashid).set(data)
            

        docARef = docA.reference
        docBRef = docB.reference
        docCRef = docC.reference

        updatedAt = firestore.SERVER_TIMESTAMP

        docARef.update({u'status': 2, u'updatedAt': updatedAt})
        docBRef.update({u'status': 2, u'updatedAt': updatedAt})
        docCRef.update({u'status': 2, u'updatedAt': updatedAt})

    else:
        print(u'No such document!')