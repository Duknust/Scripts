#!/bin/bash

filename="$1"

while read -r line
do
    IFS='-' read -a array <<< "$line"

    indexItem=${array[0]}
    dateItem=${array[1]}
    ucItem=${array[2]}
    descriptionItem=${array[3]}
done < "$filename"

#next index number to be unique
nextIndex=$((indexItem + 1))

if [ "$#" -gt 1 ]; then
    if [ "$2" == "a" ]; then #add new entry
        echo -e "\033[1;31mdate (YYYYMMDD) : \033[0m"
        read dateItem
        echo -e "\033[1;31muc (w/out -) : \033[0m"
        read ucItem
        echo -e "\033[1;31mdescription (w/out -) : \033[0m"
        read descriptionItem
        
        newLine=$nextIndex"-"$dateItem"-"$ucItem"-"$descriptionItem"-n"
        echo $newLine >> todo.txt
    fi
    if [ "$2" == "c" ]; then #close entry
        echo -e "\033[1;31mIndex : \033[0m"
        read indexToConclude
        
        while read -r line
        do
            IFS='-' read -a array <<< "$line"

            indexItem=${array[0]}
            dateItem=${array[1]}
            ucItem=${array[2]}
            descriptionItem=${array[3]}
            doneItem=${array[4]}

            if [ $indexItem -eq indexToConclude ]; then
                newLine=$indexItem"-"$dateItem"-"$ucItem"-"$descriptionItem"-y"
            else
                newLine=$indexItem"-"$dateItem"-"$ucItem"-"$descriptionItem"-"$doneItem
            fi
            echo $newLine >> tmp9141q74414148baf.txt
        done < "$filename"
        rm -f $1
        mv tmp9141q74414148baf.txt $1
        echo -e "\033[1;36mDone\033[0m"
    fi
    if [ "$2" == "ld" ]; then #list by date
        dateToSearch=$3
        echo $dateToSearch

        while read -r line
        do
            IFS='-' read -a array <<< "$line"

            indexItem=${array[0]}
            dateItem=${array[1]}
            ucItem=${array[2]}
            descriptionItem=${array[3]}
            doneItem=${array[4]}
            echo $indexItem
            echo $dateItem
            echo $ucItem
            echo $descriptionItem
            echo $doneItem

            if [ $dateItem == "$3" ] && [ $doneItem == "n" ]; then
                echo $indexItem $ucItem    $descriptionItem
            fi
        done < "$filename"
    fi
    if [ "$2" == "luc" ]; then #list by UC
        dateToSearch=$3
        echo $dateToSearch

        while read -r line
        do
            IFS='-' read -a array <<< "$line"

            indexItem=${array[0]}
            dateItem=${array[1]}
            ucItem=${array[2]}
            descriptionItem=${array[3]}
            doneItem=${array[4]}
            echo $indexItem
            echo $dateItem
            echo $ucItem
            echo $descriptionItem
            echo $doneItem

            if [ $ucItem == "$3" ] && [ $doneItem == "n" ]; then
                echo $indexItem $dateItem    $descriptionItem
            fi
        done < "$filename"
    fi
else 
    echo "You must provide arguments"
    echo "  a - to add new entry"
    echo "  c - to complete an entry"
    echo "  ld - list entries by date"
    echo "  luc - list entries by class"
fi


