#List에 있는 LTE number 를 이용하여, Exel에서 추출한 tag 정보를 JSON 으로 출력
#python3 list2json.py -i in_list -l inverter_list -r ref_list.xlsx -s 2 -o inverter_list.json


# 최근 작업
# 20171212 새로구해진 rc05_none_dp_v5 으로 totoal 카운트를 다시 구함
# 20171212 TO DO: ubuntu 에서 python 3.6 설치가 잘 안됨


echo "...start..."

#python3.6 copy_tsdb.py -i rc06_op_rate_v3 -o rc100__op__rate_v1 -r count_list.json -e 31 -s 2016/07/01 -d &&
python3.6 copy_tsdb.py -i rc06_op_rate_v3 -o rc100__op__rate_v1 -r count_list.json -e 31 -s 2016/07/01 -d -q &&

echo "...done..."
exit

#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/07/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/08/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/09/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/10/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/11/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/12/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/01/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/02/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/03/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/04/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/05/01 -d -x &&
#python3.6 count_tsdb.py -i rc05_none_dp_v5 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2017/06/01 -d -x

#python3.6 count_tsdb.py -i rc05_none_dp_v4 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/10/01 -d -x && python3.6 count_tsdb.py -i rc05_none_dp_v4 -o rc04_total_cnt__001 -r count_list.json -e 31 -s 2016/11/01 -d -x && python3.6 count_tsdb.py -i rc05_none_dp_v4 -o rc04_totoal_cnt__001 -r count_list.json -e 31 -s 2016/12/01 -d -x
