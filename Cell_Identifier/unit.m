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
        inth_kurt
        inth_skew
        inth_std
        inth_bar
        depth
        lm
        ap
    end
    
    methods
        function ThisUnit = set.label(ThisUnit,lbl)
            if ~(strcmpi(lbl,'unclassified')||...
                    strcmpi(lbl,'golgi')||...
                    strcmpi(lbl,'purkinje')||...
                    strcmpi(lbl,'fiber'))
                error('Improper classification! Choose another name.')
            end
            ThisUnit.label = lbl;
        end
                
        function NewUnit = unit(label,maxi,mini,pk2pk,wid,inth_kurt,inth_skew,inth_std,inth_bar,depth,lm,ap)
                NewUnit.label = label;
                NewUnit.maxi = maxi;
                NewUnit.mini = mini;
                NewUnit.pk2pk = pk2pk;
                NewUnit.wid = wid;
                NewUnit.inth_kurt = inth_kurt;
                NewUnit.inth_skew = inth_skew;
                NewUnit.inth_std = inth_std;
                NewUnit.inth_bar = inth_bar;
                NewUnit.depth = depth;
                NewUnit.lm = lm;
                NewUnit.ap = ap;
        end
    end
    
end

