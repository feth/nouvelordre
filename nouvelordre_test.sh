for script in *.py
do
    cat $script|nouvelordre.py > /tmp/new_order
    the_diff=`diff --unified $script /tmp/new_order`
    if [ -n "$the_diff" ]
    then
        diff --unified $script /tmp/new_order
        read -p "Does the new import order seem correct ? [Yn]" answer
        if [ x"$answer" = x"n" ]
        then
            echo ""
            echo $(diff --unified $script /tmp/new_order) >> nouvelordre_bug_report
        fi
        echo "================================================"
    fi
done

if [ -f nouvelordre_bug_report ]
then
    echo "Please send the bug report (nouvelordre_bug_report) to feth@tuttu.info. Many thanks."
fi
