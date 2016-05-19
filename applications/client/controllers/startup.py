def start():
    """NB: procedureapi.add_schedule() could have been used to add sync schedules
    by passing a dummy procedure name, but this is the only place where scheduling
    of these functions occurs, and it seemed safer to create tasks directly.  Also,
    since this is the only place at which the task is scheduled, it is safe to
    simply delete and recreate tasks at each startup (the parameters don't change)"""

    from gluon import current
    import datetime

    start_time = datetime.datetime.now()

    db(db.scheduler_task.task_name == 'do_procedure_sync').delete()
    db(db.scheduler_task.task_name == 'do_synchronization').delete()

    current.slugiot_scheduler.queue_task(
        task_name='do_procedure_sync',
        function='do_procedure_sync',
        start_time=start_time,
        pvars={},
        repeats=1,  # If repeats=0 (unlimited), it would constantly fail.
        period=60,
        timeout=60,
        retry_failed=1
    )
    current.db.commit()


    current.slugiot_scheduler.queue_task(
        task_name='do_synchronization',
        function='do_synchronization',
        start_time=start_time,
        pvars={},
        repeats=1,  # If repeats=0 (unlimited), it would constantly fail.
        period=600,
        timeout=60,
        retry_failed=5
    )
    current.db.commit()



def clear_all_tasks():
    """Here we clear all tasks"""
    current.db(db.scheduler_task).delete()
    current.db.commit()
