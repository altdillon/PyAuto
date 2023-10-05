from cInst_oscilloscope import cInst_oscilloscope
import ctypes, ctypes.util

class cInst_ps6404D_oscilloscope(cInst_oscilloscope):
    '''
    TBD
    '''
    def __init__(self, inst, inst_id, connection_mode, address):
        super().__init__(inst, inst_id, connection_mode, address)
        self.type = 'oscilloscope'
        self.ps6000 = ctypes.WinDLL(ctypes.util.find_library("ps6000"))
        
    def comm(self,command):
        raise ValueError('Comm is not available for non-visa devices. Use the library (.ps6000) and the handle (.inst) to make a raw command.')

    def set_address(self, address):
        pass

    def launch_gui(self):
        pass

    def reset(self):
        pass

    def disconnect(self):
        self.ps6000['ps6000CloseUnit'](self.inst)

    """ PICO_STATUS ps6000GetUnitInfo
        (
            int16_t    handle,
            int8_t    *string,
            int16_t    stringLength,
            int16_t   *requiredSize,
            PICO_INFO  info
        ); """
    make_symbol(ldlib, "GetUnitInfo", "ps6000GetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

    """ PICO_STATUS ps6000FlashLed
        (
            int16_t  handle,
            int16_t  start
        ); """
    make_symbol(ldlib, "FlashLed", "ps6000FlashLed", c_uint32, [c_int16, c_int16])

    """ PICO_STATUS ps6000MemorySegments
        (
            int16_t   handle,
            uint32_t  nSegments,
            uint32_t *nMaxSamples
        );  """
    make_symbol(ldlib, "MemorySegments", "ps6000MemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

    """ PICO_STATUS ps6000SetChannel
        (
            int16_t                   handle,
            PS6000_CHANNEL            channel,
            int16_t                   enabled,
            PS6000_COUPLING           type,
            PS6000_RANGE              range,
            float                     analogueOffset,
            PS6000_BANDWIDTH_LIMITER  bandwidth
        ); """
    make_symbol(ldlib, "SetChannel", "ps6000SetChannel", c_uint32,
                [c_int16, c_int32, c_int16, c_int32, c_int32, c_float, c_int32])

    """ PICO_STATUS ps6000GetTimebase
        (
            int16_t   handle,
            uint32_t  timebase,
            uint32_t  noSamples,
            int32_t  *timeIntervalNanoseconds,
            int16_t   oversample,
            uint32_t *maxSamples,
            uint32_t  segmentIndex
        ); """

    """ PICO_STATUS ps6000GetTimebase2
        (
            int16_t   handle,
            uint32_t  timebase,
            uint32_t  noSamples,
            float    *timeIntervalNanoseconds,
            int16_t   oversample,
            uint32_t *maxSamples,
            uint32_t  segmentIndex
        ); """
    make_symbol(ldlib, "GetTimebase", "ps6000GetTimebase2", c_uint32,
                [c_int16, c_uint32, c_uint32, c_void_p, c_int16, c_void_p, c_uint32])

    """ PICO_STATUS ps6000SetSigGenArbitrary
        (
            int16_t                    handle,
            int32_t                    offsetVoltage,
            uint32_t                   pkToPk,
            uint32_t                   startDeltaPhase,
            uint32_t                   stopDeltaPhase,
            uint32_t                   deltaPhaseIncrement,
            uint32_t                   dwellCount,
            int16_t                   *arbitraryWaveform,
            int32_t                    arbitraryWaveformSize,
            PS6000_SWEEP_TYPE          sweepType,
            PS6000_EXTRA_OPERATIONS    operation,
            PS6000_INDEX_MODE          indexMode,
            uint32_t                   shots,
            uint32_t                   sweeps,
            PS6000_SIGGEN_TRIG_TYPE    triggerType,
            PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
            int16_t                    extInThreshold
        ); """
    make_symbol(ldlib, "SetSigGenArbitrary", "ps6000SetSigGenArbitrary", c_uint32,
                [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
                 c_int32, c_int32, c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

    """ PICO_STATUS ps6000SetSigGenBuiltIn
        (
            int16_t                    handle,
            int32_t                    offsetVoltage,
            uint32_t                   pkToPk,
            int16_t                    waveType,
            float                      startFrequency,
            float                      stopFrequency,
            float                      increment,
            float                      dwellTime,
            PS6000_SWEEP_TYPE          sweepType,
            PS6000_EXTRA_OPERATIONS    operation,
            uint32_t                   shots,
            uint32_t                   sweeps,
            PS6000_SIGGEN_TRIG_TYPE    triggerType,
            PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
            int16_t                    extInThreshold
        ); """
    make_symbol(ldlib, "SetSigGenBuiltIn", "ps6000SetSigGenBuiltIn", c_uint32,
                [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float,
                 c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

    """ PICO_STATUS ps6000SetSigGenBuiltInV2
        (
            int16_t                    handle,
            int32_t                    offsetVoltage,
            uint32_t                   pkToPk,
            int16_t                    waveType,
            double                     startFrequency,
            double                     stopFrequency,
            double                     increment,
            double                     dwellTime,
            PS6000_SWEEP_TYPE          sweepType,
            PS6000_EXTRA_OPERATIONS    operation,
            uint32_t                   shots,
            uint32_t                   sweeps,
            PS6000_SIGGEN_TRIG_TYPE    triggerType,
            PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
            int16_t                    extInThreshold
        ); """

    """ PICO_STATUS ps6000SetSigGenPropertiesArbitrary
        (
            int16_t                    handle,
            int32_t                    offsetVoltage,
            uint32_t                   pkToPk,
            uint32_t                   startDeltaPhase,
            uint32_t                   stopDeltaPhase,
            uint32_t                   deltaPhaseIncrement,
            uint32_t                   dwellCount,
            PS6000_SWEEP_TYPE          sweepType,
            uint32_t                   shots,
            uint32_t                   sweeps,
            PS6000_SIGGEN_TRIG_TYPE    triggerType,
            PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
            int16_t                    extInThreshold
        ); """
    make_symbol(ldlib, "SigGenPropertiesArbitrary", "ps6000SetSigGenPropertiesArbitrary", c_uint32,
                [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32,
                 c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

    """ PICO_STATUS ps6000SetSigGenPropertiesBuiltIn
        (
            int16_t                    handle,
            int32_t                    offsetVoltage,
            uint32_t                   pkToPk,
            double                     startFrequency,
            double                     stopFrequency,
            double                     increment,
            double                     dwellTime,
            PS6000_SWEEP_TYPE          sweepType,
            uint32_t                   shots,
            uint32_t                   sweeps,
            PS6000_SIGGEN_TRIG_TYPE    triggerType,
            PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
            int16_t                    extInThreshold
        ); """
    make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps6000SetSigGenPropertiesBuiltIn", c_uint32,
                [c_int16, c_int32, c_uint32, c_double, c_double, c_double, c_double,
                 c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

    """ PICO_STATUS ps6000SigGenFrequencyToPhase
        (
            int16_t            handle,
            double             frequency,
            PS6000_INDEX_MODE  indexMode,
            uint32_t           bufferLength,
            uint32_t          *phase
        ); """
    make_symbol(ldlib, "SigGenFrequencyToPhase", "ps6000SigGenFrequencyToPhase", c_uint32,
                [c_int16, c_double, c_int32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000SigGenArbitraryMinMaxValues
        (
            int16_t   handle,
            int16_t  *minArbitraryWaveformValue,
            int16_t  *maxArbitraryWaveformValue,
            uint32_t *minArbitraryWaveformSize,
            uint32_t *maxArbitraryWaveformSize
        ); """
    make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps6000SigGenArbitraryMinMaxValues", c_uint32,
                [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

    """ PICO_STATUS ps6000SigGenSoftwareControl
        (
            int16_t  handle,
            int16_t  state
        ); """
    make_symbol(ldlib, "SigGenSoftwareControl", "ps6000SigGenSoftwareControl", c_uint32, [c_int16, c_int16])

    """ PICO_STATUS ps6000SetSimpleTrigger
        (
            int16_t                     handle,
            int16_t                     enable,
            PS6000_CHANNEL              source,
            int16_t                     threshold,
            PS6000_THRESHOLD_DIRECTION  direction,
            uint32_t                    delay,
            int16_t                     autoTrigger_ms
        ); """
    make_symbol(ldlib, "SetSimpleTrigger", "ps6000SetSimpleTrigger", c_uint32,
                [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

    """ PICO_STATUS ps6000SetEts
        (
            int16_t          handle,
            PS6000_ETS_MODE  mode,
            int16_t          etsCycles,
            int16_t          etsInterleave,
            int32_t         *sampleTimePicoseconds
        ); """
    make_symbol(ldlib, "SetEts", "ps6000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

    """ PICO_STATUS ps6000SetTriggerChannelProperties
        (
            int16_t                            handle,
            PS6000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
            int16_t                            nChannelProperties,
            int16_t                            auxOutputEnable,
            int32_t                            autoTriggerMilliseconds
        ); """
    make_symbol(ldlib, "SetTriggerChannelProperties", "ps6000SetTriggerChannelProperties", c_uint32,
                [c_int16, c_void_p, c_int16, c_int16, c_int32])

    """ PICO_STATUS ps6000SetTriggerChannelConditions
        (
            int16_t                    handle,
            PS6000_TRIGGER_CONDITIONS *conditions,
            int16_t                    nConditions
        ); """
    make_symbol(ldlib, "SetTriggerChannelConditions", "ps6000SetTriggerChannelConditions", c_uint32,
                [c_int16, c_void_p, c_int16])

    """ PICO_STATUS ps6000SetTriggerChannelDirections
        (
            int16_t                       handle,
            PS6000_THRESHOLD_DIRECTION  channelA,
            PS6000_THRESHOLD_DIRECTION  channelB,
            PS6000_THRESHOLD_DIRECTION  channelC,
            PS6000_THRESHOLD_DIRECTION  channelD,
            PS6000_THRESHOLD_DIRECTION  ext,
            PS6000_THRESHOLD_DIRECTION  aux
        ); """
    make_symbol(ldlib, "SetTriggerChannelDirections", "ps6000SetTriggerChannelDirections", c_uint32,
                [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

    """ PICO_STATUS ps6000SetTriggerDelay
        (
            int16_t   handle,
            uint32_t  delay
        ); """
    make_symbol(ldlib, "SetTriggerDelay", "ps6000SetTriggerDelay", c_uint32, [c_int16, c_uint32])

    """ PICO_STATUS ps6000SetPulseWidthQualifier
        (
            int16_t                     handle,
            PS6000_PWQ_CONDITIONS      *conditions,
            int16_t                     nConditions,
            PS6000_THRESHOLD_DIRECTION  direction,
            uint32_t                    lower,
            uint32_t                    upper,
            PS6000_PULSE_WIDTH_TYPE     type
        ); """
    make_symbol(ldlib, "SetPulseWidthQualifier", "ps6000SetPulseWidthQualifier", c_uint32,
                [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000IsTriggerOrPulseWidthQualifierEnabled
        (
            int16_t  handle,
            int16_t *triggerEnabled,
            int16_t *pulseWidthQualifierEnabled
        ); """
    make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps6000IsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                [c_int16, c_void_p, c_void_p])

    """ PICO_STATUS ps6000GetTriggerTimeOffset
        (
            int16_t            handle,
            uint32_t          *timeUpper,
            uint32_t          *timeLower,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           segmentIndex
        ); """

    """ PICO_STATUS ps6000GetTriggerTimeOffset64
        (
            int16_t              handle,
            int64_t           *time,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t      segmentIndex
        ); """
    make_symbol(ldlib, "GetTriggerTimeOffset", "ps6000GetTriggerTimeOffset64", c_uint32,
                [c_int16, c_void_p, c_void_p, c_uint32])

    """ PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk
        (
            int16_t            handle,
            uint32_t          *timesUpper,
            uint32_t          *timesLower,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex
        ); """

    """ PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk64
        (
            int16_t            handle,
            int64_t           *times,
            PS6000_TIME_UNITS *timeUnits,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex
        ); """
    make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps6000GetValuesTriggerTimeOffsetBulk64", c_uint32,
                [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

    """ PICO_STATUS ps6000SetDataBuffers
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *bufferMax,
            int16_t           *bufferMin,
            uint32_t           bufferLth,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffers", "ps6000SetDataBuffers", c_uint32,
                [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetDataBuffer
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *buffer,
            uint32_t           bufferLth,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffer", "ps6000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_uint32, c_int32])

    """ PICO_STATUS PREF2 PREF3 (ps6000SetDataBufferBulk)
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *buffer,
            uint32_t           bufferLth,
            uint32_t           waveform,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBufferBulk", "ps6000SetDataBufferBulk", c_uint32,
                [c_int16, c_int32, c_void_p, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetDataBuffersBulk
        (
            int16_t            handle,
            PS6000_CHANNEL     channel,
            int16_t           *bufferMax,
            int16_t           *bufferMin,
            uint32_t           bufferLth,
            uint32_t           waveform,
            PS6000_RATIO_MODE  downSampleRatioMode
        ); """
    make_symbol(ldlib, "SetDataBuffersBulk", "ps6000SetDataBuffersBulk", c_uint32,
                [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_uint32, c_int32])

    """ PICO_STATUS ps6000SetEtsTimeBuffer
        (
            int16_t   handle,
            int64_t  *buffer,
            uint32_t  bufferLth
        ); """
    make_symbol(ldlib, "SetEtsTimeBuffer", "ps6000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_uint32])

    """ PICO_STATUS ps6000SetEtsTimeBuffers
        (
            int16_t   handle,
            uint32_t *timeUpper,
            uint32_t *timeLower,
            uint32_t  bufferLth
        ); """

    """ PICO_STATUS ps6000RunBlock
        (
            int16_t           handle,
            uint32_t          noOfPreTriggerSamples,
            uint32_t          noOfPostTriggerSamples,
            uint32_t          timebase,
            int16_t           oversample,
            int32_t          *timeIndisposedMs,
            uint32_t          segmentIndex,
            ps6000BlockReady  lpReady,
            void             *pParameter
        ); """
    make_symbol(ldlib, "RunBlock", "ps6000RunBlock", c_uint32,
                [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p])

    """ PICO_STATUS ps6000IsReady
        (
            int16_t  handle,
            int16_t *ready
        ); """
    make_symbol(ldlib, "IsReady", "ps6000IsReady", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000RunStreaming
        (
            int16_t            handle,
            uint32_t          *sampleInterval,
            PS6000_TIME_UNITS  sampleIntervalTimeUnits,
            uint32_t           maxPreTriggerSamples,
            uint32_t           maxPostPreTriggerSamples,
            int16_t            autoStop,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           overviewBufferSize
        ); """
    make_symbol(ldlib, "RunStreaming", "ps6000RunStreaming", c_uint32,
                [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

    """ PICO_STATUS ps6000GetStreamingLatestValues
        (
            int16_t               handle,
            ps6000StreamingReady  lpPs6000Ready,
            void                 *pParameter
        ); """
    make_symbol(ldlib, "GetStreamingLatestValues", "ps6000GetStreamingLatestValues", c_uint32,
                [c_int16, c_void_p, c_void_p])

    """ PICO_STATUS ps6000NoOfStreamingValues
        (
            int16_t   handle,
            uint32_t *noOfValues
        ); """
    make_symbol(ldlib, "NoOfStreamingValues", "ps6000NoOfStreamingValues", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000GetMaxDownSampleRatio
        (
            int16_t            handle,
            uint32_t           noOfUnaggreatedSamples,
            uint32_t          *maxDownSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex
        ); """
    make_symbol(ldlib, "GetMaxDownSampleRatio", "ps6000GetMaxDownSampleRatio", c_uint32,
                [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

    """ PICO_STATUS ps6000GetValues
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValues", "ps6000GetValues", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesBulk
        (
            int16_t            handle,
            uint32_t          *noOfSamples,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesBulk", "ps6000GetValuesBulk", c_uint32,
                [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

    """ PICO_STATUS ps6000GetValuesAsync
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t           noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            void              *lpDataReady,
            void              *pParameter
        ); """
    make_symbol(ldlib, "GetValuesAsync", "ps6000GetValuesAsync", c_uint32,
                [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

    """ PICO_STATUS ps6000GetValuesOverlapped
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           segmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesOverlapped", "ps6000GetValuesOverlapped", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesOverlappedBulk
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            int16_t           *overflow
        ); """
    make_symbol(ldlib, "GetValuesOverlappedBulk", "ps6000GetValuesOverlappedBulk", c_uint32,
                [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

    """ PICO_STATUS ps6000GetValuesBulkAsyc
        (
            int16_t            handle,
            uint32_t           startIndex,
            uint32_t          *noOfSamples,
            uint32_t           downSampleRatio,
            PS6000_RATIO_MODE  downSampleRatioMode,
            uint32_t           fromSegmentIndex,
            uint32_t           toSegmentIndex,
            int16_t           *overflow
        ); """

    """ PICO_STATUS ps6000GetNoOfCaptures
        (
            int16_t   handle,
            uint32_t *nCaptures
        ); """
    make_symbol(ldlib, "GetNoOfCaptures", "ps6000GetNoOfCaptures", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000GetNoOfProcessedCaptures
        (
            int16_t   handle,
            uint32_t *nProcessedCaptures
        ); """
    make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps6000GetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

    """ PICO_STATUS ps6000Stop
        (
            int16_t  handle
        ); """
    make_symbol(ldlib, "Stop", "ps6000Stop", c_uint32, [c_int16, ])

    """ PICO_STATUS ps6000SetNoOfCaptures
        (
            int16_t   handle,
            uint32_t  nCaptures
        ); """
    make_symbol(ldlib, "SetNoOfCaptures", "ps6000SetNoOfCaptures", c_uint32, [c_int16, c_uint32])

    """ PICO_STATUS ps6000SetWaveformLimiter
        (
            int16_t   handle,
            uint32_t  nWaveformsPerSecond
        ); """
    make_symbol(ldlib, "SetWaveformLimiter", "ps6000SetWaveformLimiter", c_uint32, [c_int16, c_uint32])

    """ PICO_STATUS ps6000EnumerateUnits
        (
            int16_t *count,
            int8_t  *serials,
            int16_t *serialLth
        ); """
    make_symbol(ldlib, "EnumerateUnits", "ps6000EnumerateUnits", c_uint32, [c_void_p, c_void_p, c_void_p])

    """ PICO_STATUS ps6000SetExternalClock
        (
            int16_t                    handle,
            PS6000_EXTERNAL_FREQUENCY  frequency,
            int16_t                    threshold
        ); """
    make_symbol(ldlib, "SetExternalClock", "ps6000SetExternalClock", c_uint32, [c_int16, c_int32, c_int16])

    """ PICO_STATUS ps6000PingUnit
        (
            int16_t  handle
        ); """
    make_symbol(ldlib, "PingUnit", "ps6000PingUnit", c_uint32, [c_int16, ])

    """ PICO_STATUS ps6000GetAnalogueOffset
        (
            int16_t          handle,
            PS6000_RANGE     range,
            PS6000_COUPLING  coupling,
            float           *maximumVoltage,
            float           *minimumVoltage
        ); """
    make_symbol(ldlib, "GetAnalogueOffset", "ps6000GetAnalogueOffset", c_uint32,
                [c_int16, c_int32, c_int32, c_void_p, c_void_p])