import thriftpy

foraging_thrift = thriftpy.load("../foraging.thrift", module_name="foraging_thrift")

print 'Top Level       -> ' + str(dir(foraging_thrift))
print 'Root            -> ' + str(dir(foraging_thrift.Root))
print 'StateInitialize -> ' + str(dir(foraging_thrift.StateInitialize))
print 'RuleSet         -> ' + str(dir(foraging_thrift.RuleSet))
print 'ProbInitState   -> ' + str(dir(foraging_thrift.ProbInitState))

root = foraging_thrift.Root()
root.init = foraging_thrift.StateInitialize()
root.init.init_1 = foraging_thrift.ProbInitState.PROB_INIT_STATE_0

print dir(foraging_thrift.StateInitialize)
print dir(root.init)
print foraging_thrift.StateInitialize.thrift_spec
print root.init.thrift_spec

print '\n'
print root
print root.init
print root.init.init_1
print '\n'


import thriftpy.transport as tran
import thriftpy.protocol as prot

transOut = tran.TMemoryBuffer()
protocolOut = prot.TBinaryProtocol(transOut)
root.write(protocolOut)
print transOut.getvalue()

def wrap_it(object):

    return dict((key, value + (object,)) for key, value in object.thrift_spec.iteritems())

print wrap_it(root).values()