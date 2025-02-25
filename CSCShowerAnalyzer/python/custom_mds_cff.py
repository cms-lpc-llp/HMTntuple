import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

# CSC clusters
from RecoMuon.MuonRechitClusterProducer.cscRechitClusterProducer_cfi import cscRechitClusterProducer
from RecoMuon.MuonRechitClusterProducer.dtRechitClusterProducer_cfi import dtRechitClusterProducer 

cscMDSClusterTable = cms.EDProducer("SimpleMuonRecHitClusterFlatTableProducer",
    src  = cms.InputTag("ca4CSCrechitClusters"),
    name = cms.string("cscMDSHLTCluster"),
    doc  = cms.string("MDS cluster at HLT"),
    variables = cms.PSet(
        eta = Var("eta", float, doc="cluster eta"),
        phi = Var("phi", float, doc="cluster phi"),
        x   = Var("x"  , float, doc="cluster x"),
        y   = Var("y"  , float, doc="cluster y"),
        z   = Var("z"  , float, doc="cluster z"),
        r   = Var("r"  , float, doc="cluster r"),
        size   = Var("size"  , int, doc="cluster size"),
        nStation   = Var("nStation"  , int, doc="cluster nStation"),
        avgStation   = Var("avgStation"  , float, doc="cluster avgStation"),
        nMB1   = Var("nMB1"  , int, doc="cluster nMB1"),
        nMB2   = Var("nMB2"  , int, doc="cluster nMB2"),
        nME11   = Var("nME11"  , int, doc="cluster nME11"),
        nME12   = Var("nME12"  , int, doc="cluster nME12"),
        nME41   = Var("nME41"  , int, doc="cluster nME41"),
        nME42   = Var("nME42"  , int, doc="cluster nME42"),
        time   = Var("time"  , float, doc="cluster time = avg cathode and anode time"),
        timeSpread   = Var("timeSpread"  , float, doc="cluster timeSpread")
    )
)

dtMDSClusterTable = cscMDSClusterTable.clone(
    src = cms.InputTag("ca4DTrechitClusters"),
    name= cms.string("dtMDSHLTCluster")
)

from HMTntuple.CSCShowerAnalyzer.cscShowerDigiTable_cfi import cscShowerDigiTable

dataCSCdigiTable = cscShowerDigiTable.clone(
    LCTShower = cms.InputTag("muonCSCDigis","MuonCSCShowerDigi"),
    name = cms.string("lct")
)
emulCSCdigiTable = cscShowerDigiTable.clone(
    LCTShower =  cms.InputTag("cscTriggerPrimitiveDigis"),
    name = cms.string("elct")
)

from HMTntuple.CSCShowerAnalyzer.cscRechitsTable_cfi import cscRechitsTable 
from HMTntuple.CSCShowerAnalyzer.dtRechitsTable_cfi import dtRechitsTable 
from HMTntuple.CSCShowerAnalyzer.rpcRechitsTable_cfi import rpcRechitsTable 
from HMTntuple.CSCShowerAnalyzer.cscSegmentsTable_cfi import cscSegmentsTable 
from HMTntuple.CSCShowerAnalyzer.dtSegmentsTable_cfi import dtSegmentsTable 

cscRechitsTable = cscRechitsTable.clone( 
    recHitLabel = cms.InputTag("csc2DRecHits")
)
dtRechitsTable = dtRechitsTable.clone( 
    recHitLabel = cms.InputTag("dt1DRecHits")
)
rpcRechitsTable = rpcRechitsTable.clone( 
    recHitLabel = cms.InputTag("rpcRecHits")
)
cscSegmentsTable = cscSegmentsTable.clone( 
    segmentLabel = cms.InputTag("cscSegments")
)
dtSegmentsTable = dtSegmentsTable.clone( 
    segmentLabel = cms.InputTag("dt4DSegments")
)


def add_mdsTables(process, MDSshowerDigi=False,saveRechits=False):

    process.ca4CSCrechitClusters = cscRechitClusterProducer    
    process.ca4DTrechitClusters = dtRechitClusterProducer
    process.cscMDSClusterTable = cscMDSClusterTable
    process.dtMDSClusterTable = dtMDSClusterTable 

    process.MDSTask = cms.Task(process.ca4CSCrechitClusters)
    process.MDSTask.add(process.ca4DTrechitClusters)
    process.MDSTask.add(process.cscMDSClusterTable)
    process.MDSTask.add(process.dtMDSClusterTable)

    if MDSshowerDigi:
        process.load("CalibMuon.CSCCalibration.CSCL1TPLookupTableEP_cff")
        process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
        process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
        process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"
        process.cscTriggerPrimitiveDigis.commonParam.runME11ILT = False
        process.cscTriggerPrimitiveDigis.commonParam.runME21ILT = False

        process.dataCSCdigiTable = dataCSCdigiTable 
        process.emulCSCdigiTable = emulCSCdigiTable 

        process.MDSTask.add(process.cscTriggerPrimitiveDigis)
        process.MDSTask.add(process.dataCSCdigiTable)
        process.MDSTask.add(process.emulCSCdigiTable)

    if saveRechits:
        process.cscRechitsTable = cscRechitsTable
        process.dtRechitsTable = dtRechitsTable
        process.rpcRechitsTable = rpcRechitsTable
        process.cscSegmentsTable = cscSegmentsTable 
        process.dtSegmentsTable = dtSegmentsTable 
        process.MDSTask.add(process.cscRechitsTable)
        process.MDSTask.add(process.dtRechitsTable)
        process.MDSTask.add(process.rpcRechitsTable)
        process.MDSTask.add(process.cscSegmentsTable)
        process.MDSTask.add(process.dtSegmentsTable)


    process.nanoTableTaskCommon.add(process.MDSTask)

    return process
