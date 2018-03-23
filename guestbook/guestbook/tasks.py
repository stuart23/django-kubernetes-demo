from celery import shared_task
from merkle import MerkleTree
from .models import Message

@shared_task
def hasher(message_id):
    '''
    Takes the current root of the Merkle tree, adds another leaf to the root,
    calculates a new hash, and then puts that back in the table.
    '''
    tree = MerkleTree()
    message = Message.objects.get(pk=message_id)
    tree.add(message.text.encode())
    tree.build()
    message.hash = tree.root.val
    message.save()
