cd('E:\\Spike_Sorting\\spike2temp\\');

% Variables from Spike2, uncomment for debugging

load('holdINTH.mat'); % post simple spike data
tn1 = whos; % temporary name holder
tn2 = tn1.name;
eval(['inth = ', tn2,';']); % get data as a struct
clearvars -except inth

load('holdwaves.mat');
tn1 = whos; % temporary name holder
tn2 = tn1.name;
eval(['waves = ', tn2,';']); % get data as a struct
[subj, coord, depth] = extract_info(tn2);
clearvars -except inth waves subj coord depth

inth.kurt = kurtosis(inth.values);
inth.skew = skewness(inth.values);
inth.std = std(inth.values);
inth.mean = mean(inth.values);

waves = get_wave_feat(waves);