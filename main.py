import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Rangos comida y servicio
calidad_comida = ctrl.Antecedent(np.arange(1, 11, 1), 'CalidadComida')
calidad_servicio = ctrl.Antecedent(np.arange(1, 11, 1), 'CalidadServicio')

#Parametros comida
mala_comida = fuzz.trapmf(calidad_comida.universe, [1, 1, 3, 5])
buena_comida = fuzz.trapmf(calidad_comida.universe, [4, 5, 7, 8])
excelente_comida = fuzz.trapmf(calidad_comida.universe, [7, 8.5, 10, 10])

#Parametros servicio
mal_servicio = fuzz.trapmf(calidad_servicio.universe, [1, 1, 3, 4])
buen_servicio = fuzz.trapmf(calidad_servicio.universe, [3, 4, 7, 8])
excelente_servicio = fuzz.trapmf(calidad_servicio.universe, [6.76, 9.64, 10.36, 13.24])

#Comida
calidad_comida['MalaComida'] = mala_comida
calidad_comida['BuenaComida'] = buena_comida
calidad_comida['ExcelenteComida'] = excelente_comida

#Servicio
calidad_servicio['MalServicio'] = mal_servicio
calidad_servicio['BuenServicio'] = buen_servicio
calidad_servicio['ExcelenteServicio'] = excelente_servicio

#Rango propina
propina = ctrl.Consequent(np.arange(0, 21, 1), 'Propina')

#Parametros propina
nada_propina = fuzz.trimf(propina.universe, [0, 0, 0])
baja_propina = fuzz.trimf(propina.universe, [2, 5, 8])
media_propina = fuzz.trimf(propina.universe, [7, 10, 13])
alta_propina = fuzz.trimf(propina.universe, [15, 20, 20])

#Propina
propina['NadaPropina'] = nada_propina
propina['BajaPropina'] = baja_propina
propina['MediaPropina'] = media_propina
propina['AltaPropina'] = alta_propina

#Reglas
rule1 = ctrl.Rule(calidad_comida['MalaComida'] & calidad_servicio['MalServicio'], propina['NadaPropina'])
rule2 = ctrl.Rule(calidad_comida['MalaComida'] & calidad_servicio['BuenServicio'], propina['NadaPropina'])
rule3 = ctrl.Rule(calidad_comida['MalaComida'] & calidad_servicio['ExcelenteServicio'], propina['BajaPropina'])
rule4 = ctrl.Rule(calidad_comida['BuenaComida'] & calidad_servicio['MalServicio'], propina['NadaPropina'])
rule5 = ctrl.Rule(calidad_comida['BuenaComida'] & calidad_servicio['BuenServicio'], propina['MediaPropina'])
rule6 = ctrl.Rule(calidad_comida['BuenaComida'] & calidad_servicio['ExcelenteServicio'], propina['MediaPropina'])
rule7 = ctrl.Rule(calidad_comida['ExcelenteComida'] & calidad_servicio['MalServicio'], propina['NadaPropina'])
rule8 = ctrl.Rule(calidad_comida['ExcelenteComida'] & calidad_servicio['BuenServicio'], propina['MediaPropina'])
rule9 = ctrl.Rule(calidad_comida['ExcelenteComida'] & calidad_servicio['ExcelenteServicio'], propina['AltaPropina'])

# Se crean el control de sistema de reglas
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulation = ctrl.ControlSystemSimulation(system)

# Se pide calidad de la comida y calidad del servicio
print("Calificacion de la comida (1 - 10): ")
try:
    comida_input = input()
    if comida_input == "":
        comida_calificacion = 0
    else:
        comida_calificacion = float(comida_input)
except ValueError:
    comida_calificacion = 0

print("Calificacion del servicio (1 - 10): ")
try:
    servicio_input = input()
    if servicio_input == "":
        servicio_calificacion = 0
    else:
        servicio_calificacion = float(servicio_input)
except ValueError:
    servicio_calificacion = 0

# Luego puedes asignar las calificaciones a tu simulación
simulation.input['CalidadComida'] = comida_calificacion
simulation.input['CalidadServicio'] = servicio_calificacion

# Se realiza el calculo con los datos recibidos
simulation.compute()

# Obtener el valor de la propina
if comida_calificacion == 0 and servicio_calificacion == 0:
    propina_calculada = 0
else:
    propina_calculada = simulation.output['Propina']

print(f"La propina calculada es: {propina_calculada:.8f}")

if propina_calculada >= 0 and propina_calculada <= 1.9:
    print("No se recibio nada de propina :c")
elif propina_calculada >= 2 and propina_calculada <= 4.9:
    print("La propina esta entre nada y poca")
elif propina_calculada == 5:
    print("La propina fue poca")
elif propina_calculada >= 5.1 and propina_calculada <= 9.9:
    print("La propina esta entre poca y una normal")
elif propina_calculada == 10:
    print("Se recibio una propina normal")
elif propina_calculada >= 10.1 and propina_calculada <= 19.9:
    print("la propina esta entre una normal y una generosa")
elif propina_calculada == 20:
    print("Que generosa propina :D")