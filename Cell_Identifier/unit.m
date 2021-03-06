classdef unit
    %UNIT: one putative neuron
    %   Detailed explanation goes here
    
    properties
        label = 'unclassified'
    end
    
    properties (SetAccess = protected)
        maxi
        mini
        pk2pk
        wid
        isi_kurt
        isi_skew
        isi_std
        isi_bar
        isi_med
        isi_cv
        freq_bar
        freq_med
        log_cv
        fifth
        med_cv2
        mean_cv2
        depth
        lm
        ap
        fname
    end
    
    methods
        function ThisUnit = set.label(ThisUnit,lbl)
            if ~(strcmpi(lbl,'unclassified')||...
                    strcmpi(lbl,'golgi')||...
                    strcmpi(lbl,'purkinje')||...
                    strcmpi(lbl,'dentate')||...
                    strcmpi(lbl,'ub')||...
                    strcmpi(lbl,'basket')||...
                    strcmpi(lbl,'stellate')||...
                    strcmpi(lbl,'granule')||...
                    strcmpi(lbl,'border')||...
                    strcmpi(lbl,'fiber'))
                error('Improper classification! Choose another name.')
            end
            ThisUnit.label = lbl;
        end
                
        function NewUnit = unit(label,maxi,mini,pk2pk,wid,isi_kurt,isi_skew,isi_std,isi_bar,isi_med,isi_cv,freq_bar,freq_med,log_cv,fifth,med_cv2,mean_cv2,depth,lm,ap,fname)
                NewUnit.label = label;
                NewUnit.maxi = maxi;
                NewUnit.mini = mini;
                NewUnit.pk2pk = pk2pk;
                NewUnit.wid = wid;
                NewUnit.isi_kurt = isi_kurt;
                NewUnit.isi_skew = isi_skew;
                NewUnit.isi_std = isi_std;
                NewUnit.isi_bar = isi_bar;
                NewUnit.isi_med = isi_med;
                NewUnit.isi_cv = isi_cv;
                NewUnit.freq_bar = freq_bar;
                NewUnit.freq_med = freq_med;
                NewUnit.log_cv = log_cv;
                NewUnit.fifth = fifth;
                NewUnit.med_cv2 = med_cv2;
                NewUnit.mean_cv2 = mean_cv2;
                NewUnit.depth = depth;
                NewUnit.lm = lm;
                NewUnit.ap = ap;
                NewUnit.fname = fname;
        end
    end
    
end

