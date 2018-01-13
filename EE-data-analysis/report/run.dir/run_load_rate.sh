
export run_code='python loadrateTSDB.py -rdm rc05_excel_copy_tag_v5 -wtm ___d_tag_test_load_rate_5 -start 201607010000 -end 201707010000'

cd ..

if [ -n $1 ] ; # $1 is not null
then
    echo $1
    if [ $1 = 'loadrate' ] ;
    then
      echo " ... start counting data points and calculate avg in TSDB "
      echo " ... make sure if you have written proper input list in __main__ "
      echo $run_code
      exec $run_code
    else
      echo " no argument is valid, please type one of count | copy | insert | loadrate"
    fi
fi

cd run.dir
unset run_code



#insertValue_periodically(u, write_metric, 450, stime, etime, 60)
#export run_code='python copyTSDB.py -start 201607010000 -end 20161050000 -rdm rc05_operation_rate_v6'
#export run_code='python copyTSDB.py -start 201607010000 -end 201707010000 -wtm ___d_tag_test_compressor_1 '
#export run_code='python copyTSDB.py -rdm rc05_excel_copy_tag_v5 -wtm ___d_tag_test_load_rate_3 -start 201607010000 -end 201610010000'
#export run_code='python ../countTSDB.py -start 201607010000 -end 201707010000 -wtm ___d_tag_test_pump_1 -val 14 -p 60'
#export run_code='python countTSDB.py -start 201607010000 -end 201707010000 -rdm rc05_operation_rate_v6'
#export run_code='python countTSDB.py -start 201607010000 -end 201707010000 -rdm rc04_simple_data_v3'
#export run_code='python countTSDB.py -start 201607010000 -end 201707010000 -rdm rc05_operation_rate_v6'
