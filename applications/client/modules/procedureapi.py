import datetime
from gluon import current

class ProcedureApi():

    def __init__(self, procedure_name):
        self.procedure_name = procedure_name

    def write_value(**dictionary):
    	db = current.db
        for key in dictionary:
            ModuleValues = dictionary['module_value']
            VariableName = dictionary['variable_name']
        TimeStamp = datetime.datetime.utcnow()
	ModuleName = self.procedure_name
        db.module_values.insert(modulename=ModuleName,
				name=VariableName,
        			module_value=ModuleValues,
        			time_stamp=TimeStamp)


    def write_output(self, name, data, tag):
        """ This write the values and the tag to the outputs table.
        param name : This is the name of the output
         param data : The value of the output
         Param tag: This is the ID of the sensor (or additional data to differentiate the outputs)"""
        # todo : Sync with visualization team for Json format
        db = current.db
        db.outputs.insert(modulename=self.procedure_name,
                          name=name,
                          output_value=data,
                          time_stamp=datetime.datetime.utcnow(),
                          tag=tag)

    def write_log(self, log_text, log_level=0):
        """Writes a log message to the logs table
        param log_text : message to be logged
        param log_level : 0 for error, 1 for warning, 2 for info, 3 for debug """
        db = current.db
        db.logs.insert(time_stamp=datetime.datetime.utcnow(),
                       modulename=self.procedure_name,
                       log_level=log_level,
                       log_message=log_text)

    # todo : schedule tasks for procedure
    def add_schedule(self):
        pass

