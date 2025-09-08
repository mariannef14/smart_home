from smart_home.core.dispositivos import CorEnum


class BrilhoValidator:

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)
    

    def __set__(self, instance, value):
        
        if value >= 0 and value <= 100:
           setattr(instance, self.private_name, value)
        
        else:
            raise ValueError("Valor do brilho precisa estar entre 0 e 100")
    

    def __set_name__(self, owner, name):
        self.private_name = "_" + name


class CorValidator:

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)


    def __set__(self, instance, value):

        if value.upper() in [cor.name for cor in CorEnum]:
            setattr(instance, self.private_name, value)

        else:
            raise ValueError(f"A cor {value} não existe")


    def __set_name__(self, owner, name):
        self.private_name = "_" + name


class PorcentagemValidator:


    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)


    def __set__(self, instance, value):

        if value >= 0 and value <= 100:
            setattr(instance, self.private_name, value)
        
        else:
            raise ValueError("Valor da porcentagem de abertura precisa estar entre 0 e 100")


    def __set_name__(self, owner, name):
        self. private_name = "_" + name