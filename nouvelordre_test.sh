#!/bin/sh
for file in $(locate "*.py")
	do echo "testing $file"

	if [ ! -f $file ] ; then
		echo "file $file not found or not a file."
		continue
	fi

	reorder --infile $file --outfile /dev/null --dump
	case $? in
		129)
			echo "Seems the file is not compiling, ignoring error."
			;;
		130)
			echo "NotImplementedError ! Ignoring anyway"
			;;
		0)
			echo "...ok"
			;;
		*)
			echo "Please send the bug report (nouvelordre_bug_report) to feth@tuttu.info. Many thanks."
			exit 1
			;;
	esac
done
