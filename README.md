# auto_update_records
A program to update file records based on mobile number
The program checks the folder where it is located every 15 minutes, for the csv file
When new file is added, updates result file with new file based on mobile number
That is, if the mobile number was duplicated, it would hold the last record and erase the previous record
And if the mobile number was new, the record would be added to the result file
Deletes the checked file after the operation is performed
