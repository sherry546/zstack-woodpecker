'''

Integration Test Teardown case

@author: Youyk
'''

import zstackwoodpecker.setup_actions as setup_actions
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.clean_util as clean_util
import zstackwoodpecker.test_lib as test_lib
from zstacklib.utils import linux
from zstacklib.utils import http
import os.path
from zstacktestagent.plugins import host as host_plugin
from zstacktestagent import testagent

def test():
    clean_util.cleanup_all_vms_violently()
    clean_util.cleanup_none_vm_volumes_violently()
    clean_util.umount_all_primary_storages_violently()
    clean_util.cleanup_backup_storage()
    test_lib.setup_plan.stop_node()
    cmd = host_plugin.DeleteVlanDeviceCmd()
    
    hosts = test_lib.lib_get_all_hosts_from_plan()
    if type(hosts) != type([]):
        hosts = [hosts]

    for host in hosts:
        cmd.vlan_ethname = 'eth0.10'
        http.json_dump_post(testagent.build_http_path(host.managementIp_, host_plugin.DELETE_VLAN_DEVICE_PATH), cmd)
        cmd.vlan_ethname = 'eth0.11'
        http.json_dump_post(testagent.build_http_path(host.managementIp_, host_plugin.DELETE_VLAN_DEVICE_PATH), cmd)

    test_lib.lib_cleanup_host_ip_dict()
    test_util.test_pass('VirtualRouter Teardown Success')
