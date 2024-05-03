from datetime import date
from abc import ABC, abstractmethod


class CuentaBancaria(ABC):
    def __init__(self, nombre_titular, dni_titular, fecha_nacimiento, saldo=0):
        self._nombre_titular = nombre_titular
        self._dni_titular = dni_titular
        self._fecha_nacimiento = fecha_nacimiento
        self._saldo = saldo

    @abstractmethod
    def obtener_saldo(self):
        return self._saldo

    @abstractmethod
    def depositar(self, monto):
        pass

    @abstractmethod
    def extraer(self, monto):
        pass

    def _calcular_edad(self):
        fecha_actual = date.today()
        edad = fecha_actual - self._fecha_nacimiento
        return edad.days // 365

    def obtener_edad(self):
        return self._calcular_edad()


class CuentaCorriente(CuentaBancaria):
    def __init__(self, nombre_titular, dni_titular, fecha_nacimiento, saldo=0, limite_extraccion=500):
        super().__init__(nombre_titular, dni_titular, fecha_nacimiento, saldo)
        self._limite_extraccion = limite_extraccion

    def extraer(self, monto):
        if monto <= self.obtener_saldo() and monto <= self._limite_extraccion:
            self._saldo -= monto
            print(f"Se ha extraído {monto} de la cuenta de {self._nombre_titular}. Saldo actual: {self.obtener_saldo()}")
        else:
            if monto > self._limite_extraccion:
                print("Usted no puede extraer ese monto")
            else:
                print("Usted no posee saldo suficiente para realizar la operación")


class CuentaAhorro(CuentaBancaria):
    def __init__(self, nombre_titular, dni_titular, fecha_nacimiento, saldo=0, tasa_interes=0.001):
        super().__init__(nombre_titular, dni_titular, fecha_nacimiento, saldo)
        self._tasa_interes = tasa_interes

    def calcular_interes(self):
        interes = self._tasa_interes * self.obtener_saldo()
        self._saldo += interes
        print(f"Se ha calculado un interés de {interes}. Saldo actual: {self.obtener_saldo()}")


class MiCuentaBancaria(CuentaBancaria):
    def depositar(self, monto):
        if monto > 0:
            self._saldo += monto
            print(f"Se ha depositado {monto}. Saldo actual: {self.obtener_saldo()}")
        else:
            print("El monto a depositar debe ser mayor a 0")

    def extraer(self, monto):
        if monto <= self.obtener_saldo():
            self._saldo -= monto
            print(f"Se ha extraído {monto}. Saldo actual: {self.obtener_saldo()}")
        else:
            print("No posee saldo suficiente para esta operación")


class MiCuentaCorriente(CuentaCorriente):
    pass


class MiCuentaAhorro(CuentaAhorro):
    pass

