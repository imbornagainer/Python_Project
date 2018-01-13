export cmd='python Calc_operationRate.py -rdm rc06_operation_rate_v3 -wtm rc06_op_rate_02 '

echo $cmd
echo ''
exec $cmd

unset cmd
