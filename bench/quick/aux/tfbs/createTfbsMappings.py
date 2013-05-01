import third_party.safeshelve as safeshelve
import os

from quick.aux.CustomFuncCatalog import reverseMappingHavingListValues
from config.Config import HB_SOURCE_CODE_BASE_DIR
DATA_PATH = os.sep.join([HB_SOURCE_CODE_BASE_DIR, 'data', 'tfbs'])

pwm2TFids = safeshelve.open(DATA_PATH + os.sep + 'pwm2TFids.shelf', 'r')
pwm2TFnamesNew = safeshelve.open(DATA_PATH + os.sep + 'pwm2TFnamesNew.shelf', 'r')
pwmName2id = safeshelve.open(DATA_PATH + os.sep + 'pwmName2id.shelf', 'r')
TfId2Class = safeshelve.open(DATA_PATH + os.sep + 'TfId2Class.shelf', 'r')
pwmIdToPretty = safeshelve.open(DATA_PATH + os.sep + 'pwm2pretties.shelf', 'r')

pwmName2TfClassesFn = DATA_PATH + os.sep + 'pwmName2TfClasses.shelf'
pwmName2TfNamesFn = DATA_PATH + os.sep + 'pwmName2TfNames.shelf'
pwmName2PrettyNamesFn = DATA_PATH + os.sep + 'pwmName2PrettyNames.shelf'

pwmName2TfClasses = safeshelve.open(pwmName2TfClassesFn, 'c')
pwmName2TfNames = safeshelve.open(pwmName2TfNamesFn, 'c')
pwmName2PrettyNames = safeshelve.open(pwmName2PrettyNamesFn, 'c')

tfNames2pwmNamesFn = DATA_PATH + os.sep + 'tfNames2pwmNames.shelf'
tfClasses2pwmNamesFn = DATA_PATH + os.sep + 'tfClasses2pwmNames.shelf'
prettyNames2pwmNamesFn = DATA_PATH + os.sep + 'prettyNames2pwmNames.shelf'

pwnId2Classes = {}

for id in pwm2TFids.keys():
    for tfid in pwm2TFids[id]:
        tfClass = TfId2Class.get(tfid)
        if tfClass is None:
            continue
        tfClass = tfClass.replace('\n','').replace('.','')
        tfClass = tfClass[0].upper() + tfClass[1:]
        if id not in pwnId2Classes:
            pwnId2Classes[id] = []
        pwnId2Classes[id].append(tfClass)

#pwmId2Name = {}
#for key,val in pwmName2id.iteritems():
#    pwmId2Name[val] = key

#for id in pwmId2Name:

pwmName2TfClasses.clear()
pwmName2TfNames.clear()
pwmName2PrettyNames.clear()

for name, id in pwmName2id.iteritems():
    if pwnId2Classes.get(id) is None:
        continue
    pwmName2TfClasses[name.lower()] = sorted(set(pwnId2Classes[id]))

for name, id in pwmName2id.iteritems():
    if pwm2TFnamesNew.get(id) is None:
        continue
    pwmName2TfNames[name.lower()] = sorted(set(pwm2TFnamesNew[id]))

for name in pwmName2id.keys():
    if pwmIdToPretty.get(name) is None:
        continue
    pwmName2PrettyNames[name.lower()] = sorted(set(pwmIdToPretty[name]))

pwmName2TfClasses.close()
pwmName2TfNames.close()
pwmName2PrettyNames.close()

reverseMappingHavingListValues(pwmName2TfClassesFn, tfClasses2pwmNamesFn)
reverseMappingHavingListValues(pwmName2TfNamesFn, tfNames2pwmNamesFn)
reverseMappingHavingListValues(pwmName2PrettyNamesFn, prettyNames2pwmNamesFn)