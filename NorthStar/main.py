"""

Author(s): Jordan Handy

Last Updated: 06/14/2025

Description:
    Calls all major components of NorthStar. Submodules include the GUI, propellant measurements, sensors, 
    actuators, and controls
    
Feature List:

TODO:
    
    
Notes:


"""

from GUI.gui import TestStandGUI
from PropellantMeasurements.propellant import PropellantMeasurements
from Sensors.sensor_suite import SensorSuite
from Actuators.actuators import Actuators
from Controls.controls import Controls

if __name__ == "__main__":
    gui = TestStandGUI()
    # propm =  PropellantMeasurements()
    # sensors = SensorSuite()
    # actuators = Actuators()
    # controls = Controls()
    
#HEllo World