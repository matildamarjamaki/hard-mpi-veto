# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/powheg_herwig_dijet_fragment.py --python_filename powheg_herwig_dijet_GEN_cfg.py --fileout file:powheg_herwig_dijet_GEN.root --mc --eventcontent RAWSIM --datatier GEN --conditions auto:run3_mc_FULL --beamspot DBrealistic --step LHE,GEN --era Run3_2024 --nThreads 1 -n 5 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_2024_cff import Run3_2024

process = cms.Process('GEN',Run3_2024)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring("file:__NUMBERED_LHE__")
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/powheg_herwig_dijet_fragment.py nevts:5'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(1),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string("file:__OUTPUT_ROOT__"),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_mc_FULL', '')

process.generator = cms.EDFilter("Herwig7HadronizerFilter",
    configFiles = cms.vstring(),
    crossSection = cms.untracked.double(-1),
    dataLocation = cms.string('${HERWIGPATH:-6}'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    filterEfficiency = cms.untracked.double(1.0),
    generatorModule = cms.string('/Herwig/Generators/EventGenerator'),
    herwig7CH3AlphaS = cms.vstring(
        'cd /Herwig/Shower',
        'set AlphaQCD:AlphaIn 0.118',
        'cd /'
    ),
    herwig7CH3MPISettings = cms.vstring(
        'set /Herwig/Hadronization/ColourReconnector:ReconnectionProbability 0.4712',
        'set /Herwig/UnderlyingEvent/MPIHandler:pTmin0 3.04',
        'set /Herwig/UnderlyingEvent/MPIHandler:InvRadius 1.284',
        'set /Herwig/UnderlyingEvent/MPIHandler:Power 0.1362'
    ),
    herwig7CH3PDF = cms.vstring(
        'cd /Herwig/Partons',
        'create ThePEG::LHAPDF PDFSet_nnlo ThePEGLHAPDF.so',
        'set PDFSet_nnlo:PDFName NNPDF31_nnlo_as_0118.LHgrid',
        'set PDFSet_nnlo:RemnantHandler HadronRemnants',
        'set /Herwig/Particles/p+:PDF PDFSet_nnlo',
        'set /Herwig/Particles/pbar-:PDF PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:FirstPDF  PDFSet_nnlo',
        'set /Herwig/Partons/PPExtractor:SecondPDF PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFA PDFSet_nnlo',
        'set /Herwig/Shower/ShowerHandler:PDFB PDFSet_nnlo',
        'create ThePEG::LHAPDF PDFSet_lo ThePEGLHAPDF.so',
        'set PDFSet_lo:PDFName NNPDF31_lo_as_0130.LHgrid',
        'set PDFSet_lo:RemnantHandler HadronRemnants',
        'set /Herwig/Shower/ShowerHandler:PDFARemnant PDFSet_lo',
        'set /Herwig/Shower/ShowerHandler:PDFBRemnant PDFSet_lo',
        'set /Herwig/Partons/MPIExtractor:FirstPDF PDFSet_lo',
        'set /Herwig/Partons/MPIExtractor:SecondPDF PDFSet_lo',
        'cd /'
    ),
    herwig7StableParticlesForDetector = cms.vstring(
        'set /Herwig/Decays/DecayHandler:MaxLifeTime 10*mm',
        'set /Herwig/Decays/DecayHandler:LifeTimeOption Average'
    ),
    hw_lhe_common_settings = cms.vstring(
        'cd /Herwig/EventHandlers',
        'library LesHouches.so',
        'create ThePEG::LesHouchesEventHandler LesHouchesHandler',
        'set LesHouchesHandler:PartonExtractor /Herwig/Partons/PPExtractor',
        'set LesHouchesHandler:CascadeHandler /Herwig/Shower/ShowerHandler',
        'set LesHouchesHandler:DecayHandler /Herwig/Decays/DecayHandler',
        'set LesHouchesHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler',
        'set LesHouchesHandler:WeightOption VarNegWeight',
        'set LesHouchesHandler:EventNumbering LHE',
        'set /Herwig/Generators/EventGenerator:EventHandler /Herwig/EventHandlers/LesHouchesHandler',
        'create ThePEG::Cuts /Herwig/Cuts/NoCuts',
        'create ThePEG::LHAPDF /Herwig/Partons/LHAPDF ThePEGLHAPDF.so',
        'set /Herwig/Partons/LHAPDF:PDFName NNPDF31_nnlo_as_0118',
        'set /Herwig/Partons/LHAPDF:RemnantHandler /Herwig/Partons/HadronRemnants',
        'set /Herwig/Particles/p+:PDF /Herwig/Partons/LHAPDF',
        'set /Herwig/Particles/pbar-:PDF /Herwig/Partons/LHAPDF',
        'set /Herwig/Partons/PPExtractor:FirstPDF  /Herwig/Partons/LHAPDF',
        'set /Herwig/Partons/PPExtractor:SecondPDF /Herwig/Partons/LHAPDF',
        'create ThePEG::LesHouchesFileReader LesHouchesReader',
        'set LesHouchesReader:FileName __NUMBERED_LHE__',
        'set LesHouchesReader:AllowedToReOpen No',
        'set LesHouchesReader:InitPDFs 0',
        'set LesHouchesReader:Cuts /Herwig/Cuts/NoCuts',
        'set LesHouchesReader:MomentumTreatment RescaleEnergy',
        'set LesHouchesReader:PDFA /Herwig/Partons/LHAPDF',
        'set LesHouchesReader:PDFB /Herwig/Partons/LHAPDF',
        'insert LesHouchesHandler:LesHouchesReaders 0 LesHouchesReader',
        'set /Herwig/Shower/ShowerHandler:MaxPtIsMuF Yes',
        'set /Herwig/Shower/ShowerHandler:RestrictPhasespace Yes',
        'set /Herwig/Shower/ShowerHandler:MPIHandler NULL',
        'set /Herwig/Shower/PartnerFinder:PartnerMethod Random',
        'set /Herwig/Shower/PartnerFinder:ScaleChoice Partner'
    ),
    hw_lhe_powheg_settings = cms.vstring(
        'set /Herwig/Shower/ShowerHandler:MaxPtIsMuF Yes',
        'set /Herwig/Shower/ShowerHandler:RestrictPhasespace Yes',
        'set /Herwig/Shower/ShowerHandler:MPIHandler NULL',
        'set /Herwig/Shower/PartnerFinder:PartnerMethod Random',
        'set /Herwig/Shower/PartnerFinder:ScaleChoice Partner',
        'set /Herwig/Particles/t:NominalMass 172.5'
    ),
    parameterSets = cms.vstring(
        'herwig7CH3PDF',
        'herwig7CH3AlphaS',
        'herwig7CH3MPISettings',
        'herwig7StableParticlesForDetector',
        'hw_lhe_common_settings',
        'hw_lhe_powheg_settings'
    ),
    repository = cms.string('${HERWIGPATH}/HerwigDefaults.rpo'),
    run = cms.string('InterfaceMatchboxTest'),
    runModeList = cms.untracked.string('read,run'),
    seed = cms.untracked.int32(12345)
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfConcurrentLuminosityBlocks = 1
process.options.eventSetup.numberOfConcurrentIOVs = 1
# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path).insert(0, process.ProductionFilterSequence)



# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
