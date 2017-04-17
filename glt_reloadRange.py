# Nuke frame range fixer
# Select read nodes and run the script. It will find the starting and ending frame in the sequence (if exist), and set the frame range to it. 
# (It skips other type of nodes, so you may select other types too)
# Works only if counter is before the extension, and preceded by a . (point)
# Example:
# .../AX1_020_001-cg_fx_v008_cow_beauty.0108.iff
# Useful for example if a 3d rendered sequence is loaded in nuke before the render has ended. 
# Comments are welcome
# by Gabor L. Toth (gltoth@gmail.com)


# version 1.13  2016-10-19	- Working with deep read nodes
# version 1.12  2016-02-05	- Silent mode
# version 1.11  2014-01-10	- Changing max frame digits from 6 to 10
# version 1.10  2013-05-23	- Handling sequences with expressions in them 
# version 1.07  2011-06-07	- Inserting %0xd  if not found, but there is a counter-like string ('.' followed by 1-6 digits then '.' again) 
# version 1.06  2010-08-23	- can be fed with a separate nodename, for cmdline
# version 1.05  2009-11-10	- fixed sorting for linux
# version 1.00  2009-10-21	- cleaned up version
# version 0.12  2009-10-16	- skipping not existing directories
# version 0.11  2009-09-10	- works properly with multiple sequences in the same folder. Handles pattern other than %04d too.
# version 0.10  2009-09-09	- initial version 

import nuke
import os
import os.path
import math
import glob
import re


def glt_reloadRange(node='' , silent=0):
    sn = []
    if node == '':
        sn = [n for n in nuke.selectedNodes() if n.Class() == "Read" or n.Class() == "DeepRead"]
    else:
        sn.append(nuke.toNode(node))
    print '\n<Glt_reloadRange> is running, silent = %s' % silent
    if sn != []:
        for n in sn:

            seqPathEval = n.knob('file').getEvaluatedValue()
            seqPathOriginal = n.knob('file').value()  # could contain expressions

            if seqPathEval is not None:
                frame = re.search('\.[0-9]{1,10}\.' , seqPathEval).group()

                if not silent:
                    print 'Framenumber : %s' % frame
                pad = len(re.search('\.[0-9]{1,10}\.' , seqPathEval).group()) - 2
                seqPathEvalWithPCounter = re.sub('\.[0-9]{1,10}\.' , ('.%0' + str(pad) + 'd.') , seqPathEval)

                if re.match('.*\.%0[0-9]d.*' , seqPathOriginal) == None:
                    if re.search('.+\.[0-9]+\..+' , seqPathOriginal):
                        seqPathOriginal = re.sub('\.[0-9]{1,10}\.' , ('.%0' + str(pad) + 'd.') , seqPathOriginal)
                        n.knob('file').setValue(seqPathOriginal)
                        print 'Changed readnode path, inserted %0xd counter!'
                    else:
                        print 'No counter!'
                        return

                indx = seqPathEvalWithPCounter.find('%0')  # getting padding format
                pattern = '%0' + seqPathEvalWithPCounter[indx + 2] + 'd'
                seqPathMask = seqPathEvalWithPCounter.replace(pattern ,
                                                              '*')  # replacing %04d	'AUH_010_001-cg_li_v002_H1BodyRL.beauty.*.iff'

                if not silent:
                    print '\nPathMask: %s' % (seqPathMask)
                seqDir = os.path.dirname(seqPathEvalWithPCounter)
                if not silent:
                    print 'Directory: %s' % (seqDir)
                if os.path.exists(seqDir):
                    files = os.listdir(seqDir)
                    # print files

                    # sorting files
                    filteredFiles = glob.glob(seqPathMask)
                    filteredFiles.sort()
                    if len(filteredFiles) != 0:
                        (firstFileName , ext) = os.path.splitext(filteredFiles[0])
                        firstFileTags = firstFileName.split('.')

                        sfs = firstFileTags[-1]
                        if not silent:
                            print 'Extension: ' + ext
                        sf = int(sfs)  # converted to int
                        if not silent:
                            print "Start frame: %s" % (sf)

                        (lastFileName , ext) = os.path.splitext(filteredFiles[len(filteredFiles) - 1])
                        lastFileTags = lastFileName.split('.')
                        efs = lastFileTags[-1]
                        ef = int(efs)
                        if not silent:
                            print "End frame: %s" % (ef)

                        n.knob('first').setValue(sf)
                        n.knob('last').setValue(ef)
                    else:
                        if not silent:
                            print 'No matching files in this directory! Skipping...'
                else:
                    if not silent:
                        print 'Warning! Directory doesnt exist: ' + seqDir
            else:
                pass
    else:
        print 'No selection'
