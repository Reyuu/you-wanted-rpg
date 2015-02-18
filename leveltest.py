class Observable:
    def __init__(self):
        self.__observers = []
 
    def register_observer(self, observer):
        self.__observers.append(observer)
 
    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer(self, *args, **kwargs)
 
 
class Observer:
    def __init__(self, observable):
        observable.register_observer(self.notify)
        self.tenlinesbuffer = []
 
    def notify(self, observable, *args, **kwargs):
        self.tenlinesbuffer.append(args[0])
        if len(self.tenlinesbuffer) is 11:
            self.tenlinesbuffer.pop(0)
        for i in self.tenlinesbuffer:
            print(i)
 
 
subject = Observable()
observer = Observer(subject)
for i in range(12):
    subject.notify_observers(str(i))
#subject.notify_observers("test")
x = raw_input(">>>")
subject.notify_observers(x)
