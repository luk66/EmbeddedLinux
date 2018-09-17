temp=`i2cget -y 2 0x48` 
temp2=$((( $temp * 9 ) / 5 + 32 )) 
echo $temp2

temp1=`i2cget -y 2 0x4a`
temp12=$((( $temp1 * 9 ) / 5 + 32 ))
echo $temp12
