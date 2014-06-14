class Record(object):
     def __init__(self):
          self.records = []

     def record_monthly_event(self, month, text):
          self.records.append("Month [{0:04d}]: {1} ".format(month, text))

     def record_yearly_event(self, month, text):
          self.records.append("Year [{0:04d}]: {1} ".format(int(month/12), text))
