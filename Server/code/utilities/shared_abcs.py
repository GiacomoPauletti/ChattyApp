import abc

class IObserver(abc.ABC):
    """@abc.abstractmethod
    def update(self):
        ...
        """
    ...

class IObservable(abc.ABC):
    """@abc.abstractmethod
    def registerObserver(self, observer : IObserver) -> None:
        ...

    def removeObserver(self, observer : IObserver) -> None:
        ...

    def notifyObservers(self) -> None:
        ...
        """
    ...
