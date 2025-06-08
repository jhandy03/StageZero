import matplotlib.pyplot as plt
import math

def dataHandling():
    OF = []
    Isp_600 = []
    Isp_660 = []
    with open('SZ_Engine_CEA_Data.txt', 'r') as file:
        lines = file.readlines()
        # Skip header (assume first line is header)
        data_lines = lines[1:]
        for line in data_lines:
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
        pressure_condition = "600 psi"
    else:
        max_isp_index = Isp_660.index(max_isp_660)
        OFoptimal = OF[max_isp_index]
        max_isp = max_isp_660
        c = max_isp
        pressure_condition = "660 psi"
    
    return OFoptimal, max_isp/9.81, pressure_condition, c

def mainCalculations():
    EngineName = 'Vulcan'
    runtime = 10 # seconds
    print(f"----------------------{EngineName}----------------------")
    Thrust = 5000
    Pc = 600
    Pa = 95000
    FuelType = 'Ethanol'
    OxidizerType = 'Nitrous Oxide'
    OFoptimal, max_isp, pressure_condition, c = OptimalOF(dataHandling())
    # print('From the data given:')
    print(f'OF:                                 {OFoptimal:.3f}')
    print(f'Isp:                                {max_isp:.3f} sec')
    print(f'Chamber Pressure:                   {Pc} psi')
    print(f'Ambient Pressure:                   {Pa} Pa')
    
    cstar = 1419.2 #m/s
    AeAt = 6.1825
    mdot_total = Thrust / c
    mdot_fuel = mdot_total / (OFoptimal + 1)
    mdot_oxidizer = mdot_fuel * OFoptimal
    At = (cstar*mdot_total) / (Pc * 6894.76)  # Convert Pc from psi to Pa
    Dt = (4 * At / math.pi) ** 0.5
    Ae = AeAt * At
    De = (4 * Ae / math.pi) ** 0.5
    
    Pinjection = 1.3*Pc*6894.76  #TODO: Not sure if this value is correc. revisit later
    rhof = 789.3  #TODO: Update value
    rhoox = 1125.0  #TODO: Update value
    DisCoef = 0.6  # Discharge coefficient (Maybe Update?)
    FuelArea = mdot_fuel/(DisCoef*(math.sqrt(2*rhof*(Pinjection-Pc))))
    OrificeCountf = 20 #TODO: Update value
    OrificeAreaf = FuelArea / OrificeCountf
    OrificeDiamf = (4 * OrificeAreaf / math.pi) ** 0.5
    
    OxiArea = mdot_oxidizer/(DisCoef*(math.sqrt(2*rhoox*(Pinjection-Pc))))
    OrificeCountox = 20 #TODO: Update value
    OrificeAreaox = OxiArea / OrificeCountox
    OrificeDiamox = (4 * OrificeAreaox / math.pi) ** 0.5
    
    AcAt = 5 #TODO: Update value
    Ac = AcAt*At
    Dc = (4 * Ac / math.pi) ** 0.5
    Lstar = 0.5 #TODO: Update value
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
    print(f'Injection Pressure:                 {Pinjection/1000:.3f} kPa')
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
    mainCalculations()
    