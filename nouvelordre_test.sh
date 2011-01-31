#!/bin/sh
for file in $(locate "*.py")
	do echo "testing $file"
	reorder --infile $file --outfile /dev/null
	if [ $? != 0 ] ; then
		echo "Please send the bug report (nouvelordre_bug_report) to feth@tuttu.info. Many thanks."
		exit 1
	fi
done
