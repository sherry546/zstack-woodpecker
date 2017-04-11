'''

Integration Test for creating KVM VM in MN HA mode with all mn hosts shutdown and recovery.

@author: Mirabel
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.operations.node_operations as node_ops
import zstackwoodpecker.zstack_test.zstack_test_vm as test_vm_header
import test_stub
import random
import time
import os

vm = None
mn_host_list = None
need_recover_mn_host_list = None

def test():
    global vm
    global mn_host_list
    global need_recover_mn_host_list
    mn_host_list = test_stub.get_mn_host(test_lib.all_scenario_config, test_lib.scenario_file)
    mn_host_num = len(mn_host_list)
    test_mn_host_list = random.sample(range(mn_host_num), (mn_host_num + 1) / 2)

    for host in mn_host_list:
        test_util.test_logger("shutdown host [%s]" % (host.ip_))
        test_stub.stop_host(host, test_lib.all_scenario_config)

    need_recover_mn_host_list = range(mn_host_num)

    test_util.test_logger("wait 10s for MN VM to stop")
    mn_host = test_stub.get_host_by_mn_vm(test_lib.all_scenario_config, test_lib.scenario_file)
    if len(mn_host) != 0:
        test_util.test_fail('MN VM is still running on %d host(s)' % len(mn_host))

    for index in test_mn_host_list:
        test_util.test_logger("recover host [%s]" % (mn_host_list[index].ip_))
        test_stub.recover_host(mn_host_list[index], test_lib.all_scenario_config, test_lib.deploy_config)
        need_recover_mn_host_list.remove(index)

    test_util.test_logger("wait for 50 seconds to see if management node VM starts on any host")
    time.sleep(50)
    try:
        new_mn_host = test_stub.get_host_by_mn_vm(test_lib.all_scenario_config, test_lib.scenario_file)
        if len(new_mn_host) == 0:
            test_util.test_fail("management node VM does not start after ha status is ready")
        elif len(new_mn_host) > 1:
            test_util.test_fail("management node VM starts on more than one host after ha status is ready")
    except:
        test_util.test_fail("management node VM does not start after ha status is ready")
    test_util.test_logger("wait for 5 minutes to see if management node starts again")
    try:
        node_ops.wait_for_management_server_start(300)
    except:
        test_util.test_fail("management node does not recover after MN VM is running")

    test_util.test_logger("try to create vm, timeout is 30s")
    time_out = 30
    while time_out > 0:
        try:
            vm = test_stub.create_basic_vm()
            break
        except:
            time.sleep(1)
            time_out -= 1
    if time_out == 0:
        test_util.test_fail('Fail to create vm after mn is ready')

    vm.check()
    vm.destroy()

    test_util.test_pass('Create VM Test Success')

#Will be called what ever test result is
def env_recover():
    if need_recover_mn_host_list:
        for index in need_recover_mn_host_list:
            test_util.test_logger("recover host: %s" % (mn_host_list[index].ip_))
            test_stub.recover_host(mn_host_list[index], test_lib.all_scenario_config, test_lib.deploy_config)

#Will be called only if exception happens in test().
def error_cleanup():
    global vm
    if vm:
        try:
            vm.destroy()
        except:
            pass