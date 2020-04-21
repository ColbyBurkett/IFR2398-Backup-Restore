# IFR2398-Backup-Restore
 After many years of on/off work, I have finally completed the Backup/Restore scripts to a point where they're usable. These two scripts perform the function of the FCAL2398 Backup/Restore options.

Automatically dump to file (DONE!):
- Receiver Flatness (RXFLAT)
- 0dB-50dB Tables w/all four frequency groups
- IF Attenuator (IFATT)
- RX Attenuator (RXATT)
- Span Attenuator (SPANATT)
- LOG Adjustments w/all RBW values (LOGTBL)

Automatically restore from file (DONE!):
- Unit Manufacturer/Model between IFR or LG
- Serial Number
- Receiver Flatness
- IF Attenuator
- RX Attenuator
- Span Attenuator
- LOG Adjustments

Remaining work:

>Calibrate using one of many possible methods
>With the backup/restore process working, and leveraging the Service Manual calibration steps as clues, it should be a fairly trivial task to get the calibration process done
>My only issue is this: I've run out of working analyzers to test the cal process with!! If I can get a good, working unit, I'll resume work
>FM Sweep Gain dump/set (easy to do manually, though)
>Coarse Sweep GainS/GainF dump/set (easy to do manually, though)
>YIG Slope dump/set (easy to do manually, though)
>YIG Offset dump/set (easy to do manually, though)
>Tracking Generator calibration dump/restore

To use:
```
Install your KeySight I/O libraries. I have tested with 18.1.x
Connect your GPIB adapter (I have used 82357B USB adapter - both genuine and clone)
Install Python 2.7.x (I have tested with 2.7.13)
Install PyVisa library into Python
Connect your IFR 2398 or LG SA-7270 to the GPIB bus and set your SA to ID 7
If you don't have a GPIB port on your SA, a generic ribbon to IEEE488 connector does work - I used one from an Agilent sig gen I had laying around
Execute '2398 Dump Full.py' to back up the cal data
Edit '2398 Restore Full.py' with the name of backup file (line 38, or search for backupFileName), and execute to restore the backup of the cal data
```
