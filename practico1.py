import random

def adivinar(cant_intentos = 5):
    numero = random.randint(0, 100)
    print(numero)
    intentos_totales = 1
    while (intentos_totales <= cant_intentos):
        print('Intento {} de {}. Ingrese un entero entre 0 y 100 para adivinar.'.format(intentos_totales, cant_intentos))
        intento = 0
        try:
            intento = int(input())
        except:
            print('Formato inválido, un entero es requerido. Intente nuevamente.')
            intento = int(input())

        if (intento == numero):
            print('Ganaste!')
            intentos_totales = cant_intentos
        elif (intento < numero):
            print('No es correcto!')
            print('Pista: El numero a adivinar es mayor!')
        elif (intento > numero):
            print('No es correcto!')
            print('Pista: El numero a adivinar es menor!')

        intentos_totales += 1


adivinar(8)