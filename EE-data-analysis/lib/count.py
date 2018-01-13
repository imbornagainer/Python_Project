import max_value_dict
import _input_list_17_1026

print  " max value count = ",
print len(max_value_dict.max_dict)

print  " modem list = %d " %len(_input_list_17_1026.modem_list)
print  " led_modem list = %d " %len(_input_list_17_1026.led_modem_list)
print  " inverter_modem list = %d " %len(_input_list_17_1026.inverter_modem_list)
print  " add_list = %d " %len(_input_list_17_1026.add_list)
print  " valid_list = %d " %len(_input_list_17_1026.valid_list)


zero_count = 0
for k,v in max_value_dict.max_dict.items():
    if v == 0 :
        zero_count = zero_count + 1
print " z cout = %d" %zero_count 
