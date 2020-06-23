from pynetdicom import AE


class Modality:
    __association = None

    def __init__(self, address: str, port: int, aet: str):
        self.address = address
        self.port = port
        self.aet = aet

    def __enter__(self, context, **kwargs):
        print('get assoc')
        self.__association = self.__get_assoc(context, **kwargs)
        return self.__association

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        self.__association.release()
        self.__association = None

    def __get_assoc(self, context, **kwargs):
        ae = AE()
        [ae.add_requested_context(c) for c in context] if type(context) is list else ae.add_requested_context(context)

        assoc = ae.associate(addr=self.address, port=self.port, ae_title=self.aet, **kwargs)
        assert assoc.is_established
        return assoc



