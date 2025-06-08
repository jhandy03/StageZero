"""

Author(s): Jordan Handy

Last Updated: 06/05/2025

Description:
    Performs sizing and flow rate calculations for the StageZero BLANK Engine
    
Feature List:
    Optimization - might want to do through RPA instead of doing it ourselves. If interested
        look at Gurobi on the software website. Will likely need: import gurobipy as gb
    Fusion Integration - needs to be done through Fusion itself. The coding side is a 
        little weird
    GUI?
    
License Information:
    MIT License
    
    Copyright (c) 2025 StageZero | Jordan Handy
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal       <-sounds cool and idk if we actually need this but makes it feel official
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies
"""

import math
import sympy as sym
import matplotlib.pyplot as plt

def main_calc(Thrust,Isp,g,Pa,Pc,Tc,R,gamma,OF_ratio,Lstar,stress,A_noz_cone,q,deltaT,rho_water,
              vw,burn_time):
    # Ask user if they want to use default values or input their own
    # use_defaults = input("Use default values? (y/n): ").lower().strip()
    
    # if use_defaults == 'y':
    #     # Use the default values passed as parameters
    #     pass
    # else:
    #     # Get user inputs for all variables
    #     Thrust = float(input("Enter Thrust (N): "))
    #     Isp = float(input("Enter Specific Impulse (sec): "))
    #     g = float(input("Enter gravitational acceleration (m/s^2): "))
    #     Pa = float(input("Enter ambient pressure (Pa): "))
    #     Pc = float(input("Enter chamber pressure (Pa): "))
    #     Tc = float(input("Enter chamber temperature (K): "))
    #     R = float(input("Enter gas constant (J/kg-K): "))
    #     gamma = float(input("Enter specific heat ratio: "))
    #     OF_ratio = float(input("Enter O/F ratio: "))
    #     # Lstar = float(input("Enter L* (m): "))
    #     # stress = float(input("Enter working stress (Pa): "))
    #     # A_noz_cone = float(input("Enter nozzle cone area factor: "))
    #     # q = float(input("Enter thermal conductivity (W/m-K): "))          Unused variables for now
    #     # deltaT = float(input("Enter temperature difference (K): "))
    #     # rho_water = float(input("Enter water density (kg/m^3): "))
    #     # vw = float(input("Enter water velocity (m/s): "))
    #     burn_time = float(input("Enter burn time (sec): "))

    mdot_total = Thrust/(Isp*g)
    mdot_fuel = mdot_total/(OF_ratio+1)
    mdot_oxidizer = mdot_total-mdot_fuel
    print('-----------Mass Flow Rates-----------')
    print(f'Fuel:                  {mdot_fuel:.3f} kg/s')
    print(f'Oxidizer:              {mdot_oxidizer:.3f} kg/s')
    print(f'Total:                 {mdot_total:.3f} kg/s')
    print('\n')
    
    print('-----------Throat Conditions-----------')
    Athroat = AreaChoked(mdot_total,Pc,Tc,gamma,R)
    Dthroat = math.sqrt((4*Athroat)/math.pi)
    print(f'Area:                  {Athroat*1e6:.3f} mm^2')
    print(f'Diameter:              {Dthroat*10**3:.3f} mm | {Dthroat/0.0254:.3f} in')
    print('\n')
    
    print('------------Exit Conditions------------')
    Mexit = math.sqrt((2/(gamma-1))*((Pc/Pa)**((gamma-1)/gamma)-1))
    Texit = Tc*(1+((gamma-1)/2)*Mexit**2)**-1
    Vexit = Mexit*math.sqrt(gamma*R*Texit)
    #assume Pe=Pa
    mdot_exit = Thrust/Vexit
    rho_exit = Pa/(R*Texit)
    Aexit = mdot_exit/(rho_exit*Vexit)
    Dexit = math.sqrt((4*Aexit)/math.pi)
    print(f'Area:                  {Aexit*1e6:.3f} mm^2')
    print(f'Diameter:              {Dexit*10**3:.3f} mm | {Dexit/0.0254:.3f} in')
    print(f'Mass flow rate:        {mdot_exit:.3f} kg/s')
    print(f'Mach:                  {Mexit:.3f}')
    print(f'Temperature:           {Texit:.3f} K')
    print(f'Velocity:              {Vexit:.3f} m/s')
    print('\n')

    print('-----Combustion Chamber Parameters-----')
    mass_oxi = mdot_oxidizer * burn_time
    mass_fuel = mdot_fuel * burn_time
    print(f'Oxidizer Mass:         {mass_oxi:.3f} kg')
    print(f'Fuel Mass:             {mass_fuel:.3f} kg')
    # print(f'L*:             {Lstar:.3f} m')   #L* seems to come from other places. A few people seem to just pull theirs from a textbook but we can't due to OF selection
    # print(f'Diameter:       {Dc*10**3:.3f} mm')
    # print(f'Area:           {Ac:.3f} m^2')
    # print(f'Length:         {Lc:.3f} m')
    # print(f'Working Stress: {stress*10**-6:.3f} MPa')
    # print(f'Wall Thickness: {tw*10**3:.3f} mm\n')
    print('\n')
    
    print('-----------Other Parameters------------')
    #print(f'Total Cooling Jacket Area: {A_passage:.6f} m^2')
    #print(f'Water Flow Gap:            {D_final*10**3/2:.3f} mm\n')
    AAstar = Aexit/Athroat
    print(f'A/A*:                  {AAstar:.3f}')
    print('\n')
    plotGeometry(Dthroat,Dexit)
    
def AAstar(M,gamma):
    #Area-Mach number relation
    AAstar = math.sqrt((1/M**2)*((2/(gamma+1))*(1+((gamma-1)/2)*M**2))**((gamma+1)/(gamma-1)))
    return AAstar

def AreaChoked(mdot,Pt,Tt,gamma,R):
    A = sym.symbols('A')
    mdoteqn = ((A*Pt)/math.sqrt(Tt))*math.sqrt(gamma/R)*((gamma+1)/2)**-((gamma+1)/(2*(gamma-1)))
    Aeqn = sym.Eq(mdot,mdoteqn)
    A = sym.solve(Aeqn,A)
    A = A[0]
    return A

def plotGeometry(Dthroat,Dexit):
    # Plot the 2D side view geometry of the nozzle
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    #TODO: edit the x values. Not sure what they should be atm. 
    x_throat = 0
    x_exit = 150  #mm
    y_throat = (Dthroat/2) * 1000  #Convert to mm
    y_exit = (Dexit/2) * 1000  #Convert to mm

    ax.plot([0,x_exit+0.5], [0, 0], 'k--', linewidth=1)  #Centerline

    #upper nozzle
    ax.plot([x_throat, x_exit], [y_throat, y_exit], 'b-', linewidth=2, label='Nozzle Profile')
    
    #lower nozzle
    ax.plot([x_throat, x_exit], [-y_throat, -y_exit], 'b-', linewidth=2)
    
    #limits and labels
    x_min, x_max = min(x_throat, x_exit), max(x_throat, x_exit)
    y_min, y_max = -max(y_throat, y_exit), max(y_throat, y_exit)
    
    x_padding = (x_max - x_min) * 0.1 if x_max != x_min else 0.1
    y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 0.1
    
    ax.set_xlim(x_min - x_padding, x_max + x_padding)
    ax.set_ylim(y_min - y_padding, y_max + y_padding)
    ax.set_xlabel('Axial Position (mm)')
    ax.set_ylabel('Radial Position (mm)')
    ax.set_title('Nozzle Profile')
    ax.legend()
    
    plt.grid()
    #plt.show() #Note: Uncomment to show the plot
    plt.rcParams['toolbar'] = 'None'

if __name__ == "__main__":
    #TODO: Can change all the inputs to be user inputs. IE they input from the terminal 
    #Inputs
    Thrust = 5*10**3 #N
    Isp = 240 #sec
    g = 9.81 #m/s**2
    Pa = 95000 #Pa (Blacksburg Ambient summer)
    OF_ratio = 2.5 #got somewhere near 5 from RPA. Might need to change later
    Pc = 7*10**6 #Pa
    Tc = 3100  #K
    R = 287 #J/kg-K
    gamma = 1.4 #not sure if this is correct with the different species
    #Find a better value for L*
    Lstar = 1.5 #m
    stress = 8000*6895 #Pa working stress value of combustion chamber material
    A_noz_cone = 1.1
    q = 385 #W/m-K
    deltaT = 299.817 #K
    rho_water = 997 #kg/m**3
    #vw = ww/(rho_water*A_passage)
    vw = 10 #m/s
    burn_time = 10 #sec
    main_calc(Thrust,Isp,g,Pa,Pc,Tc,R,gamma,OF_ratio,Lstar,stress,A_noz_cone,q,deltaT,rho_water,
              vw,burn_time)
    