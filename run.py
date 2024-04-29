
from app.main import app

# import redis
# from rq import Worker, Queue, Connection

# redis_conn = redis.StrictRedis(host='localhost', port=6379)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005, use_reloader=True)

    # with Connection(connection=redis_conn):
    #     queue = Queue("email_queue")
    #     worker = Worker([queue])
    #     worker.work()

    # Start the RQ worker
    # with Connection(connection=redis_conn):
    #     worker = Worker(Queue('default'))
    #     worker.work()
