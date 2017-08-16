
from WMCore.Configuration import Configuration
import os
config = Configuration()

config.section_("General")
config.General.requestName = "ZJ_ptsqmin4_tune0"
config.General.workArea = "grid"
config.General.transferOutputs=True

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "/afs/cern.ch/work/k/kjpena/CMSSW_8_0_8_patch1/src/UserCode/VptGenAnalysis/test/runGENFromLHEandAnalysis_cfg.py"
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ['%s.root'%config.General.requestName] 
config.JobType.outputFiles += ['%s.w%d.yoda'%(config.General.requestName,x) for x in xrange(0,121)]
config.JobType.pyCfgParams = [
			   'output=%s'%config.General.requestName,
			   'ueTune=CUETP8M1',
			   'photos=False',
			   'nFinal=2',
			   'doRivetScan=True',
			   'usePoolSource=True'
			   ]
config.section_("Data")
config.Data.inputDataset = "/ZJ_ZToMuMu_powheg_minlo_8TeV_NNPDF30_ptsqmin4/RunIIWinter15wmLHE-MCRUN2_71_V1-v1/LHE"
config.Data.inputDBS = "global"
config.Data.splitting = "EventAwareLumiBased" #"EventBased"
config.Data.unitsPerJob = 5000
#config.Data.totalUnits = config.Data.unitsPerJob * 10
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.outLFNDirBase = '/store/group/phys_smp/Wmass/kjpena/%s'%config.General.requestName

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
