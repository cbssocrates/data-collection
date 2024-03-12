clearinfo()
dir$ = "./data/"
outputFile$ = dir$ + "statistics.txt"
mfccFile$ = dir$ + "mfcc.txt"
deleteFile: outputFile$
Create Strings as folder list: "folders", dir$
nFolders = Get number of strings
for language from 1 to nFolders
    selectObject: "Strings folders"
    foldername$ = Get string: language
    Create Strings as folder list: "participants", dir$ + foldername$
    nParticipants = Get number of strings
    countOfAnnotatedSpeakers = 0
    for participant from 1 to nParticipants
        selectObject: "Strings participants"
        participantSlNo$ = Get string: participant
        Create Strings as file list: "tgfiles", dir$+ foldername$ + "/" + participantSlNo$ + "/*.TextGrid"       
        nFiles = Get number of strings
        if nFiles <> 0
            countOfAnnotatedSpeakers = countOfAnnotatedSpeakers + 1
        endif
        for  tgfile from 1 to nFiles
            retroflexFlag = 0
            selectObject: "Strings tgfiles"
            tgFileName$ = Get string: tgfile
            tgFilePath$ = dir$+ foldername$ + "/" + participantSlNo$ + "/" + tgFileName$
            Read from file... 'tgFilePath$'
            objectName$ = selected$ ("TextGrid")
            numberOfIntervals = Get number of intervals... 1
            for intervalIndex from 1 to numberOfIntervals
                t0 = -1
                t1 = -1
                t2 = -1
                t3 = -1
                select TextGrid 'objectName$'
                intervalLabel$ = Get label of interval... 1 intervalIndex
                if intervalLabel$ == "TT" or intervalLabel$ == "T" or intervalLabel$ == "t" or intervalLabel$ == "Tt" or intervalLabel$ == "tT" or intervalLabel$ == "tt"
                    retroflexFlag = 1
                    if (intervalIndex - 1) <> 0
                       intervalLabel$ = Get label of interval... 1 (intervalIndex - 1)
                       appendFile: outputFile$, intervalLabel$, " "
                       v1$ = intervalLabel$
                       t0 = Get starting point... 1 (intervalIndex - 1)
                    else
                        #if interval doesn't exist
                        appendFile: outputFile$, "x "
                        v1$ = "x"
                    endif
                    t1 = Get starting point... 1 intervalIndex
                    t2 = Get end point... 1 intervalIndex
                    if (intervalIndex + 1) <= numberOfIntervals
                        intervalLabel$ = Get label of interval... 1 (intervalIndex + 1)
                        appendFile: outputFile$, intervalLabel$, " "
                        v2$ = intervalLabel$
                        t3 = Get end point... 1 (intervalIndex + 1)
                    else
                        #if interval doesn't exist
                        appendFile: outputFile$, "x "
                        v2$ = "x"
                    endif
                appendFileLine: outputFile$, t0, " ", t1, " ", t2, " ", t3

                #This section of code converts sound to MFCC
                soundFilePath$ = tgFilePath$ - "TextGrid" + "wav"
                sound = Read from file... 'soundFilePath$'
                selectObject: sound
                Extract part: (t1 - 0.03), t1, "rectangular", 1, "no"
                mfcc = To MFCC: 12, 0.015, 0.005, 100, 100, 0
                v1MFCCFilePath$ = tgFilePath$ - ".TextGrid" + "-v1.MFCC"
                Save as text file: v1MFCCFilePath$
                selectObject: sound
                Extract part: t2, (t2 + 0.03), "rectangular", 1, "no"
                mfcc = To MFCC: 12, 0.015, 0.005, 100, 100, 0
                v2MFCCFilePath$ = tgFilePath$ - ".TextGrid" + "-v2.MFCC"
                Save as text file: v2MFCCFilePath$
                endif
            endfor
            if retroflexFlag == 0
                appendInfoLine: tgFilePath$ + " e retroflex pelam na"
            endif
        endfor
    endfor
    appendInfoLine: foldername$ + " : " + string$ (countOfAnnotatedSpeakers) + " out of " + string$ (nParticipants) + " annotated."
endfor