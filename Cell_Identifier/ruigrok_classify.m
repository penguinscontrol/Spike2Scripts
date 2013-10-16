function [ out1, out2] = ruigrok_classify( in )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
if ~isa(in,'unit')
    error('input not a unit');
end

for a = 1:length(in)
    if strcmp(in(a).label,'unclassified')
        if in(a).isi_med < 0.02
            in(a).label = 'purkinje';
        else
        end
    end
end

for a = 1:length(in)
    if strcmp(in(a).label,'unclassified')
        if in(a).log_cv > 0.38 || in(a).freq_bar < 0.5
            in(a).label = 'granule';
        elseif in(a).log_cv < 0.34 || in(a).freq_bar > 0.6
        else
            in(a).label = 'border';
        end
    end
end

for a = 1:length(in)
    if strcmp(in(a).label,'unclassified')
        if in(a).mean_cv2 <0.24
            in(a).label = 'ub';
        elseif in(a).mean_cv2 > 0.28
        else
            in(a).label = 'border';
        end
    end
end

for a = 1:length(in)
    if strcmp(in(a).label,'unclassified')
        if in(a).log_cv > 0.17 || in(a).fifth < 0.022
            in(a).label = 'stellate';
        elseif in(a).log_cv < 0.15 || in(a).fifth > 0.044
        else
            in(a).label = 'border';
        end
    end
end

for a = 1:length(in)
    if strcmp(in(a).label,'unclassified')
        if in(a).isi_med > 0.32
            in(a).label = 'stellate';
        elseif in(a).isi_med < 0.30
        else
            in(a).label = 'border';
        end
    end
end

out1 = {in.label};
out2 = in;

end

