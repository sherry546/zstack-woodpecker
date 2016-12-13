'''
test for add and delete vcenter
@author: SyZhao
'''

import apibinding.inventory as inventory
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.vm_operations as vm_ops
import zstackwoodpecker.operations.vcenter_operations as vct_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import zstacklib.utils.ssh as ssh
import test_stub


vcenter1_name = "VCENTER1"
vcenter1_domain_name = "172.20.198.198"
vcenter1_username = "administrator@vsphere.local"
vcenter1_password = "Testing%123"

vcenter_uuid = None

vm_name_pattern1 = "vm-fingerprint1"
vm_name_pattern2 = "vm-fingerprint2"

def test():
    global vcenter_uuid

    #add vcenter senario1:
    zone_uuid = res_ops.get_resource(res_ops.ZONE, name = zone_name)[0].uuid
    inv = vct_ops.add_vcenter(vcenter1_name, vcenter1_domain_name, vcenter1_username, vcenter1_password, true, zone_uuid)
    vcenter_uuid = inv.uuid


    #insert the basic operations for the newly join in vcenter resourse
    vm_list = []
    vms_name = res_ops.query_resource_fields(res_ops.VM_INSTANCE, [], None, fields=['name'])
    for vm_name in vms_name:
        vm_list.append(vm_name.name)

    if vm_name_pattern1 not in vm_list and vm_name_pattern2 not in vm_list:
        test_util.test_fail("newly joined vcenter missing fingerprint vm1, test failed")



    vct_ops.delete_vcenter(vcenter_uuid)
    test_util.test_pass("add && delete vcenter test passed.")



def error_cleanup():
    global vcenter_uuid
    if vcenter_uuid:
        vct_ops.delete_vcenter(vcenter_uuid)