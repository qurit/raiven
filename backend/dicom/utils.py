from dataclasses import dataclass

from pynetdicom import AE


class ApplicationEntity(AE):
    def associate(self, address, port, **kwargs):
        return super().associate(addr=address, port=port, **kwargs)


@dataclass
class Modality:
    address: str
    port: int
    ae_title: str


class Association:
    __association = None

    def __init__(self, modality: Modality, context, **kwargs):
        self.modality = modality
        self.context = context
        self.kwargs = kwargs

    def __enter__(self):
        print('get assoc')
        self.__association = self.__get_assoc()
        return self.__association

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('RELEASE')
        self.__association.release()
        self.__association = None

    def __get_assoc(self):
        ae = ApplicationEntity()
        [ae.add_requested_context(c) for c in self.context] if type(self.context) is list else ae.add_requested_context(self.context)

        assoc = ae.associate(**vars(self.modality), **self.kwargs)
        assert assoc.is_established
        return assoc





