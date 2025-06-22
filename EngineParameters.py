"""

Author(s): Jordan Handy

Last Updated: 06/08/2025

Description:
    Performs sizing and flow rate calculations for the StageZero BLANK Engine
    
Feature List:
    Optimization - might want to do through RPA instead of doing it ourselves. If interested
        look at Gurobi on the software website. Will likely need: import gurobipy as gb
    Fusion Integration - needs to be done through Fusion itself. The coding side is a 
        little weird
    GUI?

"""

import matplotlib.pyplot as plt
import math

def dataHandling():
    OF = []
    Isp_600 = []
    Isp_660 = []
    with open('SZ_Engine_CEA_Data.txt', 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0: 
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            OF.append(float(parts[0]))
            Isp_600.append(float(parts[1]))
            Isp_660.append(float(parts[2]))
    return OF, Isp_600, Isp_660

def OptimalOF(data):
    OF, Isp_600, Isp_660 = dataHandling()
    # fig, ax = plt.subplots()
    # ax.plot(OF, Isp_600, 'bo-', label='Isp at 600 psi')
    # ax.plot(OF, Isp_660, 'ro-', label='Isp at 660 psi')
    # ax.set_xlabel('Oxidizer to Fuel Ratio (OF)')
    # ax.set_ylabel('Specific Impulse (Isp) [s]')
    # ax.set_title('Isp vs OF Ratio')
    # ax.legend()
    # ax.grid(True)
    # plt.show()
    
    # Find maximum for both pressure conditions
    max_isp_600 = max(Isp_600)
    max_isp_660 = max(Isp_660)
    
    # Choose the higher maximum and determine pressure condition
    if max_isp_600 >= max_isp_660:
        max_isp_index = Isp_600.index(max_isp_600)
        OFoptimal = OF[max_isp_index]
        max_isp = max_isp_600
        c = max_isp
        max_isp = max_isp / 9.81 #m/s -> sec
        pressure_condition = "600 psi"
    else:
        max_isp_index = Isp_660.index(max_isp_660)
        OFoptimal = OF[max_isp_index]
        max_isp = max_isp_660
        c = max_isp
        max_isp = max_isp / 9.81 #m/s -> sec
        pressure_condition = "660 psi"
    return OFoptimal, max_isp, pressure_condition, c

def mainCalculations(EngineName,runtime,Thrust,Pc,Pa,FuelType,OxidizerType,
                     cstar,AeAt,AcAt,Lstar,rhof,rhoox,DisCoef,
                     OrificeCountf,OrificeCountox,):
    print(f"----------------------{EngineName}----------------------")
    OFoptimal, max_isp, pressure_condition, c = OptimalOF(dataHandling())
    # print('From the data given:')
    print(f'OF:                                 {OFoptimal:.3f}')
    print(f'Isp:                                {max_isp:.3f} sec')
    print(f'Chamber Pressure:                   {Pc} psi')
    print(f'Ambient Pressure:                   {Pa} Pa')
    
    mdot_total = Thrust/c
    mdot_fuel = mdot_total/(OFoptimal + 1)
    mdot_oxidizer = mdot_fuel*OFoptimal
    At = (cstar*mdot_total)/(Pc*6894.76)  #6894.75: psi -> Pa
    Dt = (4*At/math.pi)**0.5
    Ae = AeAt*At
    De = (4*Ae/math.pi)**0.5
    
    Pinjection = 1.3*Pc*6894.76  #TODO: Not sure if this value is correct. revisit later (6894.75: psi -> Pa)
    Pc = Pc * 6894.76  # Convert chamber pressure from psi to Pa
    FuelArea = mdot_fuel/(DisCoef*(math.sqrt(2*rhof*(Pinjection-Pc))))
    OrificeAreaf = FuelArea/OrificeCountf
    OrificeDiamf = (4*OrificeAreaf/math.pi)**0.5
    
    OxiArea = mdot_oxidizer/(DisCoef*(math.sqrt(2*rhoox*(Pinjection-Pc))))
    OrificeAreaox = OxiArea/OrificeCountox
    OrificeDiamox = ((4*OrificeAreaox)/math.pi)**0.5
    test = 2*math.sqrt(OrificeAreaox/math.pi)
    print(test)
    
    Ac = AcAt*At
    Dc = (4*Ac/math.pi)**0.5
    Lc = Lstar/AcAt
    massfuel = mdot_fuel * runtime
    massoxidizer = mdot_oxidizer * runtime

    #Print Statements
    print('\n------------------Mass Flow Rates-----------------')
    print(f'Total Mass Flow rate:               {mdot_total:.3f} kg/s')
    print(f'Mass Flow Rate of Fuel:             {mdot_fuel:.3f} kg/s')
    print(f'Mass Flow Rate of Oxidizer:         {mdot_oxidizer:.3f} kg/s')
    print('\n-----------------Throat Conditions----------------')
    print(f'Throat Area:                        {At*1e6:.3f} mm^2')
    print(f'Throat Diameter:                    {Dt*1000:.3f} mm')
    print('\n------------------Exit Conditions-----------------')
    print(f'Exit Area:                          {Ae*1e6:.3f} mm^2')
    print(f'Exit Diameter:                      {De*1000:.3f} mm')
    print('\n----------------Injector Parameters---------------')
    print(f'Injection Pressure:                 {Pinjection/6894.76:.3f} psi')
    print(f'Fuel Area:                          {FuelArea*1e6:.3f} mm^2')
    print(f'Fuel Orifice Diameter:              {OrificeDiamf*1000:.3f} mm')
    print(f'Oxidizer Area:                      {OxiArea*1e6:.3f} mm^2')
    print(f'Oxidizer Orifice Diameter:          {OrificeDiamox*1000:.3f} mm')
    print('\n----------Combustion Chamber Parameters-----------')
    print(f'Chamber Area:                       {Ac*1e6:.3f} mm^2')
    print(f'Chamber Diameter:                   {Dc*1000:.3f} mm')
    print(f'Chamber Length:                     {Lc*1000:.3f} mm')
    print('\n-----------------Other Parameters-----------------')
    print(f'Mass Fuel:                          {massfuel:.3f} kg')
    print(f'Mass Oxidizer:                      {massoxidizer:.3f} kg')
    print(f'Ac/At:                              {Ac/At:.3f}')
    print(f'Ae/At:                              {Ae/At:.3f}')
    print(f'L*:                                 {Lstar:.3f} m')
    print(f'C* (Characteristic Velocity):       {cstar:.3f} m/s')
    print('\n')
    return   


 
if __name__ == "__main__":
    print('Use default parameters? (y/n)')
    default = input().strip().lower()
    if default == 'y':
        EngineName = 'Gallus' #TODO: Update value
        runtime = 10 # sec
        Thrust = 5000 #N
        Pc = 600 #psi
        Pa = 95000 #Pa
        FuelType = 'Ethanol'
        OxidizerType = 'Nitrous Oxide'
        cstar = 1419.2 #m/s
        AeAt = 6.1825
        rhof = 789.4  #TODO: Update value
        rhoox = 776.415  #TODO: Update value
        DisCoef = 0.6  # Discharge coefficient (Maybe Update?)
        OrificeCountf = 6 #TODO: Update value
        OrificeCountox = 6 #TODO: Update value
        AcAt = 5 #TODO: Update value
        Lstar = 0.5 #TODO: Update value
    else:
        EngineName = input('Enter Engine Name: ')
        runtime = float(input('Runtime (sec): '))
        Thrust = float(input('Thrust (N): '))
        Pc = float(input('Chamber Pressure (psi): '))
        Pa = float(input('Ambient Pressure (Pa): '))
        FuelType = input('Fuel: ')
        OxidizerType = input('Oxidizer: ')
        cstar = float(input('Characteristic Velocity (m/s): '))
        AeAt = float(input('Ae/At: '))
        rhof = float(input('Fuel Density (kg/m^3): '))
        rhoox = float(input('Oxidizer Density (kg/m^3): '))
        DisCoef = float(input('Discharge Coefficient: '))
        OrificeCountf = int(input('Number of Fuel Holes: '))
        OrificeCountox = int(input('Number of Oxidizer Holes: '))
        AcAt = float(input('Ac/At: '))
        Lstar = float(input('L*: '))

    mainCalculations(EngineName, runtime, Thrust, Pc, Pa, FuelType, OxidizerType,
                     cstar, AeAt, AcAt, Lstar, rhof, rhoox, DisCoef,
                     OrificeCountf, OrificeCountox)
    