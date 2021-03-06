#! /usr/bin/env python
import os, sys
import ROOT
counters = {}
badFiles = []

def isint(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def getBaseNames(dirname,reqExt):
    names = set()
    for item in os.listdir(dirname):
        filename, ext = os.path.splitext(item)
        filename, sec_ext= os.path.splitext(filename)
        print 'filename=',filename,' sec_ext=',sec_ext,' ext=',ext 
        if not ext == reqExt: continue
        print 'flag: reqExt=',reqExt,' ext=',ext

        try:
            goodFile=True
            
            #fIn=ROOT.TFile.Open(dirname+'/'+item)
            #goodFile = False
            #try:
            #    if fIn and not fIn.IsZombie() and not fIn.TestBit(ROOT.TFile.kRecovered):
            #        goodFile = True
            #except:
            #    pass
            basename, number = filename.rsplit('_',1)            
            if not number == 'missing' and not isint(number):
                if 'w' in number: 
                    number,sec_ext=number.split('w')
                    sec_ext ='w%s'%sec_ext
                if not isint(number):
                    raise ValueError
            if len(sec_ext)!=0: basename=basename+sec_ext
            if (not goodFile):
                badFiles.append(dirname+'/'+item)
                continue

            try:
                counters[basename].append(dirname+'/'+item)
            except KeyError:
                counters[basename] = [dirname+'/'+item]
            names.add(basename)
            
        except ValueError:
            print filename,'is single'
            names.add(filename)
            
    return names

try:
    inputdir = sys.argv[1]
    if not os.path.isdir(inputdir):
        print "Input directory not found:", inputdir
        exit(-1)
    outputdir = sys.argv[2]
    if not os.path.isdir(outputdir):
        print "Output directory not found:", outputdir
        exit(-1)
except IndexError:
    print "Need to provide an input and output directories."
    exit(-1)

for ext in ['.root','.yoda']:

    basenames = getBaseNames(inputdir,ext)
    print '-----------------------'
    print 'Will process the following samples:', basenames

    for basename, files in counters.iteritems():

        filenames = " ".join(files)
    
        # merging:
        print '... processing', basename
    
        if ext=='.root':
            target = os.path.join(outputdir,"%s.root" % basename)
            cmd = 'hadd -f -k %s %s' % (target, filenames)
            #print cmd
            os.system(cmd)
            #os.system('rm %s'%filenames)

        else:
            target = os.path.join(outputdir,"%s.yoda" % basename)
            if len(files)==1:
                cmd='mv -v %s %s'%(files[0],target)
                os.system(cmd)
            else:                
                cmd = 'yodamerge -o %s %s' % (target, filenames)
                print cmd
                os.system(cmd)
                #os.system('rm %s'%filenames)

if (len(badFiles) > 0):
    print '-----------------------'
    print 'The following files are not done yet or require resubmission, please check LSF output:', badFiles
