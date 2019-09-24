# Introduction
Building on the guestbook application created here https://josephb.org/blog/, a task queue could be a beneficial addition to our app. Celery is a “batteries included” task queue with easy integration and numerous features.

With the threat of meddling by foreign forces being a threat, we should add some verification method. Blockchain technologies seem to be all the rage right now, so we will create a Merkle Tree of our ledger using the python Merkle package – ‘merkle’. https://github.com/jvsteiner/

The hashing algorithm is not particularly computationally intensive, however by offloading processes from Django on to worker processes, there is less risk of Django being bound up. Offloading tasks is often necessary when dealing with user submitted files or data, for example encoding a user uploaded video for a video streaming site.

# Resizing Cluster
With the addition of 2 more pods to our application, 2 cores are no longer sufficient to handle all the processes (if overloaded, gcloud will refuse to spool up one of the pods). Provision another CPU:

``gcloud container clusters resize guestbook --size=3``

Kubenetes will automatically rebalance the pods over all the avalible VMs.

# Building New Containers
There are two new containers for the two new roles that we have to add to our app. From within the django-kubernetes-demo directory, enter the guestbook app and build both of the containers.

``cd guestbook``

``docker build . -f Dockerfile.celery-worker --tag gcr.io/$(gcloud config list project --format="value(core.project)")/celery-worker:v1``

``docker build . -f Dockerfile.celery-beat --tag gcr.io/$(gcloud config list project --format="value(core.project)")/celery-beat:v1``

Then push the containers to the repository.

``gcloud docker -- push gcr.io/$(gcloud config list project --format="value(core.project)")/celery-worker:v1``

``gcloud docker -- push gcr.io/$(gcloud config list project –format="value(core.project)")/celery-beat:``

And finally deploy them.

``kubectl apply -f ../celery.yaml``



As we have changed the source code of the Django app, we need to recompile a new container and deploy that too.

``docker build . -f --tag gcr.io/$(gcloud config list project --format="value(core.project)")/guestbook:v3``

``gcloud docker -- push gcr.io/$(gcloud config list project --format="value(core.project)")/guestbook:v3``

``kubectl set image deployment/guestbook guestbook=gcr.io/$(gcloud config list project --format="value(core.project)")/guestbook:v3``

We have changed the database schema, and so need to apply a migration to update the database structure.

``kubectl exec $(kubectl get pods | grep guestbook | awk '{ print $1 }') python ./manage.py migrate``

# Testing the New App
The load balancer has not changed, so the exposed IP address will not have changed. Open a browser and navigate to the IP address of the service. The guestbook will look the same as before but when new items are added, they’ll show up in the below table. In the background, the hash will be computed and added to the database record belonging to the message. When the website is refreshed, the hash will show up next to the message written. Instead of the hash being shown when the message has been submitted, it is calculated asynchronously and only displayed when the client requests it.

# Cleaning up
Just as with the first part of this tutorial, close down the cluster when finished.

``gcloud container clusters delete guestbook``
``gcloud compute disks delete pg-data``
