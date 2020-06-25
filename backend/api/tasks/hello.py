import time
import dramatiq

from api import db


def audit(func):
    def wrapper():
        message = dramatiq.middleware.CurrentMessage.get_current_message()

        db.jobs.update_one({'pid': message.message_id}, {'$set': {'status': 'Running'}})
        print('TASK IS ACTIVE', message.message_id)
        func()
        print('TASK HAS FINISHED', dramatiq.middleware.CurrentMessage.get_current_message().message_id)
        db.jobs.update_one({'pid': message.message_id}, {'$set': {'status': 'Finished'}})

    return wrapper


@dramatiq.actor
@audit
def count_words():
    print(f'Running Background Task', dramatiq.middleware.CurrentMessage.get_current_message().message_id)
    for x in range(0, 3):
        print("Running...")
        time.sleep(5)
    print('Finished Background Task')
