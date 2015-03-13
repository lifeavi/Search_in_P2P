#!/usr/bin/bash

for i in $(cat path_to_ips.txt/ips.txt) #ips.txt contains the planetlab nodes one line each
do
	xterm -hold -e "ssh -i ~/.ssh/identity colostate_cnrl@${i} 'mkdir divyanka; cd divyanka'" & 
	# This command will open xterm terminals for each entry in ips.txt and ssh into them. It will then create a directory called divyanka and go into the folder divyanka.
	# you can enter the system commands you want to run wthin the single quotation marks. Change the directory to your own folder
	# you can replace the entire ssh command with the scp command to transfer your files to PlanetLab
	# The SCP command : "scp -r -i ~/.ssh/identity ~/path_to_your_files/*.class colostate_cnrl@${i}:you_folder_in_PlanetLab"
	  
	
done
