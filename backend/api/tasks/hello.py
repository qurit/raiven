import time
import dramatiq

from api import db, socketio


def audit(func):
    def wrapper():
        message = dramatiq.middleware.CurrentMessage.get_current_message()

        print(f'TASK {message.message_id} IS NOW RUNNING')
        db.jobs.update_one({'pid': message.message_id}, {'$set': {'status': 'Running'}})
        func()
        db.jobs.update_one({'pid': message.message_id}, {'$set': {'status': 'Finished'}})
        print(f'TASK {message.message_id} IS NOW FINISHED')

    return wrapper


@dramatiq.actor
@audit
def count_words():
    for x in range(0, 10):
        time.sleep(10)
        socketio.emit('my_response', {'data': 'Background event', 'count': x, 'progress': x / 10}, namespace='/test')

