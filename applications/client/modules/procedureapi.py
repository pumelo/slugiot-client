import constants
import datetime
import json_plus
from gluon import current
import slugiot_setup

class Procedure(json_plus.Serializable):
    """"This is the base class of all procedures.
    The initializer sets the procedure api.
    The class has a "run" method, which is the one called to trigger
    procedure execution.  Other methods can be defined by the user."""

    def __init__(self):
        self.api = None
        self.init()

    # Can be over-ridden in subclasses.
    def init(self): pass

    @staticmethod
    def create(procedure_id):
        """Creates a procedure api for a given procedure_id."""
        p = Procedure()
        api = ProcedureApi.create(procedure_id)
        p.api = api
        return p


class ProcedureApi(object):
    """This is the class defining the procedure API.
    A procedure API is instantiated from the procedure_id, and it is
    then passed to the initializer for a procedure."""

    def __init__(self, procedure_id):
        self.procedure_id = procedure_id


    def write_output(self, name, data, tag=None, timestamp=None):
        """ This write the value and the tag to the outputs table.
        param name : Name of the output
        param data : The value of the output
        Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""
        db = current.db
        timestamp = timestamp or datetime.datetime.utcnow()
        db.outputs.insert(procedure_id=self.procedure_id,
                          name=name,
                          output_value=json_plus.Serializable.dumps(data),
                          time_stamp=timestamp,
                          tag=tag)
        db.commit()


    def write_outputs(self, data, tag=None):
        """ This write the values and the tag to the outputs table.
        param data : dict of key/value pairs to be written to the table. All pairs will have the same timestamp
        Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""

        db = current.db
        time_now = datetime.datetime.utcnow()
        # Luca: check, rewritten to use previous method.
        for name, data in data.iteritems():
            self.write_output(name, data, tag=tag, timestamp=time_now)
        db.commit()


    def log(self, log_text, log_level=None):
        # Luca: Can you use the LogLevel.INFO defined
        """Writes a log message to the logs table
        param log_text : message to be logged
        param log_level : 0 for error, 1 for warning, 2 for info, 3 for debug """
        db = current.db
        log_level = slugiot_setup.LogLevel.INFO if log_level is None else log_level
        db.logs.insert(time_stamp=datetime.datetime.utcnow(),
                       procedure_id=self.procedure_id,
                       log_level=log_level,
                       log_message=log_text)
        db.commit()

    # Useful shorthands.
    def log_debug(self, s):
        return self.log(s, log_level=constants.LogLevel.DEBUG)
    def log_info(self, s):
        return self.log(s, log_level=constants.LogLevel.INFO)
    def log_warn(self, s):
        return self.log(s, log_level=constants.LogLevel.WARNING)
    def log_error(self, s):
        return self.log(s, log_level=constants.LogLevel.ERROR)
    def log_critical(self, s):
        return self.log(s, log_level=constants.LogLevel.CRITICAL)

    def add_schedule(self,
                     class_name,
                     function_args=[],
                     delay=0,
                     start_time=None,
                     stop_time=None,
                     timeout=60,
                     period_between_runs=60,
                     repeats = 1,
                     num_retries=1):

        """Add a schedule to the Web2py scheduler.
        param function_args : list of arguments to be passed to the run function
        param start_time : The time for the schedule to be assigned. datetime object.
            Passed to Web2py's queue_task with delay added.
        param delay : delay added to initial start time.
        param stop_time : datetime object, defaults to none.
        param timeout : The maximum time the function runs, defaults to 60 seconds
        param period_between_runs : The number of seconds between runs. Use this to setup a recurring schedule.
                             Defaults to 60 seconds
        param repeats : The number of times the task should run. Use this to setup a recurring schedule.
                            Defaults to 1, which means the function is run once
        param num_retries : The number of times a task is retried if it fails
        """
        start_time = start_time or datetime.datetime.now()
        start_time += datetime.timedelta(seconds=delay)

        current.slugiot_scheduler.queue_task(
            task_name=str(self.procedure_id),
            function='run_procedure',
            pvars = {'procedure_id':self.procedure_id, 'class_name':class_name, 'function_args':function_args},
            repeats = repeats,
            period = period_between_runs,
            start_time=start_time,
            stop_time=stop_time,
            timeout=timeout,
            retry_failed=num_retries)
        current.db.commit();


    def remove_schedule(self, function):
        """Deletes the existing schedule for this procedure and function
        param function: The function of this procedure whose schedule should be deleted"""

        self.log("Removing scheduled task for the current function " + function,
                 constants.LogLevel.INFO)
        db = current.db
        db((db.scheduler_task.task_name == str(self.procedure_id))).delete()
        db.commit()