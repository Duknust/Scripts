#!/bin/bash

filename="$1"
minimumGradeLEI=20 #starting minimum value
maximumGradeLEI=0 #starting maximum value
minimumGradeMEI=20 #starting minimum value
maximumGradeMEI=0 #starting maximum value
countLEIVar=0
sumLEIVar=0
countMEIVar=0
sumMEIVar=0
inLEI=0
INMEI=0

while read -r line
do
    IFS='-' read -a array <<< "$line"

    #echo "$index ${array[index]}"
    #echo ${array[0]}
    if [ ${array[0]} == "LEI" ]; then
        inLEI=1
        #echo INLEI
    elif [ ${array[0]} == "MEI" ]; then
        inLEI=0
        #echo $countLEIVar
        #echo INMEI
    fi
    if [ $inLEI -eq 1 ]; then
        if [ ${array[1]} -lt 21 ]; then
            countLEIVar=$((countLEIVar + 1))
            sumLEIVar=$((sumLEIVar + ${array[1]}))
        fi
    else
        if [ ${array[1]} -lt 21 ]; then
            countMEIVar=$((countMEIVar + 1))
            sumMEIVar=$((sumMEIVar + ${array[1]}))
        fi
    fi
    if [ ${array[1]} -lt 21 ]; then
        if [ $inLEI -eq 1 ]; then
            if [ ${array[1]} -le $minimumGradeLEI ]; then
                minimumGradeLEI=${array[1]}
                #echo "NOVO MIN ${array[1]}"
            fi  
            if [ ${array[1]} -ge $maximumGradeLEI ]; then
                maximumGradeLEI=${array[1]}
                #echo "NOVO MAX ${array[1]}"
            fi
        else
            if [ ${array[1]} -le $minimumGradeMEI ]; then
                minimumGradeMEI=${array[1]}
                #echo "NOVO MIN ${array[1]}"
            fi  
            if [ ${array[1]} -ge $maximumGradeMEI ]; then
                maximumGradeMEI=${array[1]}
                #echo "NOVO MAX ${array[1]}"
            fi
        fi
    fi 
done < "$filename"

#echo SLEI $sumLEIVar
#echo CLEI $countLEIVar
#echo SMEI $sumMEIVar
#echo CMEI $countMEIVar

#avgLEI = echo $((sumLEIVar / countLEIVar))
#avgMEI = echo $((sumMEIVar / countMEIVar))

#varLEI=$(echo '$sumLEIVar / $countLEIVar' | bc -l)
varPreciseSumLEI=`echo $sumLEIVar*1.0|bc`
varPreciseCountLEI=`echo $countLEIVar*1.0|bc`
varPreciseLEI=`echo $varPreciseSumLEI/$varPreciseCountLEI|bc -l`

varPreciseSumMEI=`echo $sumMEIVar*1.0|bc`
varPreciseCountMEI=`echo $countMEIVar*1.0|bc`
varPreciseMEI=`echo $varPreciseSumMEI/$varPreciseCountMEI|bc -l`

varLEI=`echo $sumLEIVar/$countLEIVar|bc`
varMEI=`echo $sumMEIVar/$countMEIVar|bc`

varPreciseLEI=$(echo "$varPreciseLEI" | head -c 5)
varPreciseMEI=$(echo "$varPreciseMEI" | head -c 5)


echo -e "\033[1;32m$varLEI""\033[0m""("$varPreciseLEI")"
echo -e "\033[1;32m$varMEI""\033[0m""("$varPreciseMEI")"


inLEI=0
INMEI=0

if [ "$#" -ge 2 ]; then
    if [ "$2" == "wg" ] || [ "$2" == "all" ]; then
        #shows worst grades
        echo -e "\033[1;36mWorst Grades:\033[0m" 
        while read -r line
        do
            IFS='-' read -a array <<< "$line"

            if [ ${array[0]} == "LEI" ]; then
                inLEI=1
                INMEI=0
                echo -e "\033[1;36mLEI\033[0m"
            fi
            if [ ${array[0]} == "MEI" ]; then
                inLEI=0
                INMEI=1
                echo -e "\033[1;36mMEI\033[0m"
            fi
            if [ $inLEI -eq 1 ]; then
                if [ ${array[1]} -eq $minimumGradeLEI ]; then
                    if [ ${array[2]} == "y" ]; then
                        echo -e "\033[1;31m${array[0]} ${array[1]}\033[0m"
                    else
                        echo "${array[0]} ${array[1]}"
                    fi
                fi
            else 
                if [ ${array[1]} -eq $minimumGradeMEI ]; then
                    if [ ${array[2]} == "y" ]; then
                        echo -e "\033[1;31m${array[0]} ${array[1]}\033[0m"
                    else
                        echo "${array[0]} ${array[1]}"
                    fi
                fi
            fi
        done < "$filename"
    fi
    if [ "$2" == "bg" ] || [ "$2" == "all" ]; then
        #shows best grades
        echo -e "\033[1;36mBest Grades:\033[0m"
        while read -r line
        do
            IFS='-' read -a array <<< "$line"

            if [ ${array[0]} == "LEI" ]; then
                inLEI=1
                INMEI=0
                echo -e "\033[1;36mLEI\033[0m"
            fi
            if [ ${array[0]} == "MEI" ]; then
                inLEI=0
                INMEI=1
                echo -e "\033[1;36mMEI\033[0m"
            fi
            if [ $inLEI -eq 1 ]; then
                if [ ${array[1]} -eq $maximumGradeLEI ]; then
                    if [ ${array[2]} == "y" ]; then
                        echo -e "\033[1;31m${array[0]} ${array[1]}\033[0m"
                    else
                        echo "${array[0]} ${array[1]}"
                    fi
                fi
            else
                if [ ${array[1]} -eq $maximumGradeMEI ]; then
                    if [ ${array[2]} == "y" ]; then
                        echo -e "\033[1;31m${array[0]} ${array[1]}\033[0m"
                    else
                        echo "${array[0]} ${array[1]}"
                    fi
                fi
            fi
        done < "$filename"
    fi
    if [ "$2" == "change" ]; then
        uc="$3"
        newGrade="$4"
        while read -r line
        do
            IFS='-' read -a array <<< "$line"
                if [ ${array[0]} == $3 ]; then
                    array[1]=$newGrade
                fi
            newLine=${array[0]}"-"${array[1]}
            echo $newLine >> tmp.txt
        done < "$filename"
        rm -f $1
        mv tmp.txt $1
        echo -e "\033[1;36mchanged\033[0m"
    fi
fi



