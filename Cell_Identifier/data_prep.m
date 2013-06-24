function out = data_prep()

cd('E:\\Spike_Sorting\\spike2temp\\');

% Variables from Spike2, uncomment for debugging

load('holdINTH.mat'); % post simple spike data
tn1 = whos; % temporary name holder
tn2 = tn1.name;
eval(['inth = ', tn2,';']); % get data as a struct
clearvars -except inth newname

load('holdwaves.mat');
tn1 = whos; % temporary name holder
tn2 = tn1.name;
eval(['waves = ', tn2,';']); % get data as a struct
[subj, coord, depth] = extract_info(tn2);
clearvars -except inth waves subj coord depth newname

inth_kurt = kurtosis(inth.values);
inth_skew = skewness(inth.values);
inth_std = std(inth.values);
inth_bar = mean(inth.values);

[mini, maxi, pk2pk, wid] = get_wave_feat(waves);

out = unit('unclassified',mean(maxi),mean(mini),mean(pk2pk),mean(wid),inth_kurt,inth_skew,inth_std,inth_bar,depth,coord.lm,coord.ap);
end