'''

New Integration test for testing vm migration between hosts with some ops.

@author: quarkonics
'''
import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib

vm = None
test_stub = test_lib.lib_get_test_stub()

def test():
    global vm
    vm = test_stub.create_vr_vm('migrate_vm', 'imageName_s', 'l3VlanNetwork2')
    vm.check()

    test_stub.migrate_vm_to_random_host(vm)
    vm.check()

    vm.reboot()
    vm.check()

    vm.destroy()
    test_util.test_pass('Migrate VM Ops Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global vm
    if vm:
        try:
            vm.destroy()
        except:
            pass

