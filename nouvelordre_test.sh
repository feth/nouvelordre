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
			echo "Please see https://github.com/feth/nouvelordre/issues and maybe leave a message. Many thanks."
			exit 1
			;;
	esac
done
