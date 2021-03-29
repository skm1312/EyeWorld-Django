from .models import Product , OrderItem , ShippingAddress , FullOrder , Purchased_item, ProductCategories, sendEmail

class UserOrderCore:
        def __init__(self, user_id):
                print("init function")
                self._observers = []
                self.user_id = user_id
 
        def attach(self, observer):
                print("attach observer")
                if observer not in self._observers: 
                        self._observers.append(observer)

        def detach(self, observer):
                try:
                        self._observers.remove(observer)
                except ValueError:
                        print("Observer is already not in the list of observers.")

        def notify(self):
                print("Notify observer")
                for observer in self._observers: 
                        observer.mail(self)
                 
        @property
        def user_id(self):
                '''The @property decorator makes a property object 'user_id', on which a setter can be defined, as done below.'''
                return self._user_id
 
        @user_id.setter
        def user_id(self, user_id):
                '''Notify the observers whenever new order has been made.
                   @user_id.setter notation signifies the setter method of the user_id property which
                   allows to call the learnig model using the assignment operator'''
                self._user_id= user_id
                self.notify()
                 
class OrderMonitoringCore:

  def mail(self, subject):
    print("ObserverPattern OrderMonitoringCore")
    user_id = subject._user_id
    mailinter = sendEmail()
    mailinter.sendmail(user_id)