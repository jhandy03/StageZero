"""
Test Document for StageZero Engine Parameters

"""

import matplotlib.pyplot as plt

def mainCalc(Thrust, Pc, FuelType, OxidizerType, EngineName,c):
    print(f"----------{EngineName}----------")
    print('Input Parameters:')
    print(f'Thrust:              {Thrust} N')
    print(f'Combustion Pressure: {Pc} psi')
    print(f'Fuel Type:           {FuelType}')
    print(f'Oxidizer Type:       {OxidizerType}')
    g = 9.81
    
    Isp = c/g
    print('----------Mass FLow Rates----------')
    mdot_total = Thrust/Isp


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
    fig, ax = plt.subplots()
    ax.plot(OF, Isp_600, 'bo-', label='Isp at 600 psi')
    ax.plot(OF, Isp_660, 'ro-', label='Isp at 660 psi')
    ax.set_xlabel('Oxidizer to Fuel Ratio (OF)')
    ax.set_ylabel('Specific Impulse (Isp) [s]')
    ax.set_title('Isp vs OF Ratio')
    ax.legend()
    ax.grid(True)
    plt.show()
    
    # Find maximum for both pressure conditions
    max_isp_600 = max(Isp_600)
    max_isp_660 = max(Isp_660)
    
    # Choose the higher maximum and determine pressure condition
    if max_isp_600 >= max_isp_660:
        max_isp_index = Isp_600.index(max_isp_600)
        OFoptimal = OF[max_isp_index]
        max_isp = max_isp_600
        pressure_condition = "600 psi"
    else:
        max_isp_index = Isp_660.index(max_isp_660)
        OFoptimal = OF[max_isp_index]
        max_isp = max_isp_660
        pressure_condition = "660 psi"
    
    return OFoptimal, max_isp/9.81, pressure_condition
    
    

if __name__ == "__main__":
    print('use default parameters (y/n)?')
    useDefault = input().strip().lower()
    if useDefault == 'y':
        Thrust = 5000 #N
        Pc = 300 #psi
        FuelType = 'Ethanol'
        OxidizerType = 'Nitrous Oxide'
        EngineName = 'BLANK'
        OFratio = 4
        c = 3800
    else:
        Thrust = float(input('Enter Thrust (N): '))
        Pc = float(input('Enter Combustion Pressure (psi): '))
        FuelType = input('Enter Fuel Type: ')
        OxidizerType = input('Enter Oxidizer Type: ')
        EngineName = input('Enter Engine Name: ')
        OFratio = float(input('Enter Oxidizer to Fuel Ratio: '))
        c = float(input('Enter Specific Impulse (s): '))

    mainCalc(Thrust, Pc, FuelType, OxidizerType, EngineName,c)
    OFratio = OptimalOF(dataHandling())
    print(f'\nOptimal OF Ratio: {OFratio[0]}, Maximum Isp: {OFratio[1]} sec at: {OFratio[2]}\n')
    
