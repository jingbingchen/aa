from base_logging import log
from pzdf_dm.device_logcat import device_log
from pzdf_test_case import call_hold_test_case, tripartite_test_case, blind_turn_answer_case, \
    blind_turn_answer_case_result, attend_transfer_verification, video_function_check, phone_conference_verification, \
    phone_conference_six_verification
from tools.run_pool import RunPool
from utils import mysql

_phone_list = [
    {"ip": "192.168.0.107", "phone": "6018"},
    {"ip": "192.168.0.109", "phone": "6020"},
    {"ip": "192.168.0.111", "phone": "6028"},
    {"ip": "192.168.0.112", "phone": "6024"},
    {"ip": "192.168.0.113", "phone": "6026"},
    {"ip": "192.168.0.114", "phone": "6027"},
    {"ip": "192.168.0.115", "phone": "6029"},
    {"ip": "192.168.0.116", "phone": "6021"},
    {"ip": "192.168.30.143", "phone": "6000"}
]


def allocation_phone(phone_list, amount):
    new_phone_list = [phone_list[i:i + amount] for i in range(0, len(phone_list), amount)]
    res_list = []
    for phone_list_info in new_phone_list:
        # 如果话机数量不够直接抛弃
        if not len(phone_list_info) < amount:
            res = {}
            for index, phone_info in enumerate(phone_list_info):
                if index == 0:
                    res.update({"dial_ip": phone_info["ip"], "dial_code": phone_info["phone"]})
                elif index == 1:
                    res.update({"answer_ip": phone_info["ip"], "code": phone_info["phone"]})
                elif index == 2:
                    res.update({"tripartite_ip": phone_info["ip"], "tripartite_code": phone_info["phone"]})
                elif index == 3:
                    res.update({"tripartite_two_ip": phone_info["ip"], "tripartite_two_code": phone_info["phone"]})
                elif index == 4:
                    res.update({"tripartite_three_ip": phone_info["ip"], "tripartite_three_code": phone_info["phone"]})
                elif index == 5:
                    res.update({"tripartite_four_ip": phone_info["ip"], "tripartite_four_code": phone_info["phone"]})
            res_list.append(res)
        else:
            print("-- 不参加case的话机：", phone_list_info)
    return res_list


if __name__ == '__main__':

    devices = [
        # {"ip": "192.168.0.214", "port": ""},
        # {"ip": "192.168.0.191", "port": ""},
        # {"ip": "192.168.0.60", "port": ""},
        # {"ip": "192.168.0.215", "port": ""},
        {"ip": "192.168.30.162", "port": ""},
        {"ip": "192.168.30.164", "port": ""},
        {"ip": "192.168.30.170", "port": ""},
        {"ip": "192.168.30.165", "port": ""},
        {"ip": "192.168.30.175", "port": ""},
        {"ip": "192.168.30.163", "port": ""},
        {"ip": "192.168.30.169", "port": ""},
        # {"ip": "192.168.30.171", "port": ""},
        {"ip": "192.168.30.167", "port": ""},
        {"ip": "192.168.30.172", "port": ""},
        {"ip": "192.168.30.168", "port": ""},
        {"ip": "192.168.30.183", "port": ""},
        {"ip": "192.168.30.166", "port": ""}
    ]
    for param in devices:
        log.info("初始化终端[{}:{}]", param.get("ip"), param.get("port"))
        # device_log(param.get("ip"))

    params = [
        {"dial_ip": "192.168.0.214", "answer_ip": "192.168.0.191", "code": "6025"}
        ,
        {"dial_ip": "192.168.0.60", "answer_ip": "192.168.0.215", "code": "6024"}
        ,
        {"dial_ip": "192.168.30.162", "answer_ip": "192.168.30.164", "code": "6004"}
        ,
        {"dial_ip": "192.168.30.170", "answer_ip": "192.168.30.165", "code": "6015"}
        ,
        {"dial_ip": "192.168.30.175", "answer_ip": "192.168.30.163", "code": "6016"}
        ,
        {"dial_ip": "192.168.30.169", "answer_ip": "192.168.30.171", "code": "6012"}
        ,
        {"dial_ip": "192.168.30.167", "answer_ip": "192.168.30.172", "code": "6018"}
        ,
        {"dial_ip": "192.168.30.168", "answer_ip": "192.168.30.166", "code": "6020"}
    ]

    params2 = [
        {"dial_ip": "192.168.0.214", "answer_ip": "192.168.0.191", "code": "6025"}
        ,
        {"dial_ip": "192.168.0.60", "answer_ip": "192.168.0.215", "code": "6024"}
        ,
        {"dial_ip": "192.168.30.164", "answer_ip": "192.168.30.162", "code": "6000"}
        ,
        {"dial_ip": "192.168.30.165", "answer_ip": "192.168.30.170", "code": "6014"}
        ,
        {"dial_ip": "192.168.30.163", "answer_ip": "192.168.30.175", "code": "6008"}
        ,
        {"dial_ip": "192.168.30.171", "answer_ip": "192.168.30.169", "code": "6017"}
        ,
        {"dial_ip": "192.168.30.172", "answer_ip": "192.168.30.167", "code": "6013"}
        ,
        {"dial_ip": "192.168.30.166", "answer_ip": "192.168.30.168", "code": "6019"}
    ]

    params3 = [
        {"dial_ip": "192.168.0.214", "answer_ip": "192.168.0.191", "code": "6025", "tripartite_ip": "192.168.0.215",
         "tripartite_code": "6024"},
        {"dial_ip": "192.168.30.162", "answer_ip": "192.168.30.164", "code": "6004", "tripartite_ip": "192.168.30.170",
         "tripartite_code": "6014"},
        {"dial_ip": "192.168.30.165", "answer_ip": "192.168.30.175", "code": "6008", "tripartite_ip": "192.168.30.163",
         "tripartite_code": "6016"},
        {"dial_ip": "192.168.30.169", "answer_ip": "192.168.30.171", "code": "6012", "tripartite_ip": "192.168.30.167",
         "tripartite_code": "6013"},
        {"dial_ip": "192.168.30.172", "answer_ip": "192.168.30.168", "code": "6019", "tripartite_ip": "192.168.30.166",
         "tripartite_code": "6020"}
    ]
    cycle_number = 2000
    params4 = [
        {'dial_ip': '192.168.30.162', 'dial_code': '6000', 'answer_ip': '192.168.30.164', 'code': '6004',
         'tripartite_ip': '192.168.30.175', 'tripartite_code': '6008', "cycle_number": cycle_number},
        {'dial_ip': '192.168.30.183', 'dial_code': '6027', 'answer_ip': '192.168.30.167', 'code': '6013',
         'tripartite_ip': '192.168.30.170', 'tripartite_code': '6014', "cycle_number": cycle_number},
        {'dial_ip': '192.168.30.172', 'dial_code': '6018', 'answer_ip': '192.168.30.168', 'code': '6019',
         'tripartite_ip': '192.168.30.166', 'tripartite_code': '6020', "cycle_number": cycle_number},
        {'dial_ip': '192.168.30.165', 'dial_code': '6015', 'answer_ip': '192.168.30.163', 'code': '6016',
         'tripartite_ip': '192.168.30.169', 'tripartite_code': '6017', "cycle_number": cycle_number}
    ]

    params4 = [
        {'service_uuid': '1111', 'case_uuid': '222', 'dial_ip': '192.168.0.91', 'dial_code': '6050',
         'answer_ip': '192.168.0.92', 'code': '6010',
         'tripartite_ip': '192.168.0.94', 'tripartite_code': '6015', "cycle_number": cycle_number}
    ]

    # params5 = [
    #     {'dial_ip': '192.168.0.105', 'dial_code': '6022', 'answer_ip': '192.168.0.106', 'code': '6003',
    #      'tripartite_ip': '192.168.0.107', 'tripartite_code': '6018', "cycle_number": cycle_number},
    #     {'dial_ip': '192.168.0.108', 'dial_code': '6025', 'answer_ip': '192.168.0.109', 'code': '6020',
    #      'tripartite_ip': '192.168.0.110', 'tripartite_code': '6019', "cycle_number": cycle_number},
    #     {'dial_ip': '192.168.0.111', 'dial_code': '6028', 'answer_ip': '192.168.0.112', 'code': '6024',
    #      'tripartite_ip': '192.168.0.113', 'tripartite_code': '6026', "cycle_number": cycle_number}
    # ]

    service_uuid = "431926b5913d4e7fb55c09271e164882"
    case_uuid = "case1"
    case_uuid1 = "case2"
    case_uuid2 = "case3"
    case_uuid3 = "case4"
    case_uuid4 = "case5"
    case_uuid5 = "case6"
    case_uuid6 = "case7"
    case_uuid7 = "case8"
    case_uuid8 = "case9"
    case_uuid9 = "case10"
    params7 = [
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.143', 'dial_code': '6000',
         'answer_ip': '192.168.30.148', 'code': '6052',
         'tripartite_ip': '192.168.30.147', 'tripartite_code': '6002', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid1, 'dial_ip': '192.168.30.154', 'dial_code': '6004',
         'answer_ip': '192.168.30.144', 'code': '6005',
         'tripartite_ip': '192.168.30.159', 'tripartite_code': '6006', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid2, 'dial_ip': '192.168.30.160', 'dial_code': '6007',
         'answer_ip': '192.168.30.157', 'code': '6008',
         'tripartite_ip': '192.168.30.156', 'tripartite_code': '6009', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid3, 'dial_ip': '192.168.30.142', 'dial_code': '6011',
         'answer_ip': '192.168.30.152', 'code': '6012',
         'tripartite_ip': '192.168.30.150', 'tripartite_code': '6013', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid4, 'dial_ip': '192.168.30.145', 'dial_code': '6014',
         'answer_ip': '192.168.30.151', 'code': '6017',
         'tripartite_ip': '192.168.30.149', 'tripartite_code': '6023', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid5, 'dial_ip': '192.168.30.139', 'dial_code': '6022',
         'answer_ip': '192.168.30.153', 'code': '6003',
         'tripartite_ip': '192.168.0.107', 'tripartite_code': '6018', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid6, 'dial_ip': '192.168.30.138', 'dial_code': '6025',
         'answer_ip': '192.168.0.109', 'code': '6020',
         'tripartite_ip': '192.168.30.137', 'tripartite_code': '6019', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid7, 'dial_ip': '192.168.0.111', 'dial_code': '6028',
         'answer_ip': '192.168.0.112', 'code': '6024',
         'tripartite_ip': '192.168.0.113', 'tripartite_code': '6026', "cycle_number": cycle_number},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid8, 'dial_ip': '192.168.0.114', 'dial_code': '6027',
         'answer_ip': '192.168.0.115', 'code': '6029',
         'tripartite_ip': '192.168.0.116', 'tripartite_code': '6021', "cycle_number": cycle_number}
    ]

    params8 = [
        {'service_uuid': '1111', 'case_uuid': '222', 'dial_ip': '192.168.0.91', 'dial_code': '6050',
         'answer_ip': '192.168.0.92', 'code': '6010',
         'tripartite_ip': '192.168.0.94', 'tripartite_code': '6015', 'tripartite_two_ip': '192.168.30.159',
         'tripartite_two_code': '6021'}
    ]

    params9 = [
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.143', 'dial_code': '6000',
         'answer_ip': '192.168.30.148', 'code': '6052',
         'tripartite_ip': '192.168.30.147', 'tripartite_code': '6002', 'tripartite_two_ip': '192.168.30.154',
         'tripartite_two_code': '6004'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.144', 'dial_code': '6005',
         'answer_ip': '192.168.30.159', 'code': '6006',
         'tripartite_ip': '192.168.30.160', 'tripartite_code': '6007', 'tripartite_two_ip': '192.168.30.157',
         'tripartite_two_code': '6008'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.156', 'dial_code': '6009',
         'answer_ip': '192.168.30.142', 'code': '6011',
         'tripartite_ip': '192.168.30.152', 'tripartite_code': '6012', 'tripartite_two_ip': '192.168.30.150',
         'tripartite_two_code': '6013'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.145', 'dial_code': '6014',
         'answer_ip': '192.168.30.151', 'code': '6017',
         'tripartite_ip': '192.168.30.149', 'tripartite_code': '6023', 'tripartite_two_ip': '192.168.30.148',
         'tripartite_two_code': '6052'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.30.138', 'dial_code': '6025',
         'answer_ip': '192.168.30.153', 'code': '6003',
         'tripartite_ip': '192.168.30.137', 'tripartite_code': '6019', 'tripartite_two_ip': '192.168.30.139',
         'tripartite_two_code': '6022'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.0.107', 'dial_code': '6018',
         'answer_ip': '192.168.0.109', 'code': '6020',
         'tripartite_ip': '192.168.0.111', 'tripartite_code': '6028', 'tripartite_two_ip': '192.168.0.112',
         'tripartite_two_code': '6024'},
        {'service_uuid': service_uuid, 'case_uuid': case_uuid, 'dial_ip': '192.168.0.113', 'dial_code': '6026',
         'answer_ip': '192.168.0.114', 'code': '6027',
         'tripartite_ip': '192.168.0.115', 'tripartite_code': '6029', 'tripartite_two_ip': '192.168.0.116',
         'tripartite_two_code': '6021'}]

    # sql = "SELECT * FROM  phone_manage  WHERE 1=1 AND  status = {}".format(1)
    # json_data = mysql.fetchall_db(sql)
    # 匹配数据

    params10 = [
        {'service_uuid': '1111', 'case_uuid': '222', 'dial_ip': '192.168.0.91', 'dial_code': '6050',
         'answer_ip': '192.168.30.144', 'code': '6005',
         'tripartite_ip': '192.168.30.159', 'tripartite_code': '6006', 'tripartite_two_ip': '192.168.30.160',
         'tripartite_two_code': '6007', 'tripartite_three_ip': '192.168.0.94',
         'tripartite_three_code': '6015', 'tripartite_four_ip': '192.168.0.92',
         'tripartite_four_code': '6010'}
    ]

    service_uuid = "955456623b924ef9981aaa3891fc7e19"
    sql = "SELECT B.* FROM " \
          "phone_service_info A " \
          "LEFT JOIN phone_manage B " \
          "ON A.phone_uuid = B.uuid " \
          "WHERE A.service_uuid = '{}'".format(service_uuid)
    json_data = mysql.fetchall_db(sql)
    phone_list = allocation_phone(json_data, 6)
    print(phone_list)

    runPool = RunPool()
    # runPool.run(params, call_hold_test_case, 500)
    # runPool.run(params2, call_hold_test_case, 2)错误
    runPool.run(phone_list, phone_conference_six_verification, 200)
    # runPool.run_result(params4, blind_turn_answer_case_result)
    log.info("----------------------test case 执行完成，共计运行[{}]次--------------------", runPool.count_num - 1)
